from typing import cast, TYPE_CHECKING, Union

import numpy as np
import numpy.typing as npt
from ufl.core.expr import Expr as UFLExpr

from .parameters import ParametersBiharmonic

if TYPE_CHECKING:
    from dolfinx.fem import Constant

ArrayOrFloat = Union[float, npt.NDArray[np.floating]]
UFLScalar = Union[float, "Constant", UFLExpr]


class ManufacturedSolutionBiharmonic:
    """ """

    def __init__(self, parameters: ParametersBiharmonic) -> None:
        """Initialize the manufactured solution.

        Args:
            parameters: Biharmonic equation parameters, used for the mobility
                ``m`` and the initial time ``t0``.
        """
        self.m = parameters.m
        self.t0 = parameters.t0

    def phi(
        self, x: ArrayOrFloat, y: ArrayOrFloat, t: ArrayOrFloat
    ) -> ArrayOrFloat:
        """Evaluate the order parameter phi(x, y, t)."""
        return cast(
            ArrayOrFloat,
            np.exp(-np.pi**4 * t)
            * np.cos(2 * np.pi * x)
            * np.cos(2 * np.pi * y),
        )

    def phi0(self, x: npt.NDArray[np.floating]) -> npt.NDArray[np.floating]:
        return cast(npt.NDArray[np.floating], self.phi(x[0], x[1], self.t0))
