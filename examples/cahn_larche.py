# Fix MPI/OFI finalization errors on macOS
import os

os.environ["FI_PROVIDER"] = "tcp"
os.environ["MPICH_OFI_STARTUP_CONNECT"] = "0"

from dolfinx import mesh  # noqa: E402
from dolfinx.mesh import Mesh  # noqa: E402

from mpi4py import MPI  # noqa: E402
import panum as pn  # noqa: E402

parameters = pn.ParametersCahnLarche(T=2e-4, num_time_steps=20, nx=64, ny=64)

doublewell = pn.DoubleWellPolynomial()

stiffness_tensor = pn.StiffnessTensor()

diff_eq = pn.DifferentialEquationCahnLarche(
    doublewell=doublewell,
    parameters=parameters,
    imex="Eyre",
    stiffness_tensor=stiffness_tensor,
)

msh: Mesh = mesh.create_unit_square(
    MPI.COMM_WORLD,
    parameters.nx,
    parameters.ny,
    cell_type=mesh.CellType.triangle,
)

cross_initialcondition = pn.Cross(width=0.3)
half_initialcondition = pn.Half()


femhandler = pn.FEMHandlerCahnLarche(
    msh,
    parameters=parameters,
    initialcondition=half_initialcondition,
    doublewell=doublewell,
)

callbacks = []
# Optional live plot of the phase field (requires pyvista/pyvistaqt).
plot_solution = True
if plot_solution:
    plot_callback = pn.PyvistaPlotCallback(
        femhandler, parameters, component=0, name="phi"
    )
    callbacks.append(plot_callback)


output_path = "output/cahn_larche/solution_"
save_solutions = pn.SaveXDMFCallback(
    {0: output_path + "phi.xdmf", 2: output_path + "u.xdmf"}, msh, femhandler
)
callbacks.append(save_solutions)


def verbosity_callback(step, t, femhandler):
    print(f"At time step {step} and time {t}")


callbacks.append(verbosity_callback)


timediscretization = pn.IMEXImplicitEuler(
    msh, parameters, femhandler, diff_eq, callbacks
)

timediscretization()
