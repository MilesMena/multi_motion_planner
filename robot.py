class Robot():
    def __init__(self, init_state, grid):
        self.states = [self.init_state_no_collision(init_state, grid)]

    def init_state_no_collision(self, init_state, grid):
        x,y = init_state[0], init_state[1]
        size = grid.shape[0]
        half = size // 2
        while grid[y + half, x + half] == 1:
            x += 1
        return [int(x + init_state[0]),y,init_state[2], init_state[3]]
    