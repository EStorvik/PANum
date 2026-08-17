from typing import cast, Optional

from dolfinx.fem.petsc import NonlinearProblem
from ufl import Form, dx

from panum.core.time_discretization import TimeIntegrator

from ..femhandler import FEMHandlerBiharmonic
from ..manufactured_solution import ManufacturedSolutionBiharmonic
from ..parameters import ParametersBiharmonic
from ..weak_form import BiharmonicWeakForm


class TrapezoidalRuleBiharmonic(TimeIntegrator):
    """Trapezoidal-rule (Crank-Nicolson) time discretization of the biharmonic system.

    Averages the scheme-agnostic `BiharmonicWeakForm` flux/forcing term
    between the old and new time levels:

        (phi - phi_old) / dt * eta_pf * dx + (flux(t) + flux(t_old)) / 2
            = 0

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
        self.weak_form = BiharmonicWeakForm(
            femhandler.V.mesh, parameters.m, manuf
        )

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
        fh = self.femhandler
        wf = self.weak_form
        integrand = (
            wf.mass_form(fh.pf, fh.eta_pf) - wf.mass_form(fh.pf_old, fh.eta_pf)
        ) / self.parameters.dt
        integrand += (
            wf.flux_form(fh.mu, fh.eta_pf, self.t)
            + wf.flux_form(fh.mu_old, fh.eta_pf, self.t_old)
        ) / 2
        return cast(Form, integrand * dx)

    def _build_F_mu(self) -> Form:
        fh = self.femhandler
        return cast(Form, self.weak_form.mu_form(fh.pf, fh.mu, fh.eta_mu) * dx)
