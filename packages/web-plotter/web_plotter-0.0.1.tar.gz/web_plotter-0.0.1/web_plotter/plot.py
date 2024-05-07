import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

class PlotsHandler:
    def __init__(self, plots, initial_view=0, initial_shape=(2, 3)):
        self.setPlots(plots)
        self._current_view = initial_view
        self._current_shape = initial_shape
    
    def setPlots(self, plots):
        self._plots = plots
        self._titles = [plot.layout.title.text for plot in plots]
        self._length = len(self._plots)

    @property
    def titles(self):
        return self._titles

    @property
    def length(self):
        return self._length

    @property
    def plots_list(self):
        return [plot.to_json() for plot in self._plots]

    @property
    def num_views(self):
        return int(np.ceil(self._length / (self.current_shape[0] * self.current_shape[1])))

    @property
    def current_view(self):
        return self._current_view
    
    @current_view.setter
    def current_view(self, val):
        self._current_view = val

    @property
    def current_shape(self):
        return self._current_shape
    
    @current_shape.setter
    def current_shape(self, val):
        self._current_shape = val

class PlotsMatrixHandler:
    def __init__(self, plots):
        self._plots = plots
        self._titles = [plot.layout.title.text for plot in plots]
        self._length = len(plots)
        self._current_view = 0
        self.reshape(2, 3)

    def setView(self, new_view):
        self._current_view = max(min(self._num_views - 1, new_view), 0)
        
    def reshape(self, rows, columns):
        self._shape = (rows, columns)
        self._matrix_plots = []
        
        self._num_views = int(np.ceil(self._length / (rows * columns)))
        
        for view in range(self._num_views):
            matrix = []
            for i in range(rows):
                row = []
                for j in range(columns):
                    position = view * columns * rows + i * columns + j
                    if self._length > position:
                        row.append(self._plots[position].to_json())
                    else:
                        row.append([])
                matrix.append(row)
            self._matrix_plots.append(matrix)
        self.setView(self._current_view)

    def resetColorscheme(self, colorscheme):
        template = pio.templates[colorscheme]
        for plot in self._plots:
            plot.layout.template = template
        self.reshape(*self._shape)

    def resetColorschemeDefault(self):
        self.resetColorscheme(pio.templates.default)
    
    @property
    def plots_per_view(self):
        return self._shape[0] * self._shape[1]

    @property
    def titles(self):
        return self._titles
    
    @property
    def matrix_plots(self):
        return self._matrix_plots[self._current_view]
    
    @property
    def num_views(self):
        return self._num_views

    @property
    def length(self):
        return self._length

    @property
    def current_view(self):
        return self._current_view

    @current_view.setter
    def current_view(self, new_view):
        self.setView(new_view)

    @property
    def shape(self):
        return self._shape


def generate_plots_matrix(n, m):
    plots_matrix = []
    for i in range(n):
        row = []
        for j in range(m):
            x_values = np.arange(start=0, stop=10, step = 2)
            y_values = x_values * j + i

            # Create trace
            trace = go.Scatter(
                x=x_values,
                y=y_values,
                mode='markers'
            )

            # Create layout
            layout = go.Layout(
                title=f'2D Plot {i} {j}',
                xaxis=dict(title='X-axis'),
                yaxis=dict(title='Y-axis')
            )

            # Create figure
            fig = go.Figure(data=[trace], layout=layout)
            
            # fig.update_layout(
            #         margin={'t':25,'l':25,'b':25,'r':25}
            #     )

            # Convert Plotly figure to JSON
            # plot_json = fig.to_json()
            row.append(fig)
        plots_matrix.append(row)
    return plots_matrix

def generateScatterPlot3D():
    np.random.seed(0)
    x = np.random.uniform(-1, 1, size=1000)
    y = np.random.uniform(-1, 1, size=1000)
    z = np.random.uniform(-1, 1, size=1000)

    # Create 3D scatter plot
    scatter_plot = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=8,
            color=z,                # set color to z axis
            colorscale='Viridis',   # choose a colorscale
            opacity=0.8
        )
    )

    # Create layout
    layout = go.Layout(
        title='3D Scatter Plot',
        scene=dict(
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            zaxis=dict(title='Z')
        ),
    )

    # Create Figure
    fig = go.Figure(data=[scatter_plot], layout=layout)

    return fig
    # Convert the plot to JSON and pass it to the template
    # plot_json = fig.to_json()
    # return plot_json
