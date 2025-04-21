from map import Map
from mppi import MPPI
from plot import Plotter
import numpy as np

if __name__ == "__main__":
    size = 1000
    map = Map(size, size, num_obstacles=15)

    mppi = MPPI()
    h = 10
    steer_degrees = 10
    throttle = 5
    steer_var = 30
    throttle_var = 0.1
    # controls = mppi.controls(h, steer_degrees, throttle, steer_var, throttle_var) # is there a way to shorten this?
    # states = mppi.possible_states(controls, mppi.states[-1])
    num_traj = 10

    trajectories = [mppi.generate_trajectories(mppi.controls(h, steer_degrees, throttle, steer_var, throttle_var), mppi.states[-1]) for i in range(num_traj) ]

    # paths = np.array([[mppi.states[0][:2], state[:2]] for state in states])
    # print(paths)
    # [mppi.states[0]
    # print(trajectories)

    plotter = Plotter()


    # plotter.world(map.random_grid, [trajectories])
    plotter.world(map.obstacle_grid, trajectories)
    # plotter.world(map.elevation_grid, trajectories)
    # plotter.world(map.mountain_grid, trajectories)
    # plotter.world(map.terrain_grid, trajectories)