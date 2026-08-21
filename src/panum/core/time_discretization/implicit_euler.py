from ufl import dx, inner
from typing import Optional, Any
from dolfinx.mesh import Mesh
from .base import TimeDiscretization
from ..differential_equation import DifferentialEquation
from ..parameters import Parameters
from ..femhandler import FEMHandler


class ImplicitEuler(TimeDiscretization):

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

    def _build_variational_form(self):
        pfs = self.femhandler.pfs
        mus = self.femhandler.mus
        dt = self.parameters.dt

        self.F = 0
        for i, pf in pfs.items():
            pf_old = self.femhandler.pfs_old[i]
            eta = self.femhandler.eta_pfs[i]
            G = self.diff_eq.G[i]
            self.F += (inner(pf - pf_old, eta) - dt * G(pfs, mus, eta)) * dx

        for i in mus:
            eta = self.femhandler.eta_mus[i]
            H = self.diff_eq.H[i]
            self.F += H(pfs, mus, eta) * dx

    def solve_time_step(self):
        self.problem.solve()
        self.femhandler.copy_to_old()
