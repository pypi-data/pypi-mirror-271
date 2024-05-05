"""Visualization for distribution.

This module contain methods for distribution visualization.
"""

import matplotlib.pyplot as plt
import numpy as np

from enum import IntEnum
from ._utils import _save_fig


class DiagramType(IntEnum):
    VIOLIN = 1
    HIST = 2
    BOXPLOT = 3


plt.style.use("ggplot")
FIGSIZE = (16, 9)
SPACE = 0.2


def visualize_distribution(
    data: np.ndarray,
    diagram_type: DiagramType,
    path_to_save: str = "",
) -> None:
    """
    Visualize distribution. If distribution is 2D visualize 2 histograms,
      which provides additional information about the distribution of data along the axes.

    Args:
        data: The input data for distribution.
        diagram_type: The diagram type.
        path_to_save: Path to save visualization.
            If empty, show visualization in new window.
            Defaults to "".

    Examples:
        >>> import numpy as np
        >>> from solidipy_mipt.visualization import visualize_distribution
        >>> absc = np.random.normal(size=1000)
        >>> ordi = np.random.normal(size=1000)
        >>> data = np.column_stack([absc, ordi])
        >>> data = np.random.normal(size=1000)
        >>> visualize_distribution(
        ...     data=data,
        ...     diagram_type=Diagram_type.HIST,
        ...     path_to_save="TEST.png"
        ... )
    """

    if (len(data.shape) == 1):
        _visualize_distribution_1d(data, diagram_type, path_to_save)
    elif (len(data.shape) == 2 and data.shape[1] == 2):
        _visualize_distribution_2d(data, path_to_save)


def _visualize_distribution_1d(
    data: np.ndarray,
    diagram_type: DiagramType,
    path_to_save: str = "",
) -> None:
    """
    Visualize distribution.

    Args:
        data: Data for distribution.
        diagram_type: The diagram type.
        path_to_save: Path to save visualization.
            If empty, show visualization in new window.
    """

    _, axis = plt.subplots(figsize=FIGSIZE)

    match(diagram_type):
        case DiagramType.VIOLIN:
            axis.violinplot(
                data,
                vert=False,
                showmedians=True,
            )
            axis.set_yticks([])

        case DiagramType.HIST:
            axis.hist(
                data,
                bins=100,
                color="cornflowerblue",
                density=True,
                alpha=0.5,
            )

        case DiagramType.BOXPLOT:
            axis.boxplot(
                data,
                vert=False,
                patch_artist=True,
                boxprops=dict(facecolor="blue"),
                medianprops=dict(color="black"),
            )

    if (path_to_save):
        _save_fig(path_to_save)
    else:
        plt.show()


def _visualize_distribution_2d(
    data: np.ndarray,
    path_to_save: str = "",
) -> None:
    """
    Visualize distribution and 2 histograms,
      which provides additional information about the distribution of data along the axes.

    Args:
        data: Data for distribution.
        path_to_save: Path to save visualization.
            If empty, show visualization in new window.
    """

    figure = plt.figure(figsize=(8, 8))
    grid = plt.GridSpec(4, 4, wspace=SPACE, hspace=SPACE)

    axis_scatter = figure.add_subplot(grid[:-1, 1:])
    axis_hist_vert = figure.add_subplot(
        grid[:-1, 0],
        sharey=axis_scatter,
    )
    axis_hist_hor = figure.add_subplot(
        grid[-1, 1:],
        sharex=axis_scatter,
    )

    abscissa, ordinates = data[:, 0], data[:, 1]
    axis_scatter.scatter(
        abscissa,
        ordinates,
        color="cornflowerblue",
        alpha=0.5
    )
    axis_hist_hor.hist(
        abscissa,
        bins=50,
        density=True,
        color="cornflowerblue",
        alpha=0.5,
    )
    axis_hist_vert.hist(
        ordinates,
        bins=50,
        density=True,
        orientation="horizontal",
        color="cornflowerblue",
        alpha=0.5,
    )

    axis_hist_hor.invert_yaxis()
    axis_hist_vert.invert_xaxis()

    if (path_to_save):
        _save_fig(path_to_save)
    else:
        plt.show()
