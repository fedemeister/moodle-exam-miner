import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import scripts.graph_functions.functions_for_clusters as functions_for_clusters
import web.graph_scatter_plot
import web.graph_fig_estudiantes

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Hello world'),
    ])
])


if __name__ == '__main__':
    app.run_server()