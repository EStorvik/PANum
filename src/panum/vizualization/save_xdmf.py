
from dolfinx.io import XDMFFile
from mpi4py import MPI
from dolfinx.mesh import Mesh

from pathlib import Path
from panum import FEMHandler


class SaveXDMFCallback:
    def __init__(self, file_paths: dict[int, str], msh: Mesh, femhandler: FEMHandler, t0: float = 0):
        """
        arguments:
        - file_paths: a dictionary where the keys represent the component to be saved, and the values are the paths where it should be saved.
        """
        self.output_files: dict[int, XDMFFile] = {}
        functions = femhandler.xi.split()
        for component, path in file_paths.items():
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            self.output_files.update({component: XDMFFile(MPI.COMM_WORLD, path, "w")})
            self.output_files[component].write_mesh(msh)
            self.output_files[component].write_function(functions[component], t0)


    def __call__(self, step: int, t: float, femhandler: FEMHandler):
        functions = femhandler.xi.split()
        for component, file in self.output_files.items():
            file.write_function(functions[component], t)






