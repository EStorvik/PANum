"""PyVista-based visualization for FEniCSx solutions."""

import pyvista as pv
import pyvistaqt as pvqt
from dolfinx import plot

if pv.OFF_SCREEN:
    pv.start_xvfb(wait=0.5)


class PyvistaVizualization:

    def __init__(self, V, xi, t0, name="phi") -> None:
        """
        Initialize the visualization object.

        Args:
            V (FunctionSpace): Function space. Provide the function
                space of the solution that you want to plot. F.ex. use
                .subs(0) to get the function space of the first
                component of the solution.
            xi (Function): The solution to visualize
            t0 (float): The initial time
            name (str): The name of the scalar field to plot
        """
        self.V0, self.dofs = V.collapse()
        self.name = name

        # Create a VTK 'mesh' with 'nodes' at the function dofs
        self.topology, self.cell_types, self.x = plot.vtk_mesh(self.V0)
        self.grid = pv.UnstructuredGrid(self.topology, self.cell_types, self.x)

        # Set output data
        self.grid.point_data[name] = xi.x.array[self.dofs].real
        self.grid.set_active_scalars(name)
        self.p = pvqt.BackgroundPlotter(title=self.name, auto_update=True)
        self.p.add_mesh(self.grid, clim=[0, 1])
        self.p.view_xy(negative=True)
        self.p.add_text(f"time: {t0}", font_size=12, name="timelabel")

    def update(self, xi, t):
        """
        Update the visualization with the new solution xi at time t.

        Args:
            xi (Function): The new solution
            t (float): The new time
        """
        self.p.add_text(f"time: {t:.2e}", font_size=12, name="timelabel")
        self.grid.point_data[self.name] = xi.x.array[self.dofs].real
        self.p.app.processEvents()

    # Update ghost entries and plot
    def final_plot(self, xi):
        """
        Update the visualization with the final solution.

        Args:
            xi (Function): The final solution
        """

        xi.x.scatter_forward()
        self.grid.point_data[self.name] = xi.x.array[self.dofs].real

        screenshot = None
        if pv.OFF_SCREEN:
            screenshot = self.name + ".png"
        pv.plot(self.grid, show_edges=True, screenshot=screenshot)


class PyvistaPlotCallback:
    """Live-plots a component of the solution with `PyvistaVizualization` after each time step.

    Matches the `callbacks` interface expected by `panum.TimeMarching`:
    call as `callback(step, time_integrator, femhandler)`.
    """

    def __init__(
        self,
        femhandler,
        parameters,
        component: int = 0,
        name: str = "phi",
        every: int = 1,
    ) -> None:
        """Initialize the plot window for the given solution component.

        Args:
            femhandler: Finite element handler holding the mixed function
                space `V` and the solution `xi`.
            parameters: Simulation parameters (uses `t0`).
            component: Index of the component of the mixed space to plot.
            name: Name of the scalar field to plot.
            every: Only update the plot every `every` time steps.
        """
        self.viz = PyvistaVizualization(
            femhandler.V.sub(component),
            femhandler.xi,
            parameters.t0,
            name=name,
        )
        self.every = every

    def __call__(self, step, t, femhandler) -> None:
        """Update the plot with the current solution, skipping non-`every` steps."""
        if step % self.every != 0:
            return
        self.viz.update(femhandler.xi, t)
