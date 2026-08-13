


"""Phase field smoothing from initial condition."""

from typing import TYPE_CHECKING, Any, cast

import ch_timedisc as ch
from ufl import grad, inner
from dolfinx.fem import Function, functionspace
from ufl import TestFunction, TrialFunction, dx, split
from dolfinx.fem.petsc import LinearProblem
from ufl.core.expr import Expr as UFLExpr

if TYPE_CHECKING:
    from dolfinx.mesh import Mesh


def initial_mu_biharmonic(
    pf0: UFLExpr,
    P: Any,
    msh: "Mesh",
) -> Function:
    """Compute the initial chemical potential ``mu0`` consistent with ``pf0``.

    Solves the ``L2``-projection ``inner(u, v) * dx = inner(grad(pf0), grad(v)) * dx``
    for ``u`` on the finite element space built from ``P`` over ``msh``.

    Args:
        pf0: Initial phase field expression.
        P: Finite element (basix) used to build the scalar function space for ``mu0``.
        msh: The computational mesh.

    Returns:
        The initial chemical potential as a `Function`.
    """
    V = functionspace(msh, P)
    u = TrialFunction(V)
    v = TestFunction(V)


    a = inner(u, v) * dx
    L = inner(grad(pf0), grad(v)) * dx

    problem = LinearProblem(
        a,
        L,
        bcs=[],
        petsc_options_prefix="initial_mu_",
        petsc_options={
            "ksp_type": "preonly",
            "pc_type": "lu",
            "ksp_error_if_not_converged": True,
        },
    )
    mu = cast(Function, problem.solve())

    return mu
