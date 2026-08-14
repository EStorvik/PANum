

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from dolfinx import default_scalar_type, fem

if TYPE_CHECKING:
    from dolfinx.mesh import Mesh


class TimeIntegrator(ABC):
    """Base class for time discretizations of a variational problem.

    Handles the bookkeeping shared by every time-stepping scheme: the
    current and previous time levels, and advancing them by `dt`.
    Subclasses build the scheme-specific variational form(s) and implement
    `solve_time_step()` to solve the resulting problem for the current step
    and update the stored "old" solution used by the next step.
    """

    def __init__(self, msh: "Mesh", parameters: Any) -> None:
        """Initialize the time levels.

        Args:
            msh: The computational mesh, used to create the time `fem.Constant`s.
            parameters: Simulation parameters (uses `t0` and `dt`).
        """
        self.parameters = parameters
        self.t = fem.Constant(msh, default_scalar_type(parameters.t0))
        self.t_old = fem.Constant(msh, default_scalar_type(parameters.t0))

    def advance_time(self) -> None:
        """Advance the stored time levels by one step: ``t_old <- t``, ``t <- t + dt``."""
        self.t_old.value = self.t.value
        self.t.value = self.t.value + self.parameters.dt

    @abstractmethod
    def solve_time_step(self) -> None:
        """Solve the variational problem for the current time step and update the old solution."""
        ...

    def step(self) -> None:
        """Solve the current time step and advance the time levels for the next one."""
        self.solve_time_step()
        self.advance_time()