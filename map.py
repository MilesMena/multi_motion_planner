import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import os


class Map():
    def __init__(self, h, w, num_obstacles=5):
        self.random_grid = np.random.rand(h,w)
        self.obstacle_grid = self.generate_obstacle_grid(h,w, num_obstacles)
        # self.elevation_grid = self.generate_elevation_grid(h,w)
        self.mountain_grid = self.generate_mountainous_grid(h,w)
        self.terrain_grid = self.generate_terrain_grid(h,w)
        self.wall_grid =  np.ones((h,w)) 
        self.track_grid = self.generate_track_grid(h,w)
        # np.vstack((
                                    
        #                             np.zeros((2*h//3,w)),
        #                             np.ones((h//3,w))
        #                             ))

        # self.semantic_grid = self.generate_semantic_grid(h,w)
    
    def generate_obstacle_grid(self, h,w,num_obstacles):
        # Make sure to not generate obstacles at the start
        base_grid = np.zeros((h,w))
        for n in range(num_obstacles):
            obs_size = np.random.randint(low=1, high=10)
            obs_center = (np.random.randint(low=0, high=h), np.random.randint(low=0, high=w))

            x, y = obs_center
            r = obs_size 

            x_min = max(x - r, 0)
            x_max = min(x + r + 1, base_grid.shape[0])
            y_min = max(y - r, 0)
            y_max = min(y + r + 1, base_grid.shape[1])

            base_grid[x_min:x_max, y_min:y_max] += 1
        return base_grid

    def generate_elevation_grid(self, h, w):
        base_grid = np.zeros((h,w))
        elev_h = 1
        elev_w = 1
        elev_area = elev_h * elev_w
        x_center = np.random.randint(low=0, high = h)
        y_center = np.random.randint(low=0, high = w)
        while elev_area <= 850: # elev_area <= 850 and h>0 and w>0:
            x_min = max(x_center-elev_area,0)
            x_max = min(x_center+elev_area + 1, base_grid.shape[0])
            y_min = max(y_center-elev_area, 0)
            y_max = min(y_center+elev_area + 1, base_grid.shape[1])

            base_grid[x_min:x_max, y_min:y_max] += 1

            x_center += int(np.random.normal(0,6))
            y_center += int(np.random.normal(0,6))

            # Generate Peaks
            # elev_h += int(np.random.normal(0,3))
            # elev_w += int(np.random.normal(0,3))
            # elev_area = elev_h * elev_w

            # Kinda works
            elev_area = int(np.random.normal(0,10) * np.random.normal(0,10))
            # elev_area += max(np.random.randint(0,elev_area) * np.random.randint(0,elev_area), 2)
            # print(x_center, y_center, elev_area, x_min,x_max, y_min,y_max)
        
            # print(base_grid / np.max(base_grid))
        return base_grid / np.max(base_grid)
    

    def generate_mountainous_grid(self, h, w, num_peaks=30, peak_height=100.0, smoothness=50.0, seed=None):
        if seed is not None:
            np.random.seed(seed)

        base_grid = np.zeros((h, w))

        for _ in range(num_peaks):
            # Choose random peak location
            x, y = np.random.randint(0, h), np.random.randint(0, w)

            # Create a peak by setting a single high value
            base_grid[x, y] += peak_height

        # Smooth the grid to spread the peaks and create realistic mountain ridges
        smoothed_grid = gaussian_filter(base_grid, sigma=smoothness)

        # Normalize to [0, 1]
        smoothed_grid = smoothed_grid / smoothed_grid.max()

        return smoothed_grid
    


    def generate_terrain_grid(self, h, w, num_peaks=5, peak_height=100.0, smoothness=53.0,
                        num_valleys=10, valley_depth=50.0, erosion_passes=20,
                        num_rivers=10, river_length=100, seed=None):
        if seed is not None:
            np.random.seed(seed)

        grid = np.zeros((h, w))

        # Add mountain peaks
        for _ in range(num_peaks):
            x, y = np.random.randint(0, h), np.random.randint(0, w)
            grid[x, y] += peak_height

        # Add valley pits (negative elevations)
        for _ in range(num_valleys):
            x, y = np.random.randint(0, h), np.random.randint(0, w)
            grid[x, y] -= valley_depth

        # Smooth terrain to make it natural
        grid = gaussian_filter(grid, sigma=smoothness)

        # Erosion simulation (low-pass filtering multiple times)
        for _ in range(erosion_passes):
            grid = gaussian_filter(grid, sigma=1)

        # Normalize before river carving
        grid -= grid.min()
        grid /= grid.max()

        # Simulate rivers (carve into elevation)
        for _ in range(num_rivers):
            x, y = np.random.randint(0, h), np.random.randint(0, w)
            for _ in range(river_length):
                grid[x, y] *= 0.7  # carve down river bed
                # move downhill (simple gradient descent)
                neighbors = [(x+dx, y+dy) for dx in [-1,0,1] for dy in [-1,0,1]
                            if 0 <= x+dx < h and 0 <= y+dy < w]
                if not neighbors:
                    break
                x, y = min(neighbors, key=lambda p: grid[p[0], p[1]])

        # Normalize again to [0, 1]
        grid -= grid.min()
        grid /= grid.max()

        return grid
    
    def generate_track_grid(self, h, w):
        block_w_ratio = 3
        radius = ((w//block_w_ratio))//2
        step = 1.0

        center_block = np.ones((h//block_w_ratio,w//block_w_ratio))
        x = np.arange(-radius, radius + step -1 , step)
        y = np.arange(0, radius + step -1 , step)  # Only top half
        X, Y = np.meshgrid(x, y)
        semi = np.ones_like(X)
        # Mask out values outside the semi-circle
        mask = X**2 + Y**2 > radius**2
        semi[mask] = 0
        semi_padding_h = (h//block_w_ratio)//4
        semi_padding_w = X.shape[1]
        semi_padding = np.zeros((semi_padding_h,semi_padding_w))
        # semi_padding = np.vstack((np.zeros((semi_padding_h,semi_padding_w)), np.ones((semi_padding_h, semi_padding_w))))
        print(semi_padding.shape, semi.shape)

        semi = np.vstack(( semi, semi_padding))
        # print(semi)
        # print(semi.shape,center_block.shape)
        grid = np.vstack((np.flip(semi), center_block,semi))
        zero_w = w//(4*block_w_ratio)
        zero_padding =np.zeros((grid.shape[0],zero_w))
        # print(padding.shape, grid.shape)
        grid = np.hstack((zero_padding, grid, zero_padding))
        wall_padding = np.ones((grid.shape[0], grid.shape[1]//5))
        grid = np.hstack((wall_padding, grid, wall_padding))
        print(grid.shape)

        wall_padding = np.ones((grid.shape[0]//7, grid.shape[1]))
        grid = np.vstack((wall_padding, grid,wall_padding))
        print(grid.shape)
        DEBUG = True
        if DEBUG:
            fig, ax = plt.subplots()
            cax = ax.imshow(grid, cmap='Reds', vmin=0, vmax = 1, interpolation='nearest') # binary, greys, Reds, 
            os.makedirs("plots", exist_ok=True)
            plt.savefig("plots/test_grid.png")

        return grid

