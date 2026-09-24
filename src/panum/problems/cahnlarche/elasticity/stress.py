from dolfinx.fem import Function

from ufl import indices, as_tensor

from .stiffness_tensor import StiffnessTensor


class Stress:

    def __call__(
        self, stiffness_tensor, strain: Function, pf: Function
    ) -> Function:
        """
        Evaluate the heterogeneous and anisotropic stiffness tensor.

        Args:
            strain (df.Function): Strain
            pf (df.Function): Phasefield

        Returns:
            df.Function: Heterogeneous and anisotropic stiffness
                tensor
        """
        i, j, k, m = indices(4)
        return as_tensor(
            stiffness_tensor(pf, i, j, k, m) * strain[k, m],
            (i, j),
        )
