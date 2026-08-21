from typing import Any, Dict

from petsc4py import PETSc


class Parameters:
    """Common simulation parameters shared by all problems: mesh, time stepping
    and the nonlinear solver.

    Attributes:
        nx: Number of mesh cells in the x-direction.
        ny: Number of mesh cells in the y-direction.
        finite_element_degree: Polynomial degree of the finite element space.
        num_time_steps: Number of time steps to take between ``t0`` and ``T``.
        T: Final simulation time.
        t0: Initial simulation time.
        dt: Time step size, computed as ``(T - t0) / num_time_steps``.
        tol: Nonlinear solver step-length tolerance (``snes_stol``).
        max_iter: Maximum number of nonlinear solver iterations (``snes_max_it``).
        petsc_options: PETSc SNES/KSP options, picking the best available direct solver.
    """

    def __init__(
        self,
        nx: int = 16,
        ny: int = 16,
        finite_element_degree: int = 1,
        num_time_steps: int = 100,
        T: float = 1,
        t0: float = 0,
        tol: float = 1e-8,
        max_iter: int = 50,
    ) -> None:
        """Initialize the common simulation parameters.

        Args:
            nx: Number of mesh cells in the x-direction.
            ny: Number of mesh cells in the y-direction.
            finite_element_degree: Polynomial degree of the finite element space.
            num_time_steps: Number of time steps to take between ``t0`` and ``T``.
            T: Final simulation time.
            t0: Initial simulation time.
            tol: Nonlinear solver step-length tolerance (``snes_stol``).
            max_iter: Maximum number of nonlinear solver iterations (``snes_max_it``).
        """
        self.nx, self.ny = nx, ny
        self.finite_element_degree = finite_element_degree
        self.num_time_steps = num_time_steps
        self.T = T
        self.t0 = t0
        self.dt = (T - t0) / num_time_steps
        self.tol = tol
        self.max_iter = max_iter
        self.petsc_prefix = "base_prefix_"
        self.petsc_options: Dict[str, Any] = self._build_petsc_options()

    def _build_petsc_options(self) -> Dict[str, Any]:
        """Pick the best available direct solver and assemble the SNES/KSP options."""
        sys = PETSc.Sys()  # type: ignore
        if sys.hasExternalPackage("superlu_dist"):
            linear_solver = "superlu_dist"
        elif sys.hasExternalPackage("mumps"):
            linear_solver = "mumps"
        else:
            linear_solver = "petsc"
        return {
            "snes_type": "newtonls",
            "snes_linesearch_type": "none",
            "snes_stol": self.tol,
            "snes_atol": 0,
            "snes_rtol": 0,
            "snes_max_it": self.max_iter,
            "ksp_type": "preonly",
            "pc_type": "lu",
            "pc_factor_mat_solver_type": linear_solver,
        }
