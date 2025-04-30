from map import Map
from mppi import MPPI
from plot import Plotter
from robot import Robot
import numpy as np
import os
import time

if __name__ == "__main__":
    # PARAMS
    size = 200
    STOCHASTIC_CONTROLS = False
    horizon = 10
    steer_degrees = -20 # positive turns left (ego view)
    throttle = 2
    steer_var = 30
    throttle_var = 0.1
    num_traj = 10
    sim_steps = 5
    n_obstacles = 30
    # Classes
    map = Map(size, size, num_obstacles=n_obstacles)
    mppi = MPPI()
    grid = map.track_grid
    r1 = Robot([0,0,0,0], grid)
    r2 = Robot([10,0, 0,0], grid)
    mppi_2 = MPPI([10,10,0,5])

    plotter = Plotter()


    # Controls -> if stochastic we should put in the for loop, but for now it doesn't change
    controls = mppi.controls(horizon, steer_degrees, throttle, steer_var, throttle_var, STOCHASTIC_CONTROLS,num_traj)
    for i in range(sim_steps):    
        r1_traj = [mppi.generate_trajectories(c, r1.states[-1]) for c in controls ]
        r2_traj = [mppi.generate_trajectories(c, r2.states[-1]) for c in controls ]

        r1_costs = mppi.cost_function(grid, r1_traj)
        r2_costs = mppi.cost_function(grid, r2_traj)

        plotter.world(grid, [r1_traj, r2_traj])
        
        r1.states.append(r1_traj[np.argmin(r1_costs)][-1])
        r2.states.append(r2_traj[np.argmin(r2_costs)][-1])

        time.sleep(.3)
        # plotter.world_3d(grid)
    # Plot one more time
    # trajectories = [mppi_1.generate_trajectories(control, mppi_1.states[-1]) for control in controls ]
    # trajectory_costs = mppi_1.cost_function(grid, trajectories)
    # plotter.world(grid, trajectories)

    # print(np.array(mppi_1.states))
    # print(map.wall_grid[:,163])
    # print(map.wall_grid[163, 99])


    # os.makedirs("txt_files", exist_ok=True)
    # np.savetxt("txt_files/grid.txt",map.wall_grid ,fmt="%.2f")
    # np.savetxt("txt_files/example_traj.txt", trajectories[0], fmt= "%.2f")