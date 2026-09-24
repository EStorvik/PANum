from typing import Optional, Any

from ..cahnhilliard.doublewell import DoubleWell
from  panum import DifferentialEquation
from .parameters import ParametersCahnLarche
from .elasticity.stiffness_tensor import StiffnessTensor
from .elasticity.stress import Stress
from .elasticity.swelling import Swelling
from ufl import inner, grad, sym, Identity


class DifferentialEquationCahnLarche(DifferentialEquation):
    """
    The differential equation for the Biharmonic equation.

    NOTE: There is still some missing functionality for evaluating sources at discrete times.
    """

    def __init__(
        self,
        doublewell: DoubleWell,
        parameters: ParametersCahnLarche,
        stiffness_tensor: StiffnessTensor = StiffnessTensor(),
        source: Optional[Any] = None,
        imex: Optional[str] = None,
    ):
        self.G = {0: self._G}
        self.imex = imex
        if self.imex is not None:
            self.H = {0: self._H_mu_imex, 1: self._H_bu_imex}
        else:
            self.H = {0: self._H_mu, 1: self._H_bu}
        self.source = source
        self.doublewell = doublewell
        self.parameters = parameters
        self.stress = Stress()
        self.stiffness_tensor = stiffness_tensor
        self.swelling = Swelling(self.parameters)

    def _G(self, us, vs, eta):
        mu = vs[0]
        G = -self.parameters.m * inner(grad(mu), grad(eta))
        if self.source is not None:
            G += inner(self.source, eta)
        return G

    def _H_mu(self, us, vs, eta):
        pf = us[0]
        mu = vs[0]
        u = vs[1]
        return (
            inner(mu, eta)
            - self.parameters.gamma
            * (
                self.parameters.ell * inner(grad(pf), grad(eta))
                - (1 / self.parameters.ell)
                * inner(self.doublewell.prime(pf), eta)
            )
            - 0.5
            * inner(inner(
                sym(grad(u)) - self.swelling(pf),
                self.stress(
                    stiffness_tensor=self.stiffness_tensor.prime,
                    strain=sym(grad(u)) - self.swelling(pf),
                    pf=pf,
                ),
            ), eta)
            + inner(inner(
                self.parameters.swelling_parameter * Identity(2),
                self.stress(
                    stiffness_tensor=self.stiffness_tensor,
                    strain=sym(grad(u)) - self.swelling(pf),
                    pf=pf,
                ),
            ), eta)
        )

    # NOTE: Not working atm
    def _H_mu_imex(self, us, us_old, vs, vs_old, eta):
        pf = us[0]
        pf_old = us_old[0]
        mu = vs[0]
        u = vs[1]
        u_old = vs_old[1]
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
                - 0.5
                * inner(inner(
                    sym(grad(u_old)) - self.swelling(pf_old),
                    self.stress(
                        stiffness_tensor=self.stiffness_tensor.prime,
                        strain=sym(grad(u_old)) - self.swelling(pf_old),
                        pf=pf_old,
                    ),
                ), eta)
                + inner(inner(
                    self.parameters.swelling_parameter * Identity(2),
                    self.stress(
                        stiffness_tensor=self.stiffness_tensor,
                        strain=sym(grad(u)) - self.swelling(pf),
                        pf=pf_old,
                    ),
                ), eta)
            )

    def _H_bu(self, us, vs, eta):
        pf = us[0]
        u = vs[1]
        return inner(
            self.stress(
                stiffness_tensor=self.stiffness_tensor,
                strain=sym(grad(u)) - self.swelling(pf),
                pf=pf,
            ),
            sym(grad(eta)),
        )

    def _H_bu_imex(self, us, us_old, vs, vs_old, eta):
        pf = us[0]
        pf_old = us_old[0]
        u = vs[1]
        return inner(
            self.stress(
                stiffness_tensor=self.stiffness_tensor,
                strain=sym(grad(u)) - self.swelling(pf),
                pf=pf_old,
            ),
            sym(grad(eta)),
        )
