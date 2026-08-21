from abc import ABC
from typing import Any


class FEMHandler(ABC):

    V: Any
    xis: dict
    xis_old: dict
    pfs: dict
    pfs_old: dict
    mus: dict
    mus_old: dict
    eta_pfs: dict
    eta_mus: dict

    def copy_to_old(self):
        for i, xi in self.xis.items():
            self.xis_old[i].x.array[:] = xi.x.array
            self.xis_old[i].x.scatter_forward()
