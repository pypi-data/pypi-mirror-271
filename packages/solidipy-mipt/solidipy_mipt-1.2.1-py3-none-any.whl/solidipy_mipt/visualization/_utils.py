"""Utils for visualization.

This module contain utils for visualization.
"""

import matplotlib.pyplot as plt
import warnings
import os


def _save_fig(
    path_to_save: str = "",
) -> None:
    """
    Save figure to file.

    Args:
        path_to_save: Path to save figure.

    Raises:
        ValueError: If path to file is empty.
    """

    if (path_to_save == ""):
        raise ValueError(
            "Path to file must be not empty."
        )

    if os.path.exists(path_to_save):
        warnings.warn(
            f"The file at "
            f"'{os.path.abspath(path_to_save)}' "
            f"already exists.",
            DeprecationWarning
        )

    plt.savefig(path_to_save)
