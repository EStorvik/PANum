
from petsc4py import PETSc
from typing import Dict, Any

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
        finite_element_degree: int =1,
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
            num_time_steps: Number of time steps to take between ``t0`` and ``T``.
            T: Final simulation time.
            t0: Initial simulation time.
            m: mobility parameter.
            tol: Nonlinear solver step-length tolerance (``snes_stol``).
            max_iter: Maximum number of nonlinear solver iterations (``snes_max_it``).
        """
        self.nx, self.ny = nx, ny
        self.finite_element_degree = finite_element_degree
        self.num_time_steps = num_time_steps
        self.T = T
        self.t0 = t0
        self.dt = (T - t0) / num_time_steps
        self.m = m
        self.tol = tol
        self.max_iter = max_iter

                # Determine linear solver based on available PETSc packages
        sys = PETSc.Sys()  # type: ignore
        if sys.hasExternalPackage("superlu_dist"):
            linear_solver = "superlu_dist"
        elif sys.hasExternalPackage("mumps"):
            linear_solver = "mumps"
        else:
            linear_solver = "petsc"
        self.petsc_options: Dict[str, Any] = {
            "snes_type": "newtonls",
            "snes_linesearch_type": "none",
            "snes_stol": self.tol,
            "snes_atol": 0,
            "snes_rtol": 0,
            "snes_max_it": self.max_iter,
            "ksp_type": "preonly",
            "pc_type": "lu",
            "pc_factor_mat_solver_type": linear_solver,
            # "snes_monitor": None,
            # "snes_view": None,
        }