from map import Map
from mppi import MPPI
from plot import Plotter
import numpy as np
import os
import time

if __name__ == "__main__":
    # PARAMS
    size = 200
    STOCHASTIC_CONTROLS = False
    horizon = 10
    steer_degrees = 0
    throttle = 2
    steer_var = 30
    throttle_var = 0.1
    num_traj = 10
    sim_steps =5
    n_obstacles = 30
    # Classes
    map = Map(size, size, num_obstacles=n_obstacles)
    mppi = MPPI()
    plotter = Plotter()

    grid = map.obstacle_grid


    # Controls and Trajectories
    
    for i in range(sim_steps):
        if STOCHASTIC_CONTROLS:
            controls = [mppi.controls_stochastic(horizon, steer_degrees, throttle, steer_var, throttle_var) for i in range(num_traj)]
        else:
            step = 2*steer_var // num_traj
            start = -steer_var
            stop = steer_var + step
            controls = [mppi.controls_deterministic(horizon, steer, throttle) for steer in range(start, stop, step)]
        trajectories = [mppi.generate_trajectories(control, mppi.states[-1]) for control in controls ]

        trajectory_costs = mppi.cost_function(grid, trajectories)

        print(trajectory_costs)
        # print(trajectories[np.argmin(trajectory_costs)])
        # Plots
        # # plotter.world(map.random_grid, [trajectories])
        plotter.world(grid, trajectories)
        # plotter.world(map.elevation_grid, trajectories)
        # plotter.world(map.mountain_grid, trajectories)
        # plotter.world(map.terrain_grid, trajectories)

        prev_state = trajectories[np.argmin(trajectory_costs)][-1]
        mppi.states.append(prev_state)
        time.sleep(.1)
    # Plot one more time
    trajectories = [mppi.generate_trajectories(control, mppi.states[-1]) for control in controls ]
    trajectory_costs = mppi.cost_function(grid, trajectories)
    plotter.world(grid, trajectories)

    print(np.array(mppi.states))
    print(map.wall_grid[:,163])
    print(map.wall_grid[163, 99])


    os.makedirs("txt_files", exist_ok=True)
    np.savetxt("txt_files/grid.txt",map.wall_grid ,fmt="%.2f")
    np.savetxt("txt_files/example_traj.txt", trajectories[0], fmt= "%.2f")