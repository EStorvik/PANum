from typing import TYPE_CHECKING

from basix.ufl import element, mixed_element
from dolfinx.fem import functionspace, Function
from dolfinx.fem.function import FunctionSpace
from ufl import split

from panum import FEMHandler
from .parameters import ParametersCahnLarche

if TYPE_CHECKING:
    from dolfinx.mesh import Mesh


from ..cahnhilliard.doublewell import DoubleWell
from ..cahnhilliard.initialconditions import (
    InitialConditionCahnHilliard,
)
from .boundaryconditions.full_zero_dirichlet_u_bc import (
    DirichletZeroFullBoundary,
)


class FEMHandlerCahnLarche(FEMHandler):
    """ """

    def __init__(
        self,
        msh: "Mesh",
        parameters: ParametersCahnLarche,
        initialcondition: InitialConditionCahnHilliard,
        doublewell: DoubleWell,
        boundary_condition=DirichletZeroFullBoundary(),
        stages: int = 1,
    ) -> None:
        """Initialize the mixed function space and the initial solution.

        Args:
            msh: The computational mesh.
            parameters: CahnHilliard equation parameters (uses ``finite_element_degree``).
            initialcondition: Callable ``x -> values`` used to interpolate the
                initial phase field, as accepted by ``Function.interpolate``.
            doublewell:
            stages: stages to be used in multistage method
        """

        P_ch = element(
            "Lagrange", msh.basix_cell(), parameters.finite_element_degree
        )
        P_u = element(
            "Lagrange", msh.basix_cell(), 1, shape=(msh.geometry.dim,)
        )

        ME = mixed_element([P_ch, P_ch, P_u])

        # Function spaces
        self.V: FunctionSpace = functionspace(msh, ME)
        self.stages = stages

        super().__init__()

        # Initialize phi
        self.initialcondition = initialcondition
        self.xi.sub(0).interpolate(initialcondition)
        self.xi.x.scatter_forward()

        # Initialize mu from phi
        # pf0, mu0 = initialize_cahn_hilliard(
        #     pf0=self.pf, doublewell=doublewell, V=self.V
        # )

        # self.xi.sub(1).interpolate(mu0)
        # self.xi.x.scatter_forward()

        # Boundary conditions

        _, _, u_bc = Function(self.V).split()
        self.bcs = boundary_condition(msh, self.V.sub(2), u_bc)

        # Copy to old
        self.copy_to_old()

    def define_fields(self) -> None:

        # Test function on mixed space
        self.eta_pf, self.eta_mu, self.eta_bu = split(self.eta)
        self.eta_us = {0: self.eta_pf}
        self.eta_vs = {
            0: self.eta_mu,
            1: self.eta_bu,
        }

        # Solution functions
        self.pf, self.mu, self.bu = split(self.xi)
        self.us = {0: self.pf}
        self.vs = {
            0: self.mu,
            1: self.bu,
        }

        self.us_stages = []
        self.vs_stages = []
        for xi in self.xi_stages:
            pf, mu, bu = split(xi)
            self.us_stages.append({0: pf})
            self.vs_stages.append({0: mu, 1: bu})

        self.us_old = self.us_stages[0]
        self.vs_old = self.vs_stages[0]
