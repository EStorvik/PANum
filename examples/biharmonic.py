# Fix MPI/OFI finalization errors on macOS
import os

os.environ["FI_PROVIDER"] = "tcp"
os.environ["MPICH_OFI_STARTUP_CONNECT"] = "0"

from dolfinx import mesh  # noqa: E402
from dolfinx.mesh import Mesh  # noqa: E402

from mpi4py import MPI  # noqa: E402
import panum as pn  # noqa: E402


parameters = pn.ParametersBiharmonic(T=2e-4, num_time_steps=20)

diff_eq = pn.DifferentialEquationBiharmonic()

msh: Mesh = mesh.create_unit_square(
    MPI.COMM_WORLD,
    parameters.nx,
    parameters.ny,
    cell_type=mesh.CellType.triangle,
)

analyticalsol = pn.AnalyticalSolutionBiharmonic(parameters)

femhandler = pn.FEMHandlerBiharmonic(
    msh, parameters=parameters, initialcondition=analyticalsol.phi0
)

callbacks = []
# Optional live plot of the phase field (requires pyvista/pyvistaqt).
plot_solution = True
if plot_solution:
    plot_callback = pn.PyvistaPlotCallback(
        femhandler, parameters, component=0, name="phi"
    )
    callbacks.append(plot_callback)

timediscretization = pn.ImplicitEuler(
    msh, parameters, femhandler, diff_eq, callbacks
)

timediscretization()

print(analyticalsol.L2_error(femhandler, parameters.T))
