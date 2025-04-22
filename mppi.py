import numpy as np
np.set_printoptions(precision=3, suppress=True, floatmode='fixed')




class MPPI():
    def __init__(self):
        np.random.seed(None)
        self.states = [[0,0,0,0]] # x, y, velocity, heading

    def controls_deterministic(self, horizon, nom_steer_deg, nom_throt):
        steering = np.radians(np.full((horizon,1), nom_steer_deg))
        throttle = np.full((horizon,1), nom_throt)
        return np.hstack((steering, throttle))
       
    def controls_stochastic(self,horizon, nominal_steering_degrees, nominal_throttle, steering_variance_degrees, throtle_variance):
        nominal_control = np.array([np.radians(nominal_steering_degrees), nominal_throttle])
        steering = np.radians(np.random.normal(0, steering_variance_degrees, (horizon,1)))
        throttle = np.random.normal(0,throtle_variance, (horizon,1))
        noise = np.hstack((steering, throttle))
        return nominal_control + noise
    
    def generate_trajectories(self,controls, prev_state):
        trajectory = [prev_state]
        for control in controls:
            x,y,velocity, heading = trajectory[-1]
            x += control[1] * np.sin(control[0] + heading)
            y += control[1] * np.cos(control[0] + heading)
            heading += control[0]
            trajectory.append([x,y,control[1], heading])
        return np.array(trajectory)
    

    def cost_function(self, grid, trajectories):
        weight_heading = 1
        weight_obstacles = 10
        costs = []
        size = grid.shape[0]
        half = size // 2

        for path in trajectories:
            cost = 0
            grid_points_x = [p[0] + half for p in path]
            grid_points_y = [p[1] + half for p in path]
            # print(grid_points_y)

            # Interpolate between each pair of points
            interp_x = np.concatenate([
                np.linspace(grid_points_x[i], grid_points_x[i+1], 5)
                for i in range(len(grid_points_x) - 1)
            ])
            interp_y = np.concatenate([
                np.linspace(grid_points_y[i], grid_points_y[i+1], 5)
                for i in range(len(grid_points_y) - 1)
            ])

            # Convert to integer grid indices (and clip to grid bounds)
            # h, w = grid.shape
            # indices = set()
            # for x, y in zip(interp_x, interp_y):
            #     xi, yi = int(round(x)), int(round(y))
            #     xi = np.clip(xi, 0, h - 1)
            #     yi = np.clip(yi, 0, w - 1)
            #     indices.add((xi, yi))

            # Check for any non-zero cell in grid along the path
            collision = int(any(grid[int(y), int(x)] > 0 for x, y in zip(grid_points_x,grid_points_y)))
            print(collision)

            heading_change = np.abs(path[:-1, 3] - path[1:, 3])
            cost += (weight_obstacles * collision) + (weight_heading * np.sum(heading_change))
            costs.append(cost)

        return np.array(costs)


        

    
    def possible_states(self, controls, prev_state):
        pos_states = []
        pose = prev_state
        for control in controls:
            x,y,velocity, heading = pose
            x += control[1] * np.sin(control[0] + heading)
            y += control[1] * np.cos(control[0] + heading)
            heading += control[0]
            pos_states.append([x,y,control[1], heading])
        return np.array(pos_states)


if __name__ == "__main__":

    mppi = MPPI()
    n_traj = 20
    steer_degrees = 10
    throttle = 1
    steer_var = 10
    throttle_var = 0.1
    controls = mppi.controls(n_traj, steer_degrees, throttle, steer_var, throttle_var)
    print(controls)
    states = mppi.possible_states(controls, mppi.states[-1])
    print(states)
    trajectory = mppi.generate_trajectories(controls, mppi.states[-1])
    print(trajectory)


    


# init_state = self.states[-1]
        # num_steps = len(controls)
        # pos_states = np.zeros((num_steps, len(self.states[0])))
        # pos_states[0] = init_state
        # for t in range(1,num_steps):
        #     x,y,velocity, heading = pos_states[t -1]
        #     # Get the current control (steering, throttle)
        #     control_steering, control_throttle = controls[t]
        #     # Update x, y, and heading based on control
        #     pos_states[t, 0] = x + control_throttle * np.sin(control_steering + heading)  # x
        #     pos_states[t, 1] = y + control_throttle * np.cos(control_steering + heading)  # y
        #     pos_states[t, 2] = control_throttle  # velocity

                #     pos_states[t, 3] = (heading + control_steering) % (2*np.pi)   # heading
