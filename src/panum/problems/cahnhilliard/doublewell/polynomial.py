from . import DoubleWell


class DoubleWellPolynomial(DoubleWell):

    def __call__(self, pf):
        return pf**2 * (1 - pf) ** 2

    def prime(self, pf):
        return 2 * pf * (1 - pf) ** 2 - pf**2 * (2 * (1 - pf))

    def c(self, pf):
        return (pf - 0.5) ** 4 + 0.0625

    def cprime(self, pf):
        return 4 * (pf - 0.5) ** 3

    def e(self, pf):
        return 0.5 * (pf - 0.5) ** 2

    def eprime(self, pf):
        return pf - 0.5
