from map import Map
from mppi import MPPI
from plot import Plotter
import numpy as np

if __name__ == "__main__":
    size = 100
    map = Map(size, size)

    mppi = MPPI()
    n_traj = 100
    steer_degrees = 10
    throttle = 15
    steer_var = 30
    throttle_var = 0.1
    controls = mppi.controls(n_traj, steer_degrees, throttle, steer_var, throttle_var)
    states = mppi.possible_states(controls, mppi.states[-1])


    paths = np.array([[mppi.states[0][:2], state[:2]] for state in states])
    # print(paths)
    # [mppi.states[0]


    plotter = Plotter()


    plotter.world(map.grid, paths)
