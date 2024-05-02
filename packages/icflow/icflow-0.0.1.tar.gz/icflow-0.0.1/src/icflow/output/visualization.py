# import albumentations as A
# from albumentations.pytorch import ToTensorV2

# from torchvision import transforms as tfs
from matplotlib import pyplot as plt
import numpy as np
import random

ZEROS = [0.0, 0.0, 0.0]
ONES = [1.0, 1.0, 1.0]


def tensor_to_numpy(t, transform):
    if len(t) == 3:  # rgb
        return (
            (transform.inverse(t) * transform.scale())
            .detach()
            .cpu()
            .permute(1, 2, 0)
            .numpy()
            .astype(np.uint8)
        )
    else:
        return (t * transform.scale()).detach().cpu().numpy().astype(np.uint8)


class PlotConfig:
    def __init__(self, title, stride=4, size=(25, 20), transform=None) -> None:
        self.rows = 0
        self.cols = 0
        self.title = title
        self.stride = stride
        self.size = size
        self.transform = transform


def plot(plot_config, count, image, ground_truth=False):
    plt.subplot(plot_config.rows, plot_config.cols, count)
    if ground_truth:
        plt.imshow(tensor_to_numpy(image.squeeze(0).float()), plot_config.transform)
    else:
        plt.imshow(tensor_to_numpy(image.squeeze(0)), plot_config.transform)
    plt.axis("off")
    plt.title(plot_config.title)
    return count + 1


def plot_grid(cols, rows, data):
    plt.figure(figsize=(25, 20))
    count = 0
    for idx, (im, gt, pred) in enumerate(data):
        if idx == cols:
            break

        # First plot
        count = plot(cols, rows, count, im)

        # Second plot
        count = plot(cols, rows, count, im=gt, gt=True, title="Ground Truth")

        # Third plot
        count = plot(cols, rows, count, im=pred, title="Predicted Mask")


def visualize(dataset, num_images, plot_config):
    plt.figure(figsize=plot_config.size)
    plot_config.rows = num_images // plot_config.stride
    plot_config.cols = num_images // plot_config.rows
    count = 1
    indices = [random.randint(0, len(dataset) - 1) for _ in range(num_images)]

    for idx, index in enumerate(indices):
        if count == num_images + 1:
            break
        im, ground_truth = dataset[index]

        count = plot(plot_config, count, im=im)
        count = plot(plot_config, count, im=ground_truth, ground_truth=True)
