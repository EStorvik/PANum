from abc import ABC
from dolfinx.fem.function import FunctionSpace
from dolfinx.fem import Function
from ufl import Argument, split, TestFunction


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

    V: FunctionSpace
    xi: Function
    xi_old: Function
    xi_stages: list[Function] = []
    eta: Argument
    stages: int = 1
    us: dict
    us_old: dict
    us_stages: list[dict] = []
    vs: dict
    vs_old: dict
    vs_stages: list[dict] = []
    eta_us: dict
    eta_vs: dict

    def copy_to_old(self):
        self.xi_old.x.array[:] = self.xi.x.array
        self.xi_old.x.scatter_forward()

    def generate_functions(self):
        self.xi: Function = Function(self.V)
        self.eta: Argument = TestFunction(self.V)
        for _ in range(self.stages):
            self.xi_stages.append(Function(self.V))
        self.xi_old = self.xi_stages[0]

    def update_stages(self, stages):
        self.stages = stages
        self.xi_stages = []
        for _ in range(self.stages):
            self.xi_stages.append(Function(self.V))
        self.xi_old = self.xi_stages[0]
