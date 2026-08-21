from typing import Optional, Any

from panum import DifferentialEquation
from ufl import inner, grad


class DifferentialEquationBiharmonic(DifferentialEquation):
    """
    The differential equation for the Biharmonic equation.

    NOTE: There is still some missing functionality for evaluating sources at discrete times.
    """

    def __init__(self, source: Optional[Any] = None):
        self.G = {0: self._G}
        self.H = {0: self._H}
        self.source = source

    def _G(self, pfs, mus, eta):
        mu = mus[0]
        G = -inner(grad(mu), grad(eta))
        if self.source is not None:
            G += inner(self.source, eta)
        return G

    def _H(self, pfs, mus, eta):
        pf = pfs[0]
        mu = mus[0]
        return inner(mu, eta) - inner(grad(pf), grad(eta))
