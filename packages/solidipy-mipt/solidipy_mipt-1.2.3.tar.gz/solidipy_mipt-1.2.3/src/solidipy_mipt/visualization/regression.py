"""Visualization of regressor.

This module contain methods for regressor visualization.
"""

import matplotlib.pyplot as plt
import numpy as np

from ._utils import _save_fig

FIGSIZE = (16, 9)


def visualize_regressor(
    abscissa: np.ndarray,
    ordinates: np.ndarray,
    predictions: np.ndarray,
    error: np.ndarray,
    path_to_save: str = ""
) -> None:
    """
    Visualize regressor prediction.

    Args:
        abscessa: Abscissa of data.
        ordinates: Ordinates of data.
        prediction: Regressor prediction.
        error: Prediction error.
        path_to_save: Path to save visualization.
            Defaults to "".

    Examples:
        >>> import numpy as np
        >>> from solidipy_mipt import train_test_split
        >>> X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        >>> y = np.array([0, 1, 0, 1])
        >>> X_train, X_test, y_train, y_test = train_test_split(X, y, train_ratio=0.6, shuffle=True)
    """

    # TODO check sizes of input data

    _, axis = plt.subplots(figsize=FIGSIZE)
    axis.scatter(abscissa, ordinates, label='source', c="royalblue", s=1)
    axis.plot(abscissa, predictions, label='prediction', c="steelblue")
    axis.plot(abscissa, predictions - error, label='error', linestyle='--', c="red")
    axis.plot(abscissa, predictions + error, linestyle='--', c="red")
    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()

    if (path_to_save):
        _save_fig(path_to_save)
