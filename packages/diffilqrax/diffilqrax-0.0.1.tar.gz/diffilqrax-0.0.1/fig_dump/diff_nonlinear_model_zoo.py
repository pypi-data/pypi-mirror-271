from typing import Callable, Any, Optional, NamedTuple, Tuple
from jax import Array
import jax.numpy as jnp
from jax import lax
import jax.random as jr

from diffilqrax.ilqr import Theta, Params, System
from diffilqrax.lqr import ModelDims

# lorenz system
# ----------------

def rk4(dynamics, dt=0.01):
    def integrator(x, u):
        dt2 = dt / 2.0
        k1 = dynamics(x, u)
        k2 = dynamics(x + dt2 * k1, u)
        k3 = dynamics(x + dt2 * k2, u)
        k4 = dynamics(x + dt * k3, u)
        nx_x = x + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        return nx_x, nx_x
    return integrator

class LorenzeParams(NamedTuple):
    sigma:float # = 10.
    rho:float # = 28.
    beta:float # = 8. / 3.


def lorenz_system(current_state:Array, u:Array, theta:LorenzeParams):
    # positions of x, y, z in space at the current time point
    x, y, z = current_state

    # define the 3 ordinary differential equations known as the lorenz equations
    dx_dt = theta.sigma * (y - x) + u
    dy_dt = x * (theta.rho - z) - y + u
    dz_dt = x * y - theta.beta * z + u

    # return a list of the equations that describe the system
    nx_state = jnp.array([dx_dt, dy_dt, dz_dt])
    return nx_state

us_lorenz = jnp.zeros_like(t)

initial_state = jnp.array([[-8.], [8.], [27.]])
params = Params(initial_state, LorenzeParams(10.,28.,8./3.))

model = System(dynamics=rk4(lorenz_system, dt=.01),
       dims=ModelDims(horizon=100, n=3, m=1, dt=0.1),
       cost=None,
       costf=None)


xf, lorenz_Xs = lax.scan(f=rk4(lorenz_system, dt=.01), init=initial_state, xs=us_lorenz)

key = jr.PRNGKey(42)
new_key, subkey = jr.split(key)
us_lorenz = jnp.clip(jr.t(new_key, .9, shape=(4000,)), None, 100)
# fig, ax = plt.subplots()
ax.plot(us_lorenz)

# inverted pendulum dynamics
# ----------------
class PendulumParams(NamedTuple):
    m: float
    l: float
    g: float

def pendulum_dynamics(t: int, x: Array, u: Array, theta: PendulumParams):
    """simulate the dynamics of a pendulum. x0 is sin(theta), x1 is cos(theta), x2 is theta_dot. 
    u is the torque applied to the pendulum.

    Args:
        t (int): _description_
        x (Array): state params
        u (Array): external input
        theta (PendulumParams): parameters
    """
    dt=0.1
    sin_theta = x[0]
    cos_theta = x[1]
    theta_dot = x[2]
    torque = u
    
    # Deal with angle wrap-around.
    theta = jnp.arctan2(sin_theta, cos_theta)

    # Define acceleration.
    theta_dot_dot = -3.0 * theta.g / (2 * theta.l) * jnp.sin(theta + jnp.pi)
    theta_dot_dot += 3.0 / (theta.m * theta.l**2) * torque

    next_theta = theta + theta_dot * dt
    
    next_state = jnp.array([jnp.sin(next_theta), jnp.cos(next_theta), theta_dot + theta_dot_dot * dt])
    return next_state


# nonlinear double integrator dynamics
# ----------------
def double_integrator_dynamics(t: int, x: Array, u: Array, theta: Theta):
    """simulate the dynamics of a double integrator. x0 is position, x1 is velocity.

    Args:
        t (int): _description_
        x (Array): state params
        u (Array): external input
        theta (Theta): parameters
    """
    dt=0.1
    p, v = x
    a, = u
    
    next_x = jnp.array([p + v * dt + p * a * dt**2 / 2, v + a * dt])
    return next_x


def load_fixtures(fp):
    import numpy as np
    data = np.load(fp)
    Us_init= data['U_orig'][...,None]
    Xs_init= data['X_orig'][...,None]
    Xs_traj= data['X'][...,None]
    Us_traj= data['U'][...,None]
    Lambdas_traj= data['adjoints'][...,None]
    x0= data['x0'][...,None]
    theta = Theta(Uh=data['Uh'], Wh=data['Wh'], sigma=0)
    params = Params(x0, theta)

    return params, theta,x0, (Us_init, Xs_init), (Us_traj, Xs_traj, Lambdas_traj)

params, theta,x0, (Us_init, Xs_init), (Us_traj, Xs_traj, Lambdas_traj) = load_fixtures("/Users/thomasmullen/Documents/01 Zenith/17 IQLR/Python/Validation data/trajax_ilqr_fixtures/trajax_fixtures.npz")