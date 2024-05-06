"""LQR solver via dynamic programming"""

from typing import Callable, Tuple
from jax.typing import ArrayLike
from jax import Array
import jax
from jax import lax
import jax.numpy as jnp

from diffilqrax.typs import *

jax.config.update("jax_enable_x64", True)  # double precision
# symmetrise
symmetrise_tensor = lambda x: (x + x.transpose(0, 2, 1)) / 2
symmetrise_matrix = lambda x: (x + x.T) / 2

def bmm(arr1: Array, arr2: Array) -> Array:
    """Batch matrix multiplication"""
    return jax.vmap(jnp.matmul)(arr1, arr2)

# LQR struct
LQRBackParams = Tuple[
    ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike, ArrayLike
]


def simulate_trajectory(
    dynamics: Callable, Us: ArrayLike, params: LQRParams, dims: ModelDims
) -> Array:
    """Simulate forward pass with LQR params

    Args:
        dynamics (Callable): function of dynamics with args t, x, u, params
        Us (ArrayLike): Input timeseries shape [Txm]
        params (Params): Parameters containing x_init, horizon and theta
        dims (ModelDims): Parameters containing shape of system n, m, horizon and dt

    Returns:
        Array: state trajectory [(T+1)xn]
    """
    horizon = dims.horizon
    x0, lqr = params.x0, params[1]

    def step(x, inputs):
        t, u = inputs
        nx = dynamics(t, x, u, lqr)
        return nx, nx

    _, Xs = lax.scan(step, x0, (jnp.arange(horizon), Us))

    return jnp.vstack([x0[None], Xs])


def lin_dyn_step(t: int, x: ArrayLike, u: ArrayLike, lqr: LQR) -> Array:
    """State space linear step"""
    nx = lqr.A[t] @ x + lqr.B[t] @ u + lqr.a[t]
    return nx


def lqr_adjoint_pass(Xs: ArrayLike, Us: ArrayLike, params: LQRParams) -> Array:
    """Adjoint backward pass with LQR params

    Args:
        Xs (np.ndarray): State timeseries shape [(T+1)xn]
        Us (np.ndarray): Input timeseries shape [Txm]
        params (Params): LQR state and cost matrices

    Returns:
        np.ndarray: adjoint λs [(T+1)xn]
    """
    lqr = params[1]
    AT = lqr.A.transpose(0, 2, 1)
    lambf = lqr.Qf @ Xs[-1] + lqr.qf

    def adjoint_step(lamb, inputs):
        x, u, aT, Q, q, S = inputs
        nlamb = aT @ lamb + Q @ x + q + S @ u
        return nlamb, nlamb

    lambs = lax.scan(
        adjoint_step, lambf, (Xs[:-1], Us[:], AT, lqr.Q, lqr.q, lqr.S), reverse=True
    )[1]
    return jnp.vstack([lambs, lambf[None]])


def lqr_forward_pass(gains: Gains, params: LQRParams) -> Tuple[Array, Array]:
    """LQR forward pass using gain state feedback

    Args:
        gains (Gains): K matrices
        params (Params): LQR state and cost matrices

    Returns:
        Tuple[Array, Array]: updated state [(T+1)xn] and inputs [Txm]
    """
    x0, lqr = params.x0, params.lqr

    def dynamics(x: jnp.array, params: LQRBackParams):
        A, B, a, K, k = params
        u = K @ x + k
        nx = A @ x + B @ u + a
        return nx, (nx, u)

    Xs, Us = lax.scan(
        dynamics, init=x0, xs=(lqr.A, lqr.B, lqr.a, gains.K, gains.k)
    )[1]

    return jnp.vstack([x0[None], Xs]), Us


def calc_expected_change(dJ: CostToGo, alpha: float = 0.5):
    """expected change in cost [Tassa, 2020]"""
    return -(dJ.V * alpha**2 + dJ.v * alpha)


def lqr_backward_pass(
    lqr: LQR,
    dims: ModelDims,
    expected_change: bool = False,
    verbose: bool = False,
) -> Gains:
    """LQR backward pass learn optimal Gains given LQR cost constraints and dynamics

    Args:
        lqr (LQR): LQR parameters
        T (int): parameter time horizon
        expected_change (bool, optional): Estimate expected change in cost [Tassa, 2020].
        Defaults to False.
        verbose (bool, optional): Print out matrix shapes for debugging. Defaults to False.

    Returns:
        Gains: Optimal feedback gains.
    """
    AT, BT = lqr.A.transpose(0, 2, 1), lqr.B.transpose(0, 2, 1)

    def riccati_step(
        carry: Tuple[CostToGo, CostToGo], t: int
    ) -> Tuple[CostToGo, Gains]:
        curr_val, cost_step = carry
        V, v, dJ, dj = curr_val.V, curr_val.v, cost_step.V, cost_step.v
        Hxx = symmetrise_matrix(lqr.Q[t] + AT[t] @ V @ lqr.A[t])
        Huu = symmetrise_matrix(lqr.R[t] + BT[t] @ V @ lqr.B[t])
        Hxu = lqr.S[t] + AT[t] @ V @ lqr.B[t]
        hx = lqr.q[t] + AT[t] @ (v + V @ lqr.a[t])
        hu = lqr.r[t] + BT[t] @ (v + V @ lqr.a[t])

        # With Levenberg-Marquardt regulisation
        min_eval = jnp.linalg.eigh(Huu)[0][0]
        I_mu = jnp.maximum(0.0, 1e-6 - min_eval) * jnp.eye(dims.m)

        # solve gains
        K = -jnp.linalg.solve(Huu + I_mu, Hxu.T)
        k = -jnp.linalg.solve(Huu + I_mu, hu)

        if verbose:
            assert I_mu.shape == (dims.m, dims.m)
            assert v.shape == (dims.n,)
            assert V.shape == (dims.n, dims.n)
            assert Hxx.shape == (dims.n, dims.n)
            assert Huu.shape == (dims.m, dims.m)
            assert Hxu.shape == (dims.n, dims.m)
            assert hx.shape == (dims.n,)
            assert hu.shape == (dims.m,)
            assert k.shape == (dims.m,)
            assert K.shape == (dims.m, dims.n)

        # Find value iteration at current time
        V_curr = symmetrise_matrix(Hxx + Hxu @ K + K.T @ Hxu.T + K.T @ Huu @ K)
        v_curr = hx + (K.T @ Huu @ k) + (K.T @ hu) + (Hxu @ k)

        # expected change in cost
        dJ = dJ + 0.5 * (k.T @ Huu @ k).squeeze()
        dj = dj + (k.T @ hu).squeeze()

        return (CostToGo(V_curr, v_curr), CostToGo(dJ, dj)), Gains(K, k)

    (V_0, dJ), Ks = lax.scan(
        riccati_step,
        init=(CostToGo(lqr.Qf, lqr.qf), (CostToGo(0.0, 0.0))),
        xs=jnp.arange(dims.horizon),
        reverse=True,
    )

    if verbose:
        assert lax.bitwise_not(jnp.any(jnp.isnan(Ks.K)))
        assert lax.bitwise_not(jnp.any(jnp.isnan(Ks.k)))

    if not expected_change:
        return dJ, Ks

    return (dJ, Ks), calc_expected_change(dJ=dJ)


def kkt(params: LQRParams, Xs: Array, Us: Array, Lambs: Array):
    """Define KKT conditions for LQR problem"""
    AT = params.lqr.A.transpose(0, 2, 1)
    BT = params.lqr.B.transpose(0, 2, 1)
    ST = params.lqr.S.transpose(0, 2, 1)
    dLdXs = (
        bmm(params.lqr.Q, Xs[:-1])
        + bmm(params.lqr.S, Us[:])
        + params.lqr.q
        + bmm(AT, Lambs[1:])
        - Lambs[:-1]
    )
    dLdXf = jnp.matmul(params.lqr.Qf, Xs[-1]) + params.lqr.qf - Lambs[-1]
    dLdXs = jnp.concatenate([dLdXs, dLdXf[None]])
    dLdUs = (
        bmm(ST, Xs[:-1]) + bmm(params.lqr.R, Us[:]) + params.lqr.r + bmm(BT, Lambs[1:])
    )
    dLdLambs = (
        bmm(params.lqr.A, Xs[:-1]) + bmm(params.lqr.B, Us[:]) + params.lqr.a - Xs[1:]
    )
    dLdLamb0 = params.x0 - Xs[0]
    dLdLambs = jnp.concatenate([dLdLamb0[None], dLdLambs])
    return dLdXs, dLdUs, dLdLambs


def solve_lqr(params: LQRParams, sys_dims: ModelDims):
    "run backward forward sweep to find optimal control"
    # backward
    _, gains = lqr_backward_pass(params.lqr, sys_dims)
    # forward
    Xs, Us = lqr_forward_pass(gains, params)
    # adjoint
    Lambs = lqr_adjoint_pass(Xs, Us, params)
    return gains, Xs, Us, Lambs


def solve_lqr_swap_x0(params: LQRParams, sys_dims: ModelDims):
    "run backward forward sweep to find optimal control freeze x0 to zero"
    # backward
    # print("r", new_params.lqr.r[-10:])
    _, gains = lqr_backward_pass(params.lqr, sys_dims)
    # print("k", gains.k[-10:])
    new_params = LQRParams(jnp.zeros_like(params.x0), params.lqr)
    Xs, Us = lqr_forward_pass(gains, new_params)
    # adjoint
    Lambs = lqr_adjoint_pass(Xs, Us, new_params)
    return gains, Xs, Us, Lambs
