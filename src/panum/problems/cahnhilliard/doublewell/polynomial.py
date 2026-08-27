from .import DoubleWell

class DoubleWellPolynomial(DoubleWell):


    def __call__(self,pf):
        return pf**2*(1-pf)**2

    def prime(self, pf):
        return 2*pf*(1-pf)**2 - pf**2*(2*(1-pf))