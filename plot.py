import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go


class Plotter:

    def __init__(self):
        pass

    def world(self, grid, paths=None):

        size = grid.shape[0]
        # Coordinates for the axes (e.g., -5 to 5 if size = 11)
        half = size // 2
        x = np.arange(-half, half)
        y = np.arange(-half, half)

        # ================ .png =================

        # Plot
        fig, ax = plt.subplots()
        cax = ax.imshow(grid, cmap='Reds', vmin=0, vmax = 1, interpolation='nearest', origin='lower') # binary, greys, Reds, 

        # Set custom ticks to reflect centered (0,0)
        step = grid.shape[0] // 5
        xticks = np.arange(0, size, step)
        yticks = np.arange(0, size, step)
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)
        ax.set_xticklabels(x[xticks])
        ax.set_yticklabels(y[yticks])

        if paths is not None:
            # Transform from world coordinates to grid indices
            # Add half to shift from centered to grid indexing
            # for path in paths:
            for path in paths:
                grid_points_x = [p[0] + half for p in path]
                grid_points_y = [p[1] + half for p in path]
                ax.plot(grid_points_x, grid_points_y, linewidth = 2, zorder=1) # , c='red', s=30, edgecolors='black'
                ax.scatter(grid_points_x, grid_points_y, edgecolors='black', s=20, zorder =2)


        # Clean up
        ax.set_title('Traversability Map')
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        plt.colorbar(cax, label='Cost')

        plt.savefig("plots/grid.png")


        # =========== .html ===================

        # Flip grid to match origin='lower' behavior
        flipped_grid = np.flipud(grid)

        fig_p = go.Figure()

        fig_p.add_trace(go.Heatmap(
            z=flipped_grid,
            colorscale='Reds',
            zmin=0,
            zmax=1,
            showscale=True,
            colorbar=dict(title='Cost')
        ))

        if paths is not None:
            for path in paths:
                plot_x = [p[0] + half for p in path]
                plot_y = [size - 1 - (p[1] + half) for p in path]  # flip y to match imshow origin
                fig_p.add_trace(go.Scatter(
                    x=plot_x,
                    y=plot_y,
                    mode='lines+markers',
                    line=dict(color='black', width=2),
                    marker=dict(size=6, color='white', line=dict(color='black', width=1)),
                    name='Path'
                ))

        fig_p.update_layout(
            title='Traversability Map (Interactive)',
            xaxis_title='X',
            yaxis_title='Y',
            xaxis=dict(
                tickmode='array',
                tickvals=np.arange(0, size, step),
                ticktext=x[::step].tolist(),
                scaleanchor="y",
                constrain="domain"
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=np.arange(0, size, step),
                ticktext=np.flip(y[::step]).tolist()
            ),
            autosize=False,
            width=700,
            height=700
        )
        # import webbrowser
        # webbrowser.open("plots/grid_interactive.html")
        # fig_p.write_html("plots/grid_interactive.html")
        # fig_p.show()




        