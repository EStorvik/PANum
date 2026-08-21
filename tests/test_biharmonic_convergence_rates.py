import os
from pathlib import Path
from types import ModuleType
import runpy

import pytest


def load_module() -> ModuleType:
    module_path = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "biharmonic_convergence_rates.py"
    )
    module = ModuleType("biharmonic_convergence_rates")
    original_fi_provider = os.environ.get("FI_PROVIDER")
    original_startup_connect = os.environ.get("MPICH_OFI_STARTUP_CONNECT")
    try:
        module.__dict__.update(
            runpy.run_path(str(module_path), run_name=module.__name__)
        )
    finally:
        restore_env("FI_PROVIDER", original_fi_provider)
        restore_env("MPICH_OFI_STARTUP_CONNECT", original_startup_connect)
    return module


def restore_env(name: str, value: str | None) -> None:
    if value is None:
        os.environ.pop(name, None)
    else:
        os.environ[name] = value


@pytest.fixture(scope="module")
def convergence_module() -> ModuleType:
    return load_module()


def test_compute_convergence_ratios_returns_pairwise_ratios(
    convergence_module: ModuleType,
) -> None:

    assert convergence_module.compute_convergence_ratios([16.0, 4.0, 1.0]) == [
        4.0,
        4.0,
    ]


def test_run_convergence_study_uses_each_time_step_once(
    convergence_module: ModuleType,
) -> None:
    calls: list[int] = []

    def solve_error(num_time_steps: int) -> float:
        calls.append(num_time_steps)
        return 1.0 / num_time_steps

    errors, convergence_ratios = convergence_module.run_convergence_study(
        [1, 2, 4], solve_error
    )

    assert calls == [1, 2, 4]
    assert errors == [1.0, 0.5, 0.25]
    assert convergence_ratios == [2.0, 2.0]
