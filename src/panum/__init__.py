from .core import ParametersBase, FEMHandlerBase, TimeIntegrator, TimeMarching
from .problems.biharmonic import (
    ParametersBiharmonic,
    FEMHandlerBiharmonic,
    ManufacturedSolutionBiharmonic,
    initial_mu_biharmonic,
    BiharmonicWeakForm,
    TrapezoidalRuleBiharmonic,
)

__all__ = [
    "ParametersBase",
    "FEMHandlerBase",
    "TimeIntegrator",
    "TimeMarching",
    "ParametersBiharmonic",
    "ManufacturedSolutionBiharmonic",
    "initial_mu_biharmonic",
    "FEMHandlerBiharmonic",
    "BiharmonicWeakForm",
    "TrapezoidalRuleBiharmonic",
]

# Visualization is an optional extra (requires pyvista/pyvistaqt).
try:
    from .vizualization import PyvistaVizualization, PyvistaPlotCallback

    __all__ += ["PyvistaVizualization", "PyvistaPlotCallback"]
except ImportError:
    pass
