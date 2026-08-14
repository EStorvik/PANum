from .FEMHandler import FEMHandlerBiharmonic
from .initial_contidions import initial_mu_biharmonic
from .ManufacturedSolutions import ManufacturedSolutionBiharmonic
from .Parameters import ParametersBiharmonic
from .TimeDiscretization import TimeIntegrator, TrapezoidalRuleBiharmonic, TimeMarching

__all__ = [
    "ParametersBiharmonic",
    "ManufacturedSolutionBiharmonic",
    "initial_mu_biharmonic",
    "FEMHandlerBiharmonic",
    "TimeIntegrator",
    "TrapezoidalRuleBiharmonic",
    "TimeMarching",
]

# Visualization is an optional extra (requires pyvista/pyvistaqt).
try:
    from .vizualization import PyvistaVizualization, PyvistaPlotCallback

    __all__ += ["PyvistaVizualization", "PyvistaPlotCallback"]
except ImportError:
    pass
