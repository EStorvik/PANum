# Fix MPI/OFI finalization errors on macOS
import os

os.environ["FI_PROVIDER"] = "tcp"
os.environ["MPICH_OFI_STARTUP_CONNECT"] = "0"


from panum import DoubleWellPolynomial  # noqa: E402
import numpy as np  # noqa: E402


def test_eyre_split() -> None:

    doublewell = DoubleWellPolynomial()
    xx = np.linspace(0, 1, 100)

    assert np.allclose(doublewell(xx), doublewell.c(xx) - doublewell.e(xx))
    assert np.allclose(
        doublewell.prime(xx), doublewell.cprime(xx) - doublewell.eprime(xx)
    )
