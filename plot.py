import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go



class Plotter:

    def __init__(self):
        pass

    def world(self, grid, robot_paths=None, SAVE=True, custom_tick=False):

        size = grid.shape[0]
        # Coordinates for the axes (e.g., -5 to 5 if size = 11)
        half = size // 2
        x = np.arange(-half, half)
        y = np.arange(-half, half)

        # ================ .png =================

        # Plot
        fig, ax = plt.subplots()
        cax = ax.imshow(grid, cmap='Reds', vmin=0, vmax = 1, interpolation='nearest') # binary, greys, Reds, 

        # Set custom ticks to reflect centered (0,0)
        if custom_tick:
            step = grid.shape[0] // 5
            xticks = np.arange(0, size, step)
            yticks = np.arange(0, size, step)
            ax.set_xticks(xticks)
            ax.set_yticks(yticks)
            ax.set_xticklabels(x[xticks])
            ax.set_yticklabels(y[yticks][::-1])


        if robot_paths is not None:
            # Transform from world coordinates to grid indices
            # Add half to shift from centered to grid indexing
            # for path in paths:
            for robot_path in robot_paths:
                for path in robot_path:
                    grid_points_x = [p[0] + half for p in path]
                    grid_points_y = [p[1] + half for p in path]
                    # print(grid_points_x)
                    # print(grid_points_y)
                    ax.plot(grid_points_x, grid_points_y, linewidth = 1, zorder=1) # , c='red', s=30, edgecolors='black'
                    ax.scatter(grid_points_x, grid_points_y,  s=1, zorder =2) #edgecolors='black',


        # Clean up
        ax.set_title('Traversability Map')
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        plt.colorbar(cax, label='Cost')

        if SAVE:
            plt.savefig("plots/grid.png")


        # =========== .html ===================

        # Flip grid to match origin='lower' behavior
        # flipped_grid = np.flipud(grid)

        # fig_p = go.Figure()

        # fig_p.add_trace(go.Heatmap(
        #     z=flipped_grid,
        #     colorscale='Reds',
        #     zmin=0,
        #     zmax=1,
        #     showscale=True,
        #     colorbar=dict(title='Cost')
        # ))

        # if paths is not None:
        #     for path in paths:
        #         plot_x = [p[0] + half for p in path]
        #         plot_y = [size - 1 - (p[1] + half) for p in path]  # flip y to match imshow origin
        #         fig_p.add_trace(go.Scatter(
        #             x=plot_x,
        #             y=plot_y,
        #             mode='lines+markers',
        #             line=dict(color='black', width=2),
        #             marker=dict(size=6, color='white', line=dict(color='black', width=1)),
        #             name='Path'
        #         ))

        # fig_p.update_layout(
        #     title='Traversability Map (Interactive)',
        #     xaxis_title='X',
        #     yaxis_title='Y',
        #     xaxis=dict(
        #         tickmode='array',
        #         tickvals=np.arange(0, size, step),
        #         ticktext=x[::step].tolist(),
        #         scaleanchor="y",
        #         constrain="domain"
        #     ),
        #     yaxis=dict(
        #         tickmode='array',
        #         tickvals=np.arange(0, size, step),
        #         ticktext=np.flip(y[::step]).tolist()
        #     ),
        #     autosize=False,
        #     width=700,
        #     height=700
        # )
        # import webbrowser
        # webbrowser.open("plots/grid_interactive.html")
        # fig_p.write_html("plots/grid_interactive.html")
        # fig_p.show()


    def world_3d(self, grid, robot_paths=None, SAVE=True, custom_tick=False):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Get grid dimensions
        rows, cols = grid.shape

        # Create x, y coordinates for bars
        _x = np.arange(cols)
        _y = np.arange(rows)
        _xx, _yy = np.meshgrid(_x, _y)
        x, y = _xx.ravel(), _yy.ravel()

        # Height of bars is grid value (0 or 1)
        z = np.zeros_like(x)
        dz = grid.ravel()

        # Set bar width
        dx = dy = 1

        # Plot bars
        ax.bar3d(x, y, z, dx, dy, dz, color='skyblue', edgecolor='black')

        # Optional: add labels or adjust viewing angle
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Value')
        ax.view_init(elev=30, azim=135)  # Adjust view angle

        plt.show()



if __name__ == "__main__":
    plotter = Plotter()
    plotter.world_3d("grid")
        