from app import app

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import charts
import helpers

# Generate Plotly content
content = html.Section(
    children = [
        html.Div([
            html.H2("Network Analysis at a glance...", className="align-center"),
            html.Div([
                dcc.Dropdown(
                    id="corr_dir",
                    options=[{"label": "Positive", "value": "Positive"}, {"label": "Negative", "value": "Negative"}],
                    value=""
                )
            ]),
            html.Div(id="corr_network"),
            html.Div([
                dcc.Input(id="ego_network_count", type="text", value="0", placeholder="Top-N Ego-networks"),
            ], style = {
                "textAlign": "center" 
            }),
            html.Div(id="ego_network")
        ])
    ]
)
@app.callback(
    Output("ego_network", "children"),
    [
        Input("ego_network_count", "value")
    ],
)
def update_ego_network(ego_network_count):
    # To prevent callback error
    if ego_network_count == "":
        ego_network_count = 0

    ego_network_count = int(ego_network_count)
    ego_networks = charts.generate_ego_network(ego_network_count)

    children = [
        dcc.Graph(
            id = f'ego_network_{i}',
            figure = ego_networks[i],
            config = {"displayModeBar" : False}
        ) for i in range(len(ego_networks))
    ]
    return children

@app.callback(
    Output("corr_network", "children"),
    [
        Input("corr_dir", "value")
    ],
)
def update_corr_network(corr_dir):
    # To prevent callback error
    if corr_dir == "":
        corr_dir = "Positive"
    
    children=[
        dcc.Graph(
            id = 'corr_network_1',
            figure = charts.generate_correlation_network(corr_dir),
            config = {"displayModeBar" : False}
        )
    ]
    return children