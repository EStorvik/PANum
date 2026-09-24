
from dolfinx.mesh import locate_entities_boundary
from dolfinx.fem.function import FunctionSpace
from dolfinx.fem import locate_dofs_topological, Function, dirichletbc

from typing import Callable

class DirichletBC:

    def __init__(
            self,
            msh,
            condition: dict[int, list[Callable, FunctionSpace, Function, Callable]],
    ):
        """
        arguments:
        msh: Mesh,
        condition: Should contain a dictionary where the keys are ints (representing each boundary condition), and the values are a list in the following order: Callable that defines the boundary region, FunctionSpace for the function, a callable with the values of the function on that boundary
        """
        self.msh = msh

        self.bcs = []

        for i in condition.keys():
            facets = locate_entities_boundary(self.msh, self.msh.topology.dim - 1, condition[i][0])
            dofs = locate_dofs_topological(condition[i][1], self.msh.topology.dim-1, facets)
            u = condition[i][2]
            u.interpolate(condition[i][3])
            self.bcs.append(dirichletbc(u, dofs))