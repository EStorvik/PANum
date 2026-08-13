from dolfinx import fem
from dolfinx import mesh
from dolfinx.fem.petsc import NonlinearProblem
from dolfinx.mesh import Mesh
from typing import Optional

from mpi4py import MPI


import panum as pn


parameters = pn.ParametersBiharmonic()


# Mesh
msh: Mesh = mesh.create_unit_square(
    MPI.COMM_WORLD, parameters.nx, parameters.ny, cell_type=mesh.CellType.triangle
)

# Manufactured solution
manuf_sol = pn.ManufacturedSolutionBiharmonic(parameters)


# FEMHandler
pn.FEMHandlerBiharmonic(msh, parameters, initialcondition = manuf_sol.phi0)



