"""Non-linear pendulum example"""

from typing import Any, Union
from jax import Array
import jax.numpy as jnp
import jax.random as jr

from diffilqrax.utils import keygen
from diffilqrax.ilqr import ilqr_solver
from diffilqrax.typs import (
    iLQRParams,
    System,
    ModelDims,
    PendulumParams,
    Theta
)


def pendulum_dynamics(t: int, x: Array, u: Array, theta: PendulumParams):
    """simulate the dynamics of a pendulum. x0 is sin(theta), x1 is cos(theta), x2 is theta_dot.
    u is the torque applied to the pendulum.

    Args:
        t (int): _description_
        x (Array): state params
        u (Array): external input
        theta (Theta): parameters
    """
    dt = 0.1
    sin_theta, cos_theta, theta_dot = x
    torque = u[0]

    # Deal with angle wrap-around.
    theta_state = jnp.arctan2(sin_theta, cos_theta)

    # Define acceleration.
    theta_dot_dot = -3.0 * theta.g / (2 * theta.l) * jnp.sin(theta_state + jnp.pi)
    theta_dot_dot += 3.0 / (theta.m * theta.l**2) * torque

    next_theta = theta_state + theta_dot * dt

    next_state = jnp.array(
        [jnp.sin(next_theta), jnp.cos(next_theta), theta_dot + theta_dot_dot * dt]
    )
    return next_state


def pendulum_model():
    """define pendulum model with cost, dynamics and cost function"""
    def cost(t: int, x: Array, u: Array, theta: Any):
        return jnp.sum(x**2) + jnp.sum(u**2)

    def costf(x: Array, theta: Any):
        return jnp.sum(x**2)

    def dynamics(t: int, x: Array, u: Array, theta: Union[Theta, PendulumParams]):
        return pendulum_dynamics(t, x, u, theta)

    return System(cost, costf, dynamics, ModelDims(horizon=100, n=3, m=1, dt=0.1))


if __name__ == "__main__":
    key = jr.PRNGKey(seed=234)
    key, skeys = keygen(key, 5)

    ls_kwargs = {
        "beta": 0.8,
        "max_iter_linesearch": 16,
        "tol": 1e0,
        "alpha_min": 0.0001,
    }

    theta = PendulumParams(m=1, l=2, g=9.81)
    params = iLQRParams(x0=jr.normal(next(skeys), (3,)), theta=theta)
    model = pendulum_model()

    Us_init = jnp.zeros((model.dims.horizon, 1))

    # test ilqr solver
    (Xs_stars, Us_stars, Lambs_stars), converged_cost, cost_log = ilqr_solver(
        model,
        params,
        Us_init,
        max_iter=40,
        convergence_thresh=1e-8,
        alpha_init=1.0,
        verbose=True,
        use_linesearch=True,
        **ls_kwargs,
    )

    print(f"Converged cost: {converged_cost}")
    print(Xs_stars.shape, Us_stars.shape, Lambs_stars.shape)
