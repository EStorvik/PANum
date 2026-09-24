from dolfinx.fem import Function
from ufl import Identity

"""Swelling term"""


class Swelling:
    """Swelling term"""

    def __init__(
        self,
        parameters,
    ) -> None:
        """Initialize the swelling term

        Args:
            swelling_parameter (float): Swelling parameter. Defaults to 0.
            dim (int, optional): Dimension. Defaults to 2.

        Attributes:
            swelling_parameter (float): Swelling parameter.
            dim (int): Dimension.
        """
        self.swelling_parameter = parameters.swelling_parameter
        self.pf_ref = parameters.pf_ref
        self.dim = 2

    def __call__(self, pf: Function) -> Function:
        """Evaluate the swelling term

        Args:
            pf (df.Function): Phasefield

        Returns:
            df.Function: Swelling term
        """
        return (
            self.swelling_parameter * (pf - self.pf_ref) * Identity(self.dim)
        )

    def prime(self):
        """Evaluate the derivative of the swelling term

        Returns:
            df.Function: Derivative of the swelling term
        """
        return self.swelling_parameter * Identity(self.dim)
