from ufl import dx, inner
from typing import Optional, Any
from dolfinx.mesh import Mesh
from .base import TimeDiscretization
from ..differential_equation import DifferentialEquation
from ..parameters import Parameters
from ..femhandler import FEMHandler


class ThetaMethod(TimeDiscretization):

    def __init__(
        self,
        msh: Mesh,
        parameters: Parameters,
        femhandler: FEMHandler,
        diff_eq: DifferentialEquation,
        callbacks: Optional[Any] = None,
        theta: float = 0.5,
    ):

        self.theta = theta
        super().__init__(
            msh,
            parameters,
            femhandler,
            diff_eq,
            callbacks=callbacks,
        )

    def _build_variational_form(self):
        us = self.femhandler.us
        vs = self.femhandler.vs
        us_old = self.femhandler.us_old
        vs_old = self.femhandler.vs_old
        dt = self.parameters.dt

        self.F = 0
        for i, u in us.items():
            eta = self.femhandler.eta_us[i]
            G = self.diff_eq.G[i]
            self.F += (
                inner(u - us_old[i], eta)
                - dt
                * (
                    self.theta * G(us, vs, eta)
                    + (1.0 - self.theta) * G(us_old, vs_old, eta)
                )
            ) * dx

        for i in vs:
            eta = self.femhandler.eta_vs[i]
            H = self.diff_eq.H[i]
            self.F += H(us, vs, eta) * dx

    def solve_time_step(self):
        self.problem.solve()
        self.femhandler.copy_to_old()
