import logging
import time
from torch.utils.tensorboard import SummaryWriter

from icflow.utils.serialization import Config


class OutputHandler:
    def __init__(self, result_dir, config: Config) -> None:
        self.use_tensorboard = config.get("use_tensorboard", False)

        self.tb_writer: SummaryWriter | None = None
        if self.use_tensorboard:
            self.tb_writer = SummaryWriter(result_dir / "tensorboard")

        self.num_epochs = 0
        self.start_time = 0

    def on_epoch_start(self, epoch_count):
        logging.info(f"Starting Epoch [{epoch_count + 1}/{self.num_epochs}]")

    def on_batch_end(self, epoch_count, batch_count, metrics):
        # if self.use_tensorboard and scalar is not None:
        # self.tb_writer.add_scalar(msg, scalar, batch_count)
        loss = metrics.batch_cache["training"]["loss"]
        logging.info(f"Finished Batch {batch_count}, training loss: {loss}")

    def on_epoch_end(self, epoch_count, metrics):
        delta_time = time.time() - self.start_time
        # if self.use_tensorboard:
        # self.tb_writer.add_scalar(msg, scalar, epoch_count)
        logging.info(f"Finished Epoch [{epoch_count + 1}/{self.num_epochs}]. Results:")
        for line in self.serialize_metrics(delta_time, metrics):
            logging.info(line)

    def serialize_metrics(self, delta_time, metrics):
        lines = []
        lines.append(f"Train time {delta_time():.3f} secs")
        for key, value in metrics.batch_cache["training"].items():
            lines.append(f"training {key} -> {value:.3f}")
        for key, value in metrics.batch_cache["validation"].items():
            lines.append(f"validation {key} -> {value:.3f}")
