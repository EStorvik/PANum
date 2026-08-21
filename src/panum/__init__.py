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
    AnalyticalSolutionBiharmonic,
    initialize_biharmonic,
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
    "AnalyticalSolutionBiharmonic",
    "initialize_biharmonic",
    "FEMHandlerBiharmonic",
    "DifferentialEquationBiharmonic",
]

# Visualization is an optional extra (requires pyvista/pyvistaqt).
try:
    from .vizualization import PyvistaVizualization, PyvistaPlotCallback

    __all__ += ["PyvistaVizualization", "PyvistaPlotCallback"]
except ImportError:
    pass
