from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load_module():
    module_path = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "biharmonic_convergence_rates.py"
    )
    spec = spec_from_file_location("biharmonic_convergence_rates", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compute_convergence_ratios_returns_pairwise_ratios() -> None:
    module = load_module()

    assert module.compute_convergence_ratios([16.0, 4.0, 1.0]) == [4.0, 4.0]


def test_run_convergence_study_uses_each_time_step_once() -> None:
    module = load_module()
    calls: list[int] = []

    def solve_error(num_time_steps: int) -> float:
        calls.append(num_time_steps)
        return 1.0 / num_time_steps

    errors, convergence_ratios = module.run_convergence_study(
        [1, 2, 4], solve_error
    )

    assert calls == [1, 2, 4]
    assert errors == [1.0, 0.5, 0.25]
    assert convergence_ratios == [2.0, 2.0]
