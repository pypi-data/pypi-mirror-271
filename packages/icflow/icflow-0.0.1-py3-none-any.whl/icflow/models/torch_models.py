import logging
import time

import torch
from torchvision import models as torch_models
import torch.nn as nn
import torch.optim as optim

import segmentation_models_pytorch as smp

from icflow.output.visualization import plot_grid
from icflow.models.metrics import Metrics


class TorchModel:
    def __init__(self, settings, target_device) -> None:
        self.name = settings["model_name"]
        self.num_classes = settings["num_classes"]
        self.target_device = target_device
        self.optimizer_settings = settings["optimizer"]

        if "stopping_criteria" in settings:
            self.stopping_criteria = settings["stopping_criteria"]
        else:
            self.stopping_criteria = None
        self.optimizer = None
        self.model = None

    def load_model(self):
        logging.info("Loading model")
        # device = "mps" if torch.cuda.is_available() else "cpu"
        if self.target_device == "cuda" and torch.cuda.is_available():
            self.device = torch.device("cuda")
            logging.info("Loading on GPU")
        else:
            self.device = torch.device("cpu")
            logging.info("Loading on CPU")

        if self.name == "resnet18":
            logging.info("Loading resnet model")
            self.model = torch_models.resnet18(
                weights=torch_models.ResNet18_Weights.DEFAULT
            )
            self.model.fc = nn.Linear(self.model.fc.in_features, self.num_classes)
        elif self.name == "mobilenet_v2":
            logging.info("Loading mobilenet_v2 model")
            self.model = torch_models.mobilenet_v2(
                weights=torch_models.MobileNet_V2_Weights.DEFAULT
            )
            self.model.classifier[1] = nn.Linear(
                self.model.classifier[1].in_features, self.num_classes
            )
        elif self.name == "deeplabv3":
            self.model = smp.DeepLabV3Plus(classes=self.num_classes)
        else:
            raise RuntimeError(f"Model name {self.name} not supported")

        self.model = self.model.to(self.device)
        self.loss_func = nn.CrossEntropyLoss()

        optimizer_name = self.optimizer_settings["name"]
        if optimizer_name == "sgd":
            learning_rate = self.optimizer_settings["learning_rate"]
            momentum = self.optimizer_settings["momentum"]
            self.optimizer = optim.SGD(
                self.model.parameters(), lr=learning_rate, momentum=momentum
            )
        elif optimizer_name == "adam":
            learning_rate = self.optimizer_settings["learning_rate"]
            torch.optim.Adam(params=self.model.parameters(), lr=learning_rate)
        else:
            raise RuntimeError(f"Unsupported optimizer name {optimizer_name}")
        logging.info("Finished Loading model")

    def on_training_batch(self, x, y):
        x, y = x.to(self.device), y.to(self.device)
        self.optimizer.zero_grad()

        logging.debug("Applying model")
        preds = self.model(x)

        logging.debug("Calculating metrics")
        loss = self.metrics.loss(preds, y)
        self.metrics.on_training_batch("training", preds, y, loss.item())

        logging.debug("Doing backward pass")
        loss.backward()

        logging.debug("Stepping optimizer")
        self.optimizer.step()

    def after_training_batch(self, epoch_count, batch_count):
        self.output_handler.on_batch_end(epoch_count, batch_count, self.metrics)

    def on_before_train(self, num_epochs):
        self.output_handler.num_epochs = num_epochs
        self.metrics.cache.on_start_session()
        self.output_handler.start_time = time.time()

    def on_epoch_start(self, epoch_count):
        self.metrics.cache.on_start_batch("training")
        self.output_handler.on_epoch_start(epoch_count)

    def on_epoch_end(self, epoch_count):
        self.metrics.cache.on_end_epoch()
        self.output_handler.on_epoch_end(epoch_count, self.metrics)

        return self.check_stopping_criteria()

    def check_stopping_criteria(self):
        validation_loss = self.metrics.cache.epoch["validation"]["loss"]

        if self.best_loss > validation_loss:
            logging.info(
                f"Loss decreased from {self.best_loss:.3f} to {validation_loss:.3f}."
            )
            self.best_loss = validation_loss
            self.decrease += 1
            if self.decrease % 2 == 0:
                logging.info("Saving the model with the best loss value...")
                # torch.save(self.model, f"{save_path}/{save_prefix}_best_model.pt")

        if validation_loss > self.best_loss:
            self.not_improve += 1
            self.best_loss = validation_loss
            logging.info(f"Loss did not decrease for {self.not_improve} epoch(s)!")
            if self.not_improve == self.early_stop_threshold:
                num_epoch = self.early_stop_threshold
                stop_reason = f"loss value did not decrease for {num_epoch} epochs"
                logging.info(f"Stopping training process because {stop_reason}")
                return False
        return True

    def train(self, dataloaders, output_handler, output_settings, num_epochs=10):

        logging.info(f"Running {num_epochs} epochs")
        self.output_handler = output_handler

        self.metrics = Metrics(
            output_settings["metrics"], self.loss_func, num_classes=self.num_classes
        )
        self.metrics.set_count("training", len(dataloaders.train_dataloader))
        self.metrics.set_count("validation", len(dataloaders.val_dataloader))

        self.on_before_train()

        batch_count = 0
        for epoch in range(num_epochs):
            self.on_epoch_start()
            self.model.train()
            for x, y in dataloaders.train_dataloader:
                self.on_training_batch(x, y)
                self.after_training_batch(epoch, batch_count)
                batch_count += 1
            self.do_validation(dataloaders.val_dataloader)
            should_stop = self.on_epoch_end(epoch)
            if should_stop:
                break

    def do_validation(self, dataloader):
        logging.info("Validation step")
        self.model.eval()
        self.metrics.cache.on_start_batch("validation")
        with torch.no_grad():
            for x, y in dataloader:
                x, y = x.to(self.device), y.to(self.device)
                preds = self.model(x)
                self.metrics.on_validation_batch(preds, y)

    def do_inference(self, dataloader, num_images=15):
        cols = num_images // 3
        rows = num_images // cols

        ims, gts, preds = [], [], []
        for idx, data in enumerate(dataloader):
            x, y = data
            with torch.no_grad():
                pred = torch.argmax(self.model(x.to(self.device)), dim=1)
            ims.append(x)
            gts.append(y)
            preds.append(pred)
            if idx == num_images:
                break

        plot_grid(cols, rows, zip(ims, gts, preds))

    def save(self, path):
        torch.save(self.model.state_dict(), path)
