import matplotlib.pyplot as plt
import numpy as np

class Plotter:

    def __init__(self):
        pass

    def world(self, grid, paths=None):

        size = grid.shape[0]
        # Coordinates for the axes (e.g., -5 to 5 if size = 11)
        half = size // 2
        x = np.arange(-half, half)
        y = np.arange(-half, half)

        # Plot
        fig, ax = plt.subplots()
        cax = ax.imshow(grid, cmap='Reds', interpolation='nearest', origin='lower') # binary, greys, Reds, 

        # Set custom ticks to reflect centered (0,0)
        step = 20
        xticks = np.arange(0, size, step)
        yticks = np.arange(0, size, step)
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)
        ax.set_xticklabels(x[xticks])
        ax.set_yticklabels(y[yticks])

        if paths is not None:
            # Transform from world coordinates to grid indices
            # Add half to shift from centered to grid indexing
            for points in paths:
                grid_points_x = [p[0] + half for p in points]
                grid_points_y = [p[1] + half for p in points]
                ax.plot(grid_points_x, grid_points_y, linewidth = 2, zorder=1) # , c='red', s=30, edgecolors='black'
                ax.scatter(grid_points_x, grid_points_y, edgecolors='black', s=20, zorder =2)


        # Clean up
        ax.set_title('Traversability Map')
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        plt.colorbar(cax, label='Cost')

        plt.savefig("plots/grid.png")



        # Plot the grid
        # plt.imshow(grid, cmap='viridis', interpolation='nearest')
        # plt.colorbar(label='Cost')
        # plt.gca().invert_yaxis()
        # plt.title('Traversability Map')
        # plt.xlabel('Width')
        # plt.ylabel('Height')
        # plt.savefig("plots/grid.png")