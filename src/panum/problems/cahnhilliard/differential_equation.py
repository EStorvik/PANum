from typing import Optional, Any

from panum import DifferentialEquation
from .doublewell import DoubleWell
from .parameters import ParametersCahnHilliard
from ufl import inner, grad


class DifferentialEquationCahnHilliard(DifferentialEquation):
    """
    The differential equation for the Biharmonic equation.

    NOTE: There is still some missing functionality for evaluating sources at discrete times.
    """

    def __init__(
        self,
        doublewell: DoubleWell,
        parameters: ParametersCahnHilliard,
        source: Optional[Any] = None,
        imex: Optional[str] = None,
    ):
        self.G = {0: self._G}
        self.imex = imex
        if self.imex is not None:
            self.H = {0: self._H_imex}
        else:
            self.H = {0: self._H}
        self.source = source
        self.doublewell = doublewell
        self.parameters = parameters

    def _G(self, us, vs, eta):
        mu = vs[0]
        G = -self.parameters.m * inner(grad(mu), grad(eta))
        if self.source is not None:
            G += inner(self.source, eta)
        return G

    def _H(self, us, vs, eta):
        pf = us[0]
        mu = vs[0]
        return (
            inner(mu, eta)
            - self.parameters.ell * inner(grad(pf), grad(eta))
            - (1 / self.parameters.ell) * inner(self.doublewell.prime(pf), eta)
        )

    def _H_imex(self, us, us_old, vs, eta):
        pf = us[0]
        pf_old = us_old[0]
        mu = vs[0]
        if self.imex == "Eyre":
            return (
                inner(mu, eta)
                - self.parameters.ell * inner(grad(pf), grad(eta))
                - (1 / self.parameters.ell)
                * inner(
                    self.doublewell.cprime(pf)
                    - self.doublewell.eprime(pf_old),
                    eta,
                )
            )
