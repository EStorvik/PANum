
class ParametersBiharmonic:
    """Parameters for the biharmonic equation solver.

    Attributes:
        nx: Number of mesh cells in the x-direction.
        ny: Number of mesh cells in the y-direction.
        num_time_steps: Number of time steps to take between ``t0`` and ``T``.
        T: Final simulation time.
        t0: Initial simulation time.
        dt: Time step size, computed as ``(T - t0) / num_time_steps``.
        m: mobility parameter.
    """

    def __init__(
        self,
        nx: int = 16,
        ny: int = 16,
        num_time_steps: int = 100,
        T: float = 1,
        t0: float = 0,
        m: float = 1,
    ) -> None:
        """Initialize the biharmonic equation parameters.

        Args:
            nx: Number of mesh cells in the x-direction.
            ny: Number of mesh cells in the y-direction.
            num_time_steps: Number of time steps to take between ``t0`` and ``T``.
            T: Final simulation time.
            t0: Initial simulation time.
            m: mobility parameter.
        """
        self.nx, self.ny = nx, ny
        self.num_time_steps = num_time_steps
        self.T = T
        self.t0 = t0
        self.dt = (T - t0) / num_time_steps
        self.m = m