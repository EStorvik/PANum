from typing import Optional

import numpy as np
from ufl import as_tensor

from ..interpolator import Interpolator


class StiffnessTensor:
    """Heterogeneous and anisotropic general stiffness tensor. ONLY works in 2D"""

    def __init__(
        self,
        stiffness0: Optional[np.ndarray] = None,
        stiffness1: Optional[np.ndarray] = None,
        interpolator: Interpolator = (Interpolator()),
    ) -> None:
        """
        Initialize the heterogeneous and anisotropic stiffness tensor.

        Args:
            stiffness0 (np.ndarray, optional): Stiffness tensor for
                phasefield = 0. Defaults to None.
            stiffness1 (np.ndarray, optional): Stiffness tensor for
                phasefield = 1. Defaults to None.
            interpolator:
        """

        # Define interpolator
        self.interpolator = interpolator

        dim = 2

        # Define stiffness tensors
        if stiffness0 is None:
            self.stiffness0np = np.zeros((dim, dim, dim, dim))

            self.stiffness0np[0, 0, 0, 0] = 100
            self.stiffness0np[0, 0, 1, 1] = 20
            self.stiffness0np[0, 0, 1, 0] = 0
            self.stiffness0np[0, 0, 0, 1] = 0

            self.stiffness0np[1, 1, 0, 0] = 20
            self.stiffness0np[1, 1, 1, 1] = 100
            self.stiffness0np[1, 1, 1, 0] = 0
            self.stiffness0np[1, 1, 0, 1] = 0

            self.stiffness0np[0, 1, 0, 0] = 0
            self.stiffness0np[0, 1, 1, 1] = 0
            self.stiffness0np[0, 1, 1, 0] = 100
            self.stiffness0np[0, 1, 0, 1] = 100

            self.stiffness0np[1, 0, 0, 0] = 0
            self.stiffness0np[1, 0, 1, 1] = 0
            self.stiffness0np[1, 0, 1, 0] = 100
            self.stiffness0np[1, 0, 0, 1] = 100

            # print(self.stiffness0np.shape)
            self.stiffness0 = as_tensor(self.stiffness0np)
            # print(self.stiffness0.ufl_shape)

        else:
            self.stiffness0 = as_tensor(stiffness0)

        if stiffness1 is None:
            self.stiffness1np = np.zeros((dim, dim, dim, dim))

            self.stiffness1np[0, 0, 0, 0] = 1
            self.stiffness1np[0, 0, 1, 1] = 0.1
            self.stiffness1np[0, 0, 1, 0] = 0
            self.stiffness1np[0, 0, 0, 1] = 0

            self.stiffness1np[1, 1, 0, 0] = 0.1
            self.stiffness1np[1, 1, 1, 1] = 1
            self.stiffness1np[1, 1, 1, 0] = 0
            self.stiffness1np[1, 1, 0, 1] = 0

            self.stiffness1np[0, 1, 0, 0] = 0
            self.stiffness1np[0, 1, 1, 1] = 0
            self.stiffness1np[0, 1, 1, 0] = 1
            self.stiffness1np[0, 1, 0, 1] = 1

            self.stiffness1np[1, 0, 0, 0] = 0
            self.stiffness1np[1, 0, 1, 1] = 0
            self.stiffness1np[1, 0, 1, 0] = 1
            self.stiffness1np[1, 0, 0, 1] = 1

            self.stiffness1 = as_tensor(self.stiffness1np)

        else:
            self.stiffness1 = as_tensor(stiffness1)

    def __call__(self, pf, i, j, k, m):
        return self.stiffness0[i, j, k, m] + self.interpolator(pf) * (
            self.stiffness1[i, j, k, m] - self.stiffness0[i, j, k, m]
        )

    def prime(self, pf, i, j, k, m):
        return self.interpolator.prime(pf) * (
            self.stiffness1[i, j, k, m] - self.stiffness0[i, j, k, m]
        )
