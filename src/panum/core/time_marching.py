from typing import Any, Callable, List, Optional

from .time_discretization import TimeIntegrator

# Called after each time step as callback(step, time_integrator, femhandler).
Callback = Callable[[int, TimeIntegrator, Any], None]


class TimeMarching:
    """Drives the time loop for a `TimeIntegrator`.

    Owns the time loop itself; storing/plotting of intermediate results is
    left to the caller via `callbacks`, which are invoked once before the
    loop (`step=0`, for the initial condition) and once after every time
    step.
    """

    def __init__(
        self,
        time_integrator: TimeIntegrator,
        femhandler: Any,
        parameters: Any,
        callbacks: Optional[List[Callback]] = None,
    ) -> None:
        """Initialize the time marching driver.

        Args:
            time_integrator: Scheme-specific `TimeIntegrator` to advance each step.
            femhandler: Finite element handler holding the current solution,
                passed through to `callbacks` for storing/plotting.
            parameters: Simulation parameters (uses `num_time_steps`).
            callbacks: Optional callables invoked as
                `callback(step, time_integrator, femhandler)` after each step
                (and once with `step=0` before the loop starts), e.g. to plot
                or write the solution to disk.
        """
        self.time_integrator = time_integrator
        self.femhandler = femhandler
        self.parameters = parameters
        self.callbacks = list(callbacks) if callbacks is not None else []

    def __call__(self) -> None:
        """Run the time loop from `t0` to `T`, invoking the callbacks at each step."""
        self._run_callbacks(step=0)

        for step in range(1, self.parameters.num_time_steps + 1):
            self.time_integrator.step()
            self._run_callbacks(step=step)

    def _run_callbacks(self, step: int) -> None:
        for callback in self.callbacks:
            callback(step, self.time_integrator, self.femhandler)
