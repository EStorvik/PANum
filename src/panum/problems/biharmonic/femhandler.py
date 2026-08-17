from typing import TYPE_CHECKING, Callable

import numpy as np
import numpy.typing as npt
from basix.ufl import element, mixed_element
from dolfinx.fem import Function, functionspace
from dolfinx.fem.function import FunctionSpace
from ufl import Argument, split, TestFunction
from ufl.core.expr import Expr as UFLExpr
import panum as pn

from ...core.femhandler import FEMHandlerBase
from .parameters import ParametersBiharmonic

if TYPE_CHECKING:
    from dolfinx.mesh import Mesh

InitialCondition = Callable[
    [npt.NDArray[np.floating]], npt.NDArray[np.floating]
]


class FEMHandlerBiharmonic(FEMHandlerBase):
    """Finite element handler for the biharmonic (Cahn-Hilliard-type) equation.

    Builds the mixed function space for the phase field ``pf`` and chemical
    potential ``mu``, and initializes the current and previous time-step
    solution vectors from a given initial condition for ``pf``, with ``mu``
    initialized from ``pf`` via :func:`panum.initial_mu_biharmonic`.

    Attributes:
        V: Mixed function space for ``(pf, mu)``.
        eta: Test function on the mixed space.
        eta_pf: Test function component associated with the phase field.
        eta_mu: Test function component associated with the chemical potential.
        xi: Current solution function on the mixed space.
        pf: Phase field component of ``xi``.
        mu: Chemical potential component of ``xi``.
        xi_old: Previous time-step solution function on the mixed space.
        pf_old: Phase field component of ``xi_old``.
        mu_old: Chemical potential component of ``xi_old``.
        initialcondition: Callable used to initialize the phase field.
    """

    def __init__(
        self,
        msh: "Mesh",
        parameters: ParametersBiharmonic,
        initialcondition: InitialCondition,
    ) -> None:
        """Initialize the mixed function space and the initial solution.

        Args:
            msh: The computational mesh.
            parameters: Biharmonic equation parameters (uses ``finite_element_degree``).
            initialcondition: Callable ``x -> values`` used to interpolate the
                initial phase field, as accepted by ``Function.interpolate``.
        """
        P = element(
            "Lagrange", msh.basix_cell(), parameters.finite_element_degree
        )
        ME = mixed_element([P, P])

        # Function spaces
        self.V: FunctionSpace = functionspace(msh, ME)

        # Test function on mixed space
        self.eta: Argument = TestFunction(self.V)
        self.eta_pf: UFLExpr
        self.eta_mu: UFLExpr
        self.eta_pf, self.eta_mu = split(self.eta)

        # Solution functions
        self.xi: Function = Function(self.V)
        self.pf: UFLExpr
        self.mu: UFLExpr
        self.pf, self.mu = split(self.xi)

        self.xi_old: Function = Function(self.V)
        self.pf_old: UFLExpr
        self.mu_old: UFLExpr
        self.pf_old, self.mu_old = split(self.xi_old)

        # Initialize phi
        self.initialcondition = initialcondition
        self.xi.sub(0).interpolate(initialcondition)
        self.xi.x.scatter_forward()

        # Initialize mu from phi
        mu0: UFLExpr = pn.initial_mu_biharmonic(self.pf, P, msh)

        self.xi.sub(1).interpolate(mu0)
        self.xi.x.scatter_forward()

        # Copy to old for time stepping
        self.xi_old.x.array[:] = self.xi.x.array
        self.xi_old.x.scatter_forward()
