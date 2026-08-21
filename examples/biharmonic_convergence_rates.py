# Fix MPI/OFI finalization errors on macOS
import os

os.environ["FI_PROVIDER"] = "tcp"
os.environ["MPICH_OFI_STARTUP_CONNECT"] = "0"

from dolfinx import mesh  # noqa: E402
from dolfinx.mesh import Mesh  # noqa: E402

from mpi4py import MPI  # noqa: E402
import panum as pn  # noqa: E402


num_time_steps_list = [1, 2, 4, 8, 16]
errors_list = []


for num_time_steps in num_time_steps_list:

    parameters = pn.ParametersBiharmonic(
        T=1e-4,
        num_time_steps=num_time_steps,
        nx=64,
        ny=64,
        finite_element_degree=2,
    )
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
    timediscretization = pn.TrapezoidalRule(
        msh, parameters, femhandler, diff_eq
    )

    timediscretization()
    error = analyticalsol.L2_error(femhandler, parameters.T)
    print(f"At number of time steps = {num_time_steps} the error is: {error}")
    errors_list.append(error)

for i in range(len(errors_list) - 1):
    print(errors_list[i] / errors_list[i + 1])
