from abc import ABC
from typing import Any


class FEMHandlerBase(ABC):
    """Base class for finite element handlers.

    Subclasses build the function space(s) and solution `Function`s for a
    specific PDE. `TimeIntegrator` subclasses, `TimeMarching`, and the
    visualization callbacks rely on the following attributes being set by
    subclasses' `__init__`:

    Attributes:
        V: The (possibly mixed) function space.
        xi: The current solution `Function`.
        xi_old: The previous time-step solution `Function`.
    """

    V: Any
    xi: Any
    xi_old: Any
