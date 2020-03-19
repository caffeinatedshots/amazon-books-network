import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import charts
from app import app

content = html.Section(
    children = [
        html.Div([
            html.H2("Genre", className="align-center"),
            dcc.Graph(
                id = 'network',
                figure = charts.plot_graph(),
                config = {"displayModeBar" : False}
            )
        ])
    ]
)