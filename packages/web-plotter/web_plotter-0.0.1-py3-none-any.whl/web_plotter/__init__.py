from flask import Flask, render_template, jsonify, request
import json
import plotly.io as pio
from plotly_gruvbox_colorscheme import experimental
pio.templates.default = experimental
from web_plotter.fuzzy import RootNode, TerminalNode, ChoiceNode, CurrentNodeHandler
from web_plotter.plot import PlotsMatrixHandler, generate_plots_matrix, generateScatterPlot3D, PlotsHandler
from web_plotter.helper import findPermutations

app = Flask(__name__)


## plot matrix api
plots_handler = PlotsHandler([])

@app.route('/grid-plotter-data')
def gridPlotterData():
    return jsonify({"plots_list": plots_handler.plots_list})

@app.route('/colorscheme-data')
def colorSchemeData():
    template = pio.templates[pio.templates.default]
    # background_color = template.layout.paper_bgcolor
    # font_color = template.layout.font.color
        # template.to_json()
    return jsonify({"template": template.to_plotly_json()})
    # return jsonify({"colorscheme_data": {"background_color": background_color, "font_color": font_color}})

@app.route('/set-current-view-data', methods=['POST'])
def setCurrentViewData():
    plots_handler.current_view = request.form['query']
    return ''

@app.route('/current-view-data')
def currentViewData():
    return jsonify(plots_handler.current_view)

@app.route('/set-current-shape-data', methods=['POST'])
def setShapeData():
    plots_handler.current_shape = tuple(json.loads(request.form['query']))
    return ''

@app.route('/current-shape-data')
def shapeData():
    return jsonify(plots_handler.current_shape)

# change_current_view_options = {
#         "+1": lambda: plots_matrix_handler.setView(plots_matrix_handler.current_view + 1),
#         "-1": lambda: plots_matrix_handler.setView(plots_matrix_handler.current_view - 1),
#         **{
#             f"{i}": lambda i=i: plots_matrix_handler.setView(i) for i in range(10)
#             }
#         }

# @app.route('/change-current-view', methods=['POST'])
# def changeCurrentView():
#     query = request.form['query']
#     previous_view = plots_matrix_handler.current_view
#     option = change_current_view_options.get(query)
#     if option:
#         option()
#     else:
#         print(f"invalid query: {query}")
#     update_plot = str(previous_view != plots_matrix_handler.current_view)
#     return update_plot

@app.route('/grid-plotter/')
def gridPlotter():
    return render_template('grid_plotter.html')

## fuzzy finding nodes

root_node = RootNode()

change_grid_node = ChoiceNode(
        lambda: f"reshape grid {plots_handler.current_shape}",
        "open virtual window",
        execute_backend_callback=lambda self: self.setKids((
            TerminalNode(
                root_node,
                f"{i},{j}",
                ["reshape grid", [i, j]],
                ) for i, j in findPermutations(min(9, plots_handler.length))
            )),
        root_node = root_node
        )

change_view_node = ChoiceNode(
        lambda: f"change view ({plots_handler.current_view})",
        "open virtual window",
        execute_backend_callback=lambda self: self.setKids((
            TerminalNode(root_node,
                         f"{i}",
                         ["change view", i],
                         ) for i in range(plots_handler.num_views)
            )),
        root_node = root_node
        )

switch_plot_title_node = ChoiceNode(
        "switch to plot/title",
        "open virtual window",
        execute_backend_callback=lambda self: self.setKids((
            TerminalNode(root_node,
                         f"{name}",
                         ["change view", i // (plots_handler.current_shape[0] * plots_handler.current_shape[1])],
                        ) for i, name in enumerate(plots_handler.titles)
            )),
        root_node = root_node
        )

def plotlySetDefaultTemplate(default_template):
    pio.templates.default = default_template
    # plots_handler.resetColorschemeDefault()

change_colorscheme_node = ChoiceNode(
        lambda: f"change colour scheme ({pio.templates.default})",
        "open virtual window",
        execute_backend_callback=lambda self:self.setKids((
            TerminalNode(root_node,
                         i,
                         "update colorscheme",
                         execute_backend_callback=lambda i=i: plotlySetDefaultTemplate(i)
                         ) for i in pio.templates
            )),
        root_node = root_node
        )

root_node.addKids((
    TerminalNode(root_node, "close virtual window", "close virtual window"),
    # TerminalNode(root_node, "open virtual window", "open virtual window"),
    change_grid_node,
    change_view_node,
    change_colorscheme_node,
    switch_plot_title_node,
    ))

current_node_handler = CurrentNodeHandler(root_node)

## api for fuzzy finding

@app.route('/string-to-fuzzy', methods=['GET'])
def stringToFuzzy():
    current_node = current_node_handler.get()
    return jsonify(current_node.kids)

@app.route('/fuzzy-selected', methods=['POST'])
def fuzzySelected():
    str_chosen_node = request.form['query']
    current_node = current_node_handler.get()
    chosen_node = current_node.getChosenNode(str_chosen_node)
    chosen_node.executeBackend()
    next_node = chosen_node.transition()
    current_node_handler.assign(next_node)
    return chosen_node.updateFrontEnd()


## merely to test only the fuzzy finder
@app.route('/')
def index():
    return render_template('file_reader_example.html')

# if __name__ == '__main__':
#     app.run(debug=True)
