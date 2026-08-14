# Fix MPI/OFI finalization errors on macOS
import os

os.environ["FI_PROVIDER"] = "tcp"
os.environ["MPICH_OFI_STARTUP_CONNECT"] = "0"

from dolfinx import mesh
from dolfinx.mesh import Mesh

from mpi4py import MPI


import panum as pn


parameters = pn.ParametersBiharmonic()


# Mesh
msh: Mesh = mesh.create_unit_square(
    MPI.COMM_WORLD, parameters.nx, parameters.ny, cell_type=mesh.CellType.triangle
)

# Manufactured solution
manuf_sol = pn.ManufacturedSolutionBiharmonic(parameters)


# FEMHandler
femhandler = pn.FEMHandlerBiharmonic(msh, parameters, initialcondition = manuf_sol.phi0)


trapezoidal_rule = pn.TrapezoidalRuleBiharmonic(
    femhandler=femhandler,
    parameters=parameters,
    manuf=manuf_sol,
)


def print_time(step: int, time_integrator, femhandler) -> None:
    print(f"Step {step}: t = {time_integrator.t.value}")


callbacks = [print_time]

# Optional live plot of the phase field (requires pyvista/pyvistaqt).
plot_solution = True
if plot_solution:
    plot_callback = pn.PyvistaPlotCallback(femhandler, parameters, component=0, name="phi")
    callbacks.append(plot_callback)

time_marching = pn.TimeMarching(
    time_integrator=trapezoidal_rule,
    femhandler=femhandler,
    parameters=parameters,
    callbacks=callbacks,
)

time_marching()
