"""Visualization for base diagrams.

This module contain methods for base diagrams visualization.
"""

import numpy as np
import matplotlib.pyplot as plt

from itertools import cycle
from .colors import Colors

FIGSIZE = (16, 9)


def visualize_scatter(
    points: np.ndarray,
    labels: np.ndarray,
    colors: list[Colors] | None = None,
    axis: plt.Axes | None = None,
) -> None:
    """
    Visualize scatter with labels.

    Args:
        points: Points.
        labels: Labels.
        colors: Colors for labels.
        axis: Axis.
    """

    # TODO chech sizes of input data

    if colors is None:
        colors = list(Colors)

    colors_cycle = cycle(colors)
    labels_unique = np.unique(labels)

    if axis is None:
        _, axis = plt.subplots(figsize=FIGSIZE)

    for label in labels_unique:
        label_mask = labels == label
        axis.scatter(*points[label_mask].T, color=next(colors_cycle))

    axis.grid(True)


def visualize_violin(
    data: np.ndarray,
    axis: plt.Axes
) -> None:
    """
    Visualize violin.

    Args:
        data: Data.
        axis: Axis.
    """

    axis.violinplot(
        data,
        vert=False,
        showmedians=True,
    )
    axis.set_yticks([])


def visualize_hist(
    data: np.ndarray,
    axis: plt.Axes
) -> None:
    """
    Visualize hist.

    Args:
        data: Data.
        axis: Axis.
    """

    axis.hist(
        data,
        bins=100,
        color="cornflowerblue",
        density=True,
        alpha=0.5,
    )


def visualize_boxplot(
    data: np.ndarray,
    axis: plt.Axes
) -> None:
    """
    Visualize boxplot.

    Args:
        data: Data.
        axis: Axis.
    """
        
    axis.boxplot(
        data,
        vert=False,
        patch_artist=True,
        boxprops=dict(facecolor="blue"),
        medianprops=dict(color="black"),
    )
