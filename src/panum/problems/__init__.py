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
    FEMHandlerCahnHilliard,
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
    "FEMHandlerCahnHilliard",
]
