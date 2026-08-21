from .core import (
    Parameters,
    FEMHandler,
    TimeDiscretization,
    ImplicitEuler,
    TrapezoidalRule,
    DifferentialEquation,
)
from .problems.biharmonic import (
    ParametersBiharmonic,
    FEMHandlerBiharmonic,
    ManufacturedSolutionBiharmonic,
    initial_mu_biharmonic,
    DifferentialEquationBiharmonic,
)

__all__ = [
    "Parameters",
    "FEMHandler",
    "TimeDiscretization",
    "ImplicitEuler",
    "TrapezoidalRule",
    "DifferentialEquation",
    "ParametersBiharmonic",
    "ManufacturedSolutionBiharmonic",
    "initial_mu_biharmonic",
    "FEMHandlerBiharmonic",
    "DifferentialEquationBiharmonic",
]

# Visualization is an optional extra (requires pyvista/pyvistaqt).
try:
    from .vizualization import PyvistaVizualization, PyvistaPlotCallback

    __all__ += ["PyvistaVizualization", "PyvistaPlotCallback"]
except ImportError:
    pass
