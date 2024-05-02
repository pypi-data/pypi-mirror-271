import numpy as np
import torch
from torch.nn import functional as F


class MetricsCache:
    def __init__(self, types) -> None:
        self.epoch: dict = {}
        self.batch: dict = {}
        self.types: list = []
        self.stages = ["training", "validation"]
        self.counts: dict = {}

    def on_start_session(self):
        for stage in self.stages:
            self.epoch[stage] = {}
            for type in self.types:
                self.batch[stage][type] = []
            self.batch[stage]["loss"] = []

    def on_start_batch(self, stage):
        self.batch[stage] = {}
        for type in self.types:
            self.batch[stage][type] = 0
        self.batch[stage]["loss"] = 0

    def add_batch_value(self, stage, type, value):
        self.batch[stage][type] = self.batch[stage][type] + value

    def on_end_epoch(self):
        for stage in self.stages:
            count = self.counts[stage]
            for type in self.types:
                self.batch[stage][type] = self.batch[stage][type] / count
                self.epoch[stage][type].append(self.batch[stage][type])
            self.batch[stage]["loss"] = self.batch[stage]["loss"] / count
            self.epoch[stage]["loss"].append(self.batch[stage]["loss"])


class Metrics:
    def __init__(self, settings, loss_fn, eps=1e-10, num_classes=2):
        self.types = settings["types"]
        self.armgax_loss = settings["argmax_loss"]
        self.num_classes = num_classes
        self.loss_fn = loss_fn
        self.eps = eps

        self.cache = MetricsCache()

    def do_softmax(self, pred):
        return torch.argmax(F.softmax(pred, dim=1), dim=1)

    def set_count(self, stage, count):
        self.cache.counts[stage] = count

    def calculate(self, pred, gt):
        results = {}
        if "pixel_accuracy" in self.types or "iou" in self.types:
            softmax_pred = self.do_softmax(pred)
            if "pixel_accuracy" in self.types:
                results["pixel_accuracy"] = self.pixel_accuracy(softmax_pred, gt)
            if "iou" in self.types:
                results["iou"] = self.mean_iou(softmax_pred, gt)
        if "accuracy" in self.types:
            results["accuracy"] = self.basic_accuracy(pred, gt)
        return results

    def to_contiguous(self, input):
        return input.contiguous().view(-1)

    def on_training_batch(self, pred, gt, loss):
        self.batch_calculate_and_append("training", pred, gt, loss)

    def on_validation_batch(self, pred, gt):
        self.batch_calculate_and_append("validation", pred, gt)

    def batch_calculate_and_append(self, stage, pred, gt, loss=None):
        if loss is None:
            self.cache.add_batch_value(stage, "loss", self.loss.item())
        else:
            self.cache.add_batch_value(stage, "loss", loss)
        for key, value in self.calculate(pred, gt).items():
            self.cache.add_batch_value(stage, key, value)

    def basic_accuracy(self, pred, gt):
        _, predicted = torch.max(pred, 1)
        return (predicted == gt).sum().item()

    def pixel_accuracy(self, pred, gt):
        with torch.no_grad():
            match = torch.eq(pred, gt).int()
        return float(match.sum()) / float(match.numel())

    def mean_iou(self):
        with torch.no_grad():
            self.gt = torch.argmax(self.gt, dim=1)
            pred = self.to_contiguous(self.pred)
            gt = self.to_contiguous(self.gt)

            iou_per_class = []
            for c in range(self.num_classes):
                match_pred = pred == c
                match_gt = gt == c
                if match_gt.long().sum().item() == 0:
                    iou_per_class.append(np.nan)
                else:
                    intersect = (
                        torch.logical_and(match_pred, match_gt).sum().float().item()
                    )
                    union = torch.logical_or(match_pred, match_gt).sum().float().item()

                    iou = (intersect + self.eps) / (union + self.eps)
                    iou_per_class.append(iou)
            return np.nanmean(iou_per_class)

    def loss(self, pred, gt):
        if self.armgax_loss:
            return self.loss_fn(pred, torch.argmax(gt, dim=1))
        else:
            return self.loss_fn(pred, gt)
