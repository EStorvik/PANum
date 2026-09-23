from typing import TYPE_CHECKING

from basix.ufl import element, mixed_element
from dolfinx.fem import functionspace
from dolfinx.fem.function import FunctionSpace
from ufl import split

from panum import FEMHandler
from .parameters import ParametersCahnHilliard

if TYPE_CHECKING:
    from dolfinx.mesh import Mesh

from .initialconditions import InitialConditionCahnHilliard
from .initialconditions import initialize_cahn_hilliard
from .doublewell import DoubleWell


class FEMHandlerCahnHilliard(FEMHandler):
    """ """

    def __init__(
        self,
        msh: "Mesh",
        parameters: ParametersCahnHilliard,
        initialcondition: InitialConditionCahnHilliard,
        doublewell: DoubleWell,
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

        P = element(
            "Lagrange", msh.basix_cell(), parameters.finite_element_degree
        )
        ME = mixed_element([P, P])

        # Function spaces
        self.V: FunctionSpace = functionspace(msh, ME)
        self.stages = stages

        super().__init__()

        # Initialize phi
        self.initialcondition = initialcondition
        self.xi.sub(0).interpolate(initialcondition)
        self.xi.x.scatter_forward()

        # Initialize mu from phi
        pf0, mu0 = initialize_cahn_hilliard(
            pf0=self.pf, doublewell=doublewell, V=self.V
        )

        self.xi.sub(1).interpolate(mu0)
        self.xi.x.scatter_forward()

        # Copy to old
        self.copy_to_old()

    def define_fields(self) -> None:

        # Test function on mixed space
        self.eta_pf, self.eta_mu = split(self.eta)
        self.eta_us = {0: self.eta_pf}
        self.eta_vs = {0: self.eta_mu}

        # Solution functions
        self.pf, self.mu = split(self.xi)
        self.us = {0: self.pf}
        self.vs = {0: self.mu}

        self.us_stages = []
        self.vs_stages = []
        for xi in self.xi_stages:
            pf, mu = split(xi)
            self.us_stages.append({0: pf})
            self.vs_stages.append({0: mu})

        self.us_old = self.us_stages[0]
        self.vs_old = self.vs_stages[0]
