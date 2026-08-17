from ...core.parameters import ParametersBase


class ParametersBiharmonic(ParametersBase):
    """Parameters for the biharmonic equation solver.

    Adds the mobility parameter `m` to the common `ParametersBase` fields.
    """

    def __init__(
        self,
        nx: int = 16,
        ny: int = 16,
        finite_element_degree: int = 1,
        num_time_steps: int = 100,
        T: float = 1,
        t0: float = 0,
        m: float = 1,
        tol: float = 1e-8,
        max_iter: int = 50,
    ) -> None:
        """Initialize the biharmonic equation parameters.

        Args:
            nx: Number of mesh cells in the x-direction.
            ny: Number of mesh cells in the y-direction.
            finite_element_degree: Polynomial degree of the finite element space.
            num_time_steps: Number of time steps to take between ``t0`` and ``T``.
            T: Final simulation time.
            t0: Initial simulation time.
            m: mobility parameter.
            tol: Nonlinear solver step-length tolerance (``snes_stol``).
            max_iter: Maximum number of nonlinear solver iterations (``snes_max_it``).
        """
        super().__init__(
            nx=nx,
            ny=ny,
            finite_element_degree=finite_element_degree,
            num_time_steps=num_time_steps,
            T=T,
            t0=t0,
            tol=tol,
            max_iter=max_iter,
        )
        self.m = m
