from typing import Union

import numpy as np
import numpy.typing as npt

from ..Parameters import ParametersBiharmonic

ArrayOrFloat = Union[float, npt.NDArray[np.floating]]


class ManufacturedSolutionBiharmonic:
    """Manufactured solution for the biharmonic (Cahn-Hilliard-type) equation on the unit square.

    The solution is built around ``phi(x, y, t) = t * cos(2*pi*x) * cos(2*pi*y)``,
    with ``mu = -Delta phi`` and the right-hand side ``f`` chosen so that
    ``partial_t phi + m * Delta^2 phi = f``. Because ``cos(2*pi*x)`` and
    ``cos(2*pi*y)`` have zero derivative at ``x, y in {0, 1}``, both
    ``grad(phi) . n`` and ``grad(mu) . n`` vanish on the boundary of the unit
    square, matching homogeneous Neumann boundary conditions.
    """

    def __init__(self, parameters: ParametersBiharmonic) -> None:
        """Initialize the manufactured solution.

        Args:
            parameters: Biharmonic equation parameters, used for the mobility
                ``m`` and the initial time ``t0``.
        """
        self.m = parameters.m
        self.t0 = parameters.t0

    def phi(self, x: ArrayOrFloat, y: ArrayOrFloat, t: ArrayOrFloat) -> ArrayOrFloat:
        """Evaluate the order parameter phi(x, y, t)."""
        return t * np.cos(2 * np.pi * x) * np.cos(2 * np.pi * y)

    def phi0(self, x: npt.NDArray[np.floating]) -> npt.NDArray[np.floating]:
        """Initial phase field phi(x, y, t0), callable for FEniCSx/UFL interpolation.

        Matches the signature expected by ``dolfinx.fem.Function.interpolate``:
        a callable taking the point coordinates ``x`` with shape
        ``(gdim, num_points)`` and returning the corresponding values.

        Args:
            x: Point coordinates, with ``x[0]`` and ``x[1]`` the x- and
                y-components respectively.

        Returns:
            The values of ``phi`` at ``t = t0``, with shape ``(num_points,)``.
        """
        return self.phi(x[0], x[1], self.t0)

    def mu(self, x: ArrayOrFloat, y: ArrayOrFloat, t: ArrayOrFloat) -> ArrayOrFloat:
        """Evaluate the chemical potential mu(x, y, t) = -Delta phi(x, y, t)."""
        return t * 2 * (2 * np.pi) ** 2 * (np.cos(2 * np.pi * x) * np.cos(2 * np.pi * y))

    def f(self, x: ArrayOrFloat, y: ArrayOrFloat, t: ArrayOrFloat) -> ArrayOrFloat:
        """Evaluate the source term f = partial_t phi + m * Delta^2 phi."""
        return np.cos(2 * np.pi * x) * np.cos(2 * np.pi * y) + self.m * t * 4 * (2 * np.pi) ** 4 * (
            np.cos(2 * np.pi * x) * np.cos(2 * np.pi * y)
        )

