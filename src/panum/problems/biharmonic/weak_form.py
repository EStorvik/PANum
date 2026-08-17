from typing import cast, Optional, TYPE_CHECKING

import ufl
from ufl import grad, inner
from ufl.core.expr import Expr as UFLExpr

from .manufactured_solution import ManufacturedSolutionBiharmonic


if TYPE_CHECKING:
    from dolfinx.mesh import Mesh


class BiharmonicWeakForm:
    """Scheme-agnostic UFL building blocks for the biharmonic (Cahn-Hilliard-type) system.

    Time discretizations (e.g. `TrapezoidalRuleBiharmonic`) combine these
    forms across time levels/stages with their own coefficients; none of the
    forms here reference `dt` or an "old" state.
    """

    def __init__(
        self,
        msh: "Mesh",
        m: float,
        manuf: Optional[ManufacturedSolutionBiharmonic] = None,
    ) -> None:
        """Initialize the weak form builder.

        Args:
            msh: The computational mesh, used to evaluate the manufactured forcing term.
            m: mobility parameter.
            manuf: Manufactured solution used for the forcing term ``f``, if
                verifying the discretization against a manufactured solution.
                If `None`, no forcing term is added.
        """
        self.m = m
        self.manuf = manuf
        if manuf is not None:
            x = ufl.SpatialCoordinate(msh)
            self.x, self.y = x[0], x[1]

    def mass_form(self, pf: UFLExpr, eta_pf: UFLExpr) -> UFLExpr:
        """The phase-field mass integrand ``inner(pf, eta_pf)`` (unintegrated)."""
        return cast(UFLExpr, inner(pf, eta_pf))

    def flux_form(
        self, mu: UFLExpr, eta_pf: UFLExpr, t: Optional[UFLExpr] = None
    ) -> UFLExpr:
        """The phase-field flux/forcing integrand at a single time level ``t`` (unintegrated).

        ``m * inner(grad(mu), grad(eta_pf))``, minus the manufactured forcing
        ``f(t)`` if a manufactured solution was given.
        """
        F = self.m * inner(grad(mu), grad(eta_pf))
        if self.manuf is not None:
            if t is None:
                raise ValueError(
                    "t is required to evaluate the manufactured forcing term."
                )
            F -= inner(self.manuf.f_ufl(self.x, self.y, t), eta_pf)
        return cast(UFLExpr, F)

    def mu_form(self, pf: UFLExpr, mu: UFLExpr, eta_mu: UFLExpr) -> UFLExpr:
        """The chemical-potential constraint integrand, the same at every
        time level/stage (unintegrated)."""
        return cast(UFLExpr, inner(mu, eta_mu) - inner(grad(pf), grad(eta_mu)))
