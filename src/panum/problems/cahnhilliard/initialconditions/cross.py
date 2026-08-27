from .initialcondition import InitialConditionCahnHilliard
import numpy as np

class Cross(InitialConditionCahnHilliard):
    """Indicator function for a 2D cross centered in the unit square."""

    def __init__(self, width: float = 0.1) -> None:
        self.width: float = width

    def __call__(self, x):
        """Return 1 inside the cross arms and 0 elsewhere.

        Args:
            x (np.ndarray): Array of shape (2, n) with points
                in the unit square.
        """
        values = np.zeros(x.shape[1])
        cross_width = self.width
        values[
            np.logical_or(
                np.logical_and(
                    (np.abs(x[0] - 0.5) <= cross_width / 2),
                    (np.abs(x[1] - 0.5) <= cross_width),
                ),
                np.logical_and(
                    (np.abs(x[1] - 0.5) <= cross_width / 2),
                    (np.abs(x[0] - 0.5) <= cross_width),
                ),
            )
        ] = 1.0
        return values
