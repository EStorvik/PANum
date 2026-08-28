from .core import (
    Parameters,
    FEMHandler,
    TimeDiscretization,
    ImplicitEuler,
    TrapezoidalRule,
    DifferentialEquation,
)

__all__ = [
    "Parameters",
    "FEMHandler",
    "TimeDiscretization",
    "ImplicitEuler",
    "TrapezoidalRule",
    "DifferentialEquation",
]


from .problems.biharmonic import (
    ParametersBiharmonic,
    FEMHandlerBiharmonic,
    AnalyticalSolutionBiharmonic,
    initialize_biharmonic,
    DifferentialEquationBiharmonic,
)

__all__ += [
    "ParametersBiharmonic",
    "AnalyticalSolutionBiharmonic",
    "initialize_biharmonic",
    "FEMHandlerBiharmonic",
    "DifferentialEquationBiharmonic",
]

from .problems.cahnhilliard import (
    DoubleWell,
    DoubleWellPolynomial,
    InitialConditionCahnHilliard,
    Cross,
    initialize_cahn_hilliard,
    DifferentialEquationCahnHilliard,
    FEMHandlerCahnHilliard,
    ParametersCahnHilliard,
)

__all__ += [
    "DoubleWell",
    "DoubleWellPolynomial",
    "InitialConditionCahnHilliard",
    "Cross",
    "initialize_cahn_hilliard",
    "DifferentialEquationCahnHilliard",
    "FEMHandlerCahnHilliard",
    "ParametersCahnHilliard",
]

# Visualization is an optional extra (requires pyvista/pyvistaqt).
try:
    from .vizualization import PyvistaVizualization, PyvistaPlotCallback

    __all__ += ["PyvistaVizualization", "PyvistaPlotCallback"]
except ImportError:
    pass
