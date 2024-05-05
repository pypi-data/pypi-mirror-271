"""Visualization of comparison.

This module contain methods for comparison visualization.
"""

import matplotlib.pyplot as plt
import numpy as np

from .base_diagrams import visualize_scatter
from ._utils import _save_fig

FIGSIZE = (16, 9)


def visualize_comparison(
    points: np.ndarray,
    prediction: np.ndarray,
    expectation: np.ndarray,
    path_to_save: str = ""
) -> None:
    """
    Visualize comparison.

    Args:
        points: Points.
        prediction: Predicted labels.
        expectation: Expected labels.
        path_to_save: Path to save visualization.
            Defaults to "".

    Examples:
        >>> import numpy as np
        >>> from solidipy_mipt.visualization import visualize_comparison
        >>> x = np.array([
        ...     [1,1], [2,3], [3,1], [4,4], [6,2],
        ...     [3,8], [9,1], [8,3], [1,9], [8,4]
        ... ])
        >>> prediction = np.array([1,2,3,0,1,0,3,2,1,2])
        >>> expectation = np.array([1,2,1,5,1,4,7,2,1,2])
        >>> visualize_comparison(x,prediction=prediction, expectation=expectation)
    """

    # TODO chech sizes of input data

    _, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE)

    ax1.set_title("prediction", fontsize=15, fontweight="bold", c="dimgray")
    ax2.set_title("expectation", fontsize=15, fontweight="bold", c="dimgray")

    visualize_scatter(points, prediction, axis=ax1)
    visualize_scatter(points, expectation, axis=ax2)

    if (path_to_save):
        _save_fig(path_to_save)
