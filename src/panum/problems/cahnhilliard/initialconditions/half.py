from .initialcondition import InitialConditionCahnHilliard
import numpy as np


class Half(InitialConditionCahnHilliard):
    """Indicator function for a 2D half/half phasefield"""

    def __init__(self, width: float = 0.1) -> None:
        self.width: float = width

    def __call__(self, x):
        """Return 1 inside the cross arms and 0 elsewhere.

        Args:
            x (np.ndarray): Array of shape (2, n).
        """
        values = np.zeros(x.shape[1])
        values[x[0] < 0.5] = 1.0
        return values
