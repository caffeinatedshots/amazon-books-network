import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import charts
import helpers

from app import app

content = html.Section(
    children = [
        html.Div([
            html.H2("At a Glance", className="align-center"),
            dcc.Graph(
                id = 'sales_indicator',
                figure = charts.get_generic_insights(),
                config = {"displayModeBar" : False}
            ),
            charts.get_stats_table()
        ])
    ]
)

@app.callback(
    Output('stats_table', 'data'),
    [Input('stats_table', 'filter_query')]
)
def update_table(filter):
    filtered_df = charts.filter_stats_table(filter)
    return filtered_df.to_dict('records')