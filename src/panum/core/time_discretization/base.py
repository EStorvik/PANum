from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional

from dolfinx import default_scalar_type, fem
from ..femhandler import FEMHandler
from ..differential_equation import DifferentialEquation

from dolfinx.fem.petsc import NonlinearProblem

if TYPE_CHECKING:
    from dolfinx.mesh import Mesh


class TimeDiscretization(ABC):
    """Base class for time discretizations of a variational problem.

    Handles the bookkeeping shared by every time-stepping scheme: the
    current and previous time levels, and advancing them by `dt`.
    Subclasses build the scheme-specific variational form(s) and implement
    `solve_time_step()` to solve the resulting problem for the current step
    and update the stored "old" solution used by the next step.
    """

    def __init__(
        self,
        msh: "Mesh",
        parameters: Any,
        femhandler: FEMHandler,
        diff_eq: DifferentialEquation,
        callbacks: Optional[Any] = None,
    ) -> None:
        """Initialize the time levels.

        Args:
            msh: The computational mesh, used to create the time `fem.Constant`s.
            parameters: Simulation parameters (uses `t0` and `dt`).
        """
        self.parameters = parameters
        self.t = fem.Constant(msh, default_scalar_type(parameters.t0))
        self.t_old = fem.Constant(msh, default_scalar_type(parameters.t0))
        self.diff_eq = diff_eq
        self.femhandler = femhandler
        self._build_variational_form()
        self.problem: NonlinearProblem = NonlinearProblem(
            self.F,
            femhandler.xi,
            petsc_options_prefix=parameters.petsc_prefix,
            petsc_options=parameters.petsc_options,
        )
        self.callbacks = list(callbacks) if callbacks is not None else []

    def advance_time(self) -> None:
        """Advance the stored time levels by one step: ``t_old <- t``, ``t <- t + dt``."""
        self.t_old.value = self.t.value
        self.t.value = self.t.value + self.parameters.dt

    @abstractmethod
    def _build_variational_form(self) -> None:
        """Builds variational forms for specific time discretization"""
        ...

    @abstractmethod
    def solve_time_step(self) -> None:
        """Solve the variational problem for the current time step and update the old solution."""
        ...

    def step(self) -> None:
        """Advance the time levels for the current step, then solve it."""
        self.advance_time()
        self.solve_time_step()

    def __call__(self) -> None:
        for step in range(self.parameters.num_time_steps):
            self.step()
            self._run_callbacks(step=step)

    def _run_callbacks(self, step: int) -> None:
        for callback in self.callbacks:
            callback(step, self.t.value, self.femhandler)
