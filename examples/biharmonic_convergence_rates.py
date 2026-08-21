# Fix MPI/OFI finalization errors on macOS
import os
from collections.abc import Callable, Sequence

os.environ["FI_PROVIDER"] = "tcp"
os.environ["MPICH_OFI_STARTUP_CONNECT"] = "0"

DEFAULT_NUM_TIME_STEPS_LIST = [1, 2, 4, 8, 16]


def compute_convergence_ratios(errors: Sequence[float]) -> list[float]:
    return [errors[i] / errors[i + 1] for i in range(len(errors) - 1)]


def run_convergence_study(
    num_time_steps_list: Sequence[int],
    solve_error: Callable[[int], float],
) -> tuple[list[float], list[float]]:
    errors_list = [
        solve_error(num_time_steps) for num_time_steps in num_time_steps_list
    ]
    return errors_list, compute_convergence_ratios(errors_list)


def solve_biharmonic_error(num_time_steps: int) -> float:
    from dolfinx import mesh
    from dolfinx.mesh import Mesh
    from mpi4py import MPI
    import panum as pn

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
    return analyticalsol.L2_error(femhandler, parameters.T)


def main() -> None:
    errors_list, convergence_ratios = run_convergence_study(
        DEFAULT_NUM_TIME_STEPS_LIST, solve_biharmonic_error
    )

    for num_time_steps, error in zip(DEFAULT_NUM_TIME_STEPS_LIST, errors_list):
        print(f"At number of time steps = {num_time_steps} the error is: {error}")

    for convergence_ratio in convergence_ratios:
        print(convergence_ratio)


if __name__ == "__main__":
    main()
