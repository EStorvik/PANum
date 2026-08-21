from abc import ABC


class DifferentialEquation(ABC):
    """
    Differential equations are assumed to be coupled and on the form:
    d_t(u_1) = G_1(u_1, ..., u_n, v_1, ..., v_m)
    ...
    d_t(u_n) = G_n(u_1, ..., u_n, v_1, ..., v_m)
    H_1(u_1, ..., v_m) = 0
    ...
    H_n(u_1, ... v_m) = 0

    The G's and H's should be dictionaries
    """

    G: dict
    H: dict
