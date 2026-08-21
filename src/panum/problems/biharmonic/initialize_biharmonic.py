"""Phase field smoothing from initial condition."""

from typing import Any

from ufl import grad, inner
from dolfinx.fem import Function
from ufl import TestFunctions, TrialFunctions, dx
from dolfinx.fem.petsc import LinearProblem
from ufl.core.expr import Expr as UFLExpr


def initialize_biharmonic(
    pf0: UFLExpr,
    V: Any,
) -> Function:
    """ """
    p, m = TrialFunctions(V)

    v, w = TestFunctions(V)

    a = inner(p, v) * dx + inner(m, w) * dx
    L = inner(pf0, v) * dx + inner(grad(pf0), grad(w)) * dx

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
    z = problem.solve()

    return z.sub(0).collapse(), z.sub(1).collapse()
