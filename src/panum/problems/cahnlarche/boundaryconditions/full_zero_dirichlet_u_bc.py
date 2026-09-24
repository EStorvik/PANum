from panum import DirichletBC
import numpy as np


class DirichletZeroFullBoundary:

    def __init__(self):
        self.value = lambda x: np.zeros((2, x.shape[1]))

    # Boundary conditions
    def full_boundary(self, x):
        return np.logical_or(
            np.logical_or(np.isclose(x[0], 0.0), np.isclose(x[0], 1.0)),
            np.logical_or(np.isclose(x[1], 0.0), np.isclose(x[1], 1.0)),
        )

    def __call__(self, msh, V, u):
        condition = {0: [self.full_boundary, V, u, self.value]}
        dbc = DirichletBC(msh=msh, condition=condition)
        return dbc.bcs
