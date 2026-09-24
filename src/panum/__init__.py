from .core import (
    Parameters,
    FEMHandler,
    TimeDiscretization,
    ImplicitEuler,
    DifferentialEquation,
    ThetaMethod,
    IMEXImplicitEuler,
    DirichletBC,
)

__all__ = [
    "Parameters",
    "FEMHandler",
    "TimeDiscretization",
    "ImplicitEuler",
    "DifferentialEquation",
    "ThetaMethod",
    "IMEXImplicitEuler",
    "DirichletBC",
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
    Half,
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
    "Half",
    "initialize_cahn_hilliard",
    "DifferentialEquationCahnHilliard",
    "FEMHandlerCahnHilliard",
    "ParametersCahnHilliard",
]

from .problems.cahnlarche import (
    ParametersCahnLarche,
    DifferentialEquationCahnLarche,
    FEMHandlerCahnLarche,
    StiffnessTensor,
)

__all__ += [
    "ParametersCahnLarche",
    "DifferentialEquationCahnLarche",
    "FEMHandlerCahnLarche",
    "StiffnessTensor",
]


# Visualization is an optional extra (requires pyvista/pyvistaqt).
try:
    from .vizualization import PyvistaVizualization, PyvistaPlotCallback

    __all__ += ["PyvistaVizualization", "PyvistaPlotCallback"]
except ImportError:
    pass

from .vizualization import SaveXDMFCallback
__all__ += [
    "SaveXDMFCallback",
]
