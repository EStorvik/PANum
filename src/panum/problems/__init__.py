from .biharmonic import (
    ParametersBiharmonic,
    FEMHandlerBiharmonic,
    AnalyticalSolutionBiharmonic,
    initialize_biharmonic,
    DifferentialEquationBiharmonic,
)

from .cahnhilliard import (
    ParametersCahnHilliard,
    DifferentialEquationCahnHilliard,
    DoubleWell,
    DoubleWellPolynomial,
    InitialConditionCahnHilliard,
    Cross,
    Half,
    FEMHandlerCahnHilliard,
    Random,
)

from .cahnlarche import (
    ParametersCahnLarche,
    DifferentialEquationCahnLarche,
    FEMHandlerCahnLarche,
    StiffnessTensor,
)

__all__ = [
    "ParametersBiharmonic",
    "FEMHandlerBiharmonic",
    "AnalyticalSolutionBiharmonic",
    "initialize_biharmonic",
    "DifferentialEquationBiharmonic",
    "ParametersCahnHilliard",
    "DifferentialEquationCahnHilliard",
    "DoubleWell",
    "DoubleWellPolynomial",
    "InitialConditionCahnHilliard",
    "Cross",
    "Half",
    "Random",
    "FEMHandlerCahnHilliard",
    "ParametersCahnLarche",
    "DifferentialEquationCahnLarche",
    "FEMHandlerCahnLarche",
    "StiffnessTensor",
]
