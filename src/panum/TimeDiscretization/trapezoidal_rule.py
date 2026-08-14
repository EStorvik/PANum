
from typing import Optional

import ufl
from dolfinx.fem.petsc import NonlinearProblem
from ufl import Form, dx, inner, grad

from ..FEMHandler import FEMHandlerBiharmonic
from ..ManufacturedSolutions import ManufacturedSolutionBiharmonic
from ..Parameters import ParametersBiharmonic
from .time_integrator import TimeIntegrator


class TrapezoidalRuleBiharmonic(TimeIntegrator):
    """Trapezoidal-rule (Crank-Nicolson) time discretization of the biharmonic system.

    Builds the mixed variational form for ``phi`` and ``mu``:

        (phi - phi_old) / dt * eta_pf * dx + m * grad((mu + mu_old) / 2) . grad(eta_pf) * dx
            = (f(t) + f(t_old)) / 2 * eta_pf * dx      (only if a manufactured solution is given)

        mu * eta_mu * dx - grad(phi) . grad(eta_mu) * dx = 0

    The time levels `t` and `t_old` are stored as `dolfinx.fem.Constant`, so
    `advance_time()` can update them between time steps without recompiling
    the form.
    """

    def __init__(
        self,
        femhandler: FEMHandlerBiharmonic,
        parameters: ParametersBiharmonic,
        manuf: Optional[ManufacturedSolutionBiharmonic] = None,
    ) -> None:
        """Initialize variational forms.

        Args:
            femhandler: Finite element handler with spaces and functions.
            parameters: Simulation parameters (dt, mobility ``m``, ``t0``).
            manuf: Manufactured solution used for the forcing term ``f``, if
                verifying the discretization against a manufactured solution.
                If `None`, no forcing term is added.
        """
        super().__init__(femhandler.V.mesh, parameters)

        self.femhandler = femhandler
        self.pf = femhandler.pf
        self.mu = femhandler.mu
        self.pf_old = femhandler.pf_old
        self.mu_old = femhandler.mu_old
        self.eta_pf = femhandler.eta_pf
        self.eta_mu = femhandler.eta_mu
        self.manuf = manuf

        msh = femhandler.V.mesh
        if manuf is not None:
            x = ufl.SpatialCoordinate(msh)
            self.f_n = manuf.f_ufl(x[0], x[1], self.t)
            self.f_n_old = manuf.f_ufl(x[0], x[1], self.t_old)

        # Build forms on initialization
        self._build_forms()
        self.problem: NonlinearProblem = NonlinearProblem(
            self.F,
            femhandler.xi,
            petsc_options_prefix="biharmonic_trapezoidal_rule_",
            petsc_options=parameters.petsc_options,
        )


    def solve_time_step(self) -> None:
        """Solve the nonlinear problem for `xi` and copy it into `xi_old` for the next step."""
        self.problem.solve()
        self.femhandler.xi_old.x.array[:] = self.femhandler.xi.x.array
        self.femhandler.xi_old.x.scatter_forward()

    def _build_forms(self) -> None:
        """Build all variational forms."""
        self.F_pf: Form = self._build_F_pf()
        self.F_mu: Form = self._build_F_mu()
        self.F: Form = self.F_pf + self.F_mu

    def _build_F_pf(self) -> Form:
        F_pf = (
            inner(self.pf - self.pf_old, self.eta_pf) / self.parameters.dt * dx
            + self.parameters.m * inner(grad((self.mu + self.mu_old) / 2), grad(self.eta_pf)) * dx
        )
        if self.manuf is not None:
            F_pf -= inner((self.f_n + self.f_n_old) / 2, self.eta_pf) * dx
        return F_pf

    def _build_F_mu(self) -> Form:
        return inner(self.mu, self.eta_mu) * dx - inner(grad(self.pf), grad(self.eta_mu)) * dx

