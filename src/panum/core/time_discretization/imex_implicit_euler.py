from ufl import dx, inner
from typing import Optional, Any
from dolfinx.mesh import Mesh
from .base import TimeDiscretization
from ..differential_equation import DifferentialEquation
from ..parameters import Parameters
from ..femhandler import FEMHandler


class IMEXImplicitEuler(TimeDiscretization):

    def __init__(
        self,
        msh: Mesh,
        parameters: Parameters,
        femhandler: FEMHandler,
        diff_eq: DifferentialEquation,
        callbacks: Optional[Any] = None,
    ):
        super().__init__(
            msh, parameters, femhandler, diff_eq, callbacks=callbacks
        )
        assert (
            self.diff_eq.imex is not None
        ), "No IMEX method is implemented in the current choice of differential equation"

    def _build_variational_form(self):
        us = self.femhandler.us
        us_old = self.femhandler.us_old
        eta_us = self.femhandler.eta_us
        eta_vs = self.femhandler.eta_vs
        vs = self.femhandler.vs
        vs_old = self.femhandler.vs_old
        dt = self.parameters.dt

        self.F = 0
        for i, u in us.items():
            u_old = us_old[i]
            eta = eta_us[i]
            G = self.diff_eq.G[i]
            self.F += (inner(u - u_old, eta) - dt * G(us, vs, eta)) * dx

        for i in vs:
            eta = eta_vs[i]
            H = self.diff_eq.H[i]
            self.F += H(us, us_old, vs, vs_old, eta) * dx

    def solve_time_step(self):
        self.problem.solve()
        self.femhandler.copy_to_old()
