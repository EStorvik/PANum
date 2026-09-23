from abc import ABC, abstractmethod
from collections.abc import Mapping
from dolfinx.fem import Function
from ufl import Argument, TestFunction


class FEMHandler(ABC):
    """
    Attributes:
        V [FunctionSpace]: Function space
        xi [Function]: Solution function
        xi_old [Function]: solution function at previous time step
        xi_stages [List[Functions]]: solution function at each stage
        eta [Argument]: Test Function
        stages [int]: number of stages for multistage methods - default is 1
        us [dict]: dictionary of functions in which the time derivative is taken
        vs [dict]: dictionary of functions in which a time derivative is not taken
        us_old [dict]:
        vs_old [dict]:
        us_stages [list[dict]]:
        vs_stages [list[dict]]:
        eta_us [dict]: test functions corresponding to each u
        eta_vs [dict]: test functions coresponding to each v
    """

    def __init__(self) -> None:

        self.generate_functions()

        # Subclasses must wire split fields and stage dictionaries.
        self.define_fields()
        self.validate_fields()

    @abstractmethod
    def define_fields(self) -> None:
        """Populate us/vs dictionaries, eta dictionaries, and stage views."""
        ...

    def copy_to_old(self):
        self.xi_old.x.array[:] = self.xi.x.array
        self.xi_old.x.scatter_forward()

    def generate_functions(self):
        self.xi: Function = Function(self.V)
        self.eta: Argument = TestFunction(self.V)
        self.xi_stages: list[Function] = []
        for _ in range(self.stages):
            self.xi_stages.append(Function(self.V))
        self.xi_old: Function = self.xi_stages[0]

    def update_stages(self, stages):
        self.stages = stages
        self.xi_stages = []
        for _ in range(self.stages):
            self.xi_stages.append(Function(self.V))
        self.xi_old = self.xi_stages[0]

    def validate_fields(self) -> None:
        """Validate that subclass field dictionaries are present and aligned."""
        required = (
            "us",
            "vs",
            "eta_us",
            "eta_vs",
            "us_old",
            "vs_old",
            "us_stages",
            "vs_stages",
        )
        missing = [name for name in required if not hasattr(self, name)]
        if missing:
            raise AttributeError(
                "FEMHandler subclass missing required field definitions: "
                + ", ".join(missing)
            )

        for name in ("us", "vs", "eta_us", "eta_vs", "us_old", "vs_old"):
            value = getattr(self, name)
            if not isinstance(value, Mapping):
                raise TypeError(
                    f"FEMHandler field '{name}' must be a mapping, got {type(value).__name__}."
                )

        for name in ("us_stages", "vs_stages"):
            value = getattr(self, name)
            if not isinstance(value, list):
                raise TypeError(
                    f"FEMHandler field '{name}' must be a list, got {type(value).__name__}."
                )

        us_keys = set(self.us.keys())
        if us_keys != set(self.eta_us.keys()) or us_keys != set(
            self.us_old.keys()
        ):
            raise ValueError("Keys of us, eta_us, and us_old must match.")

        vs_keys = set(self.vs.keys())
        if vs_keys != set(self.eta_vs.keys()) or vs_keys != set(
            self.vs_old.keys()
        ):
            raise ValueError("Keys of vs, eta_vs, and vs_old must match.")

        if not self.us_stages or not self.vs_stages:
            raise ValueError(
                "us_stages and vs_stages must contain at least one stage mapping."
            )
