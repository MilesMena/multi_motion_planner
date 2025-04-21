import numpy as np
np.set_printoptions(precision=3, suppress=True, floatmode='fixed')




class MPPI():
    def __init__(self):
        np.random.seed(None)
        self.states = [[0,0,0,0]] # x, y, velocity, heading
       
    def controls(self,horizon, nominal_steering_degrees, nominal_throttle, steering_variance_degrees, throtle_variance):
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
