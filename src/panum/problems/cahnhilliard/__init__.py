from .differential_equation import DifferentialEquationCahnHilliard
from .parameters import ParametersCahnHilliard
from .doublewell import DoubleWell, DoubleWellPolynomial
from .initialconditions import (
    InitialConditionCahnHilliard,
    Cross,
    Random,
    initialize_cahn_hilliard,
    Half,
)
from .femhandler import FEMHandlerCahnHilliard

__all__ = [
    "ParametersCahnHilliard",
    "DifferentialEquationCahnHilliard",
    "DoubleWell",
    "DoubleWellPolynomial",
    "InitialConditionCahnHilliard",
    "Cross",
    "Half",
    "Random",
    "initialize_cahn_hilliard",
    "FEMHandlerCahnHilliard",
]
