import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import charts
import helpers
from app import app

content = [
    html.H1("Visualise"),
    html.Div(className = 'mg-tb-40', children = [
        html.Div(className = 'row', children = [
            html.Div(className = 'col-lg-3', children = [
                html.Div(className = 'bar-chart-wp', children = [
                    html.B("Chart Layout"),
                    dcc.Dropdown(
                        id="chart_type_option",
                        options=helpers.network_layout_options(),
                        value="spring",
                        clearable = False
                    )
                ])
            ])
        ])
    ]),
    html.Div(className = 'row', children = [
        html.Div(className = 'col-lg-12', children = [
            html.Div(className = 'bar-chart-wp', children = [ 
                charts.include_loader(dcc.Graph(
                    id = 'network',
                    figure = charts.plot_graph(),
                    config = {"displayModeBar" : False},
                    style = {'height' : '60vh'}
                ))
            ])
        ])
    ])
]

@app.callback(
    Output("network", "figure"),
    [Input("chart_type_option", "value")],
)
def update_network_graph(chart_type_option):
    fig = charts.plot_graph(params = locals())
    return fig