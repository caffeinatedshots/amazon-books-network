import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import charts
import helpers
from app import app

content = [
    html.H1("Visualise"),
    html.Div(className = 'mg-t-20', children = [
        html.Div(className = 'row', children = [
            html.Div(className = 'col-lg-3'),
            html.Div(className = 'col-lg-6', children = [
                html.Div(className = 'bar-chart-wp', children = [
                    html.B("Chart Layout"),
                    dcc.Dropdown(
                        id="chart_type_option",
                        options=helpers.network_layout_options(),
                        value="spring",
                        clearable = False
                    )
                ])
            ]),
            html.Div(className = 'col-lg-3')
        ])
    ]),
    html.Div(className = 'mg-t-20', children = [
        html.Div(className = 'row', children = [
            html.Div(className = 'col-lg-3', children = [
                html.Div(className = 'bar-chart-wp', children = [
                    html.B("Genre"),
                    dcc.Dropdown(
                        id="genre_filter",
                        options= helpers.generate_options(charts.get_unique_genres()),
                        value="spring",
                        multi = True,
                        clearable = False
                    )
                ])
            ]),
            html.Div(className = 'col-lg-3', children = [
                html.Div(className = 'bar-chart-wp', children = [
                    html.B("Sales Rank"),
                    dcc.Dropdown(
                        id="sales_rank_filter",
                        options=helpers.generate_options(charts.get_sales_rank_categories()),
                        value="spring",
                        multi = True,
                        clearable = False,
                    )
                ])
            ]),
            html.Div(className = 'col-lg-3', children = [
                html.Div(className = 'bar-chart-wp', children = [
                    html.B("Average Rating"),
                    dcc.Dropdown(
                        id="rating_filter",
                        options=helpers.generate_options(charts.get_unique_ratings()),
                        value="4.5",
                        multi = True,
                        clearable = False
                    )
                ])
            ]),
            html.Div(className = 'col-lg-3', children = [
                html.Div(className = 'bar-chart-wp', children = [
                    html.B("No. of Reviews"),
                    dcc.Dropdown(
                        id="reviews_filter",
                        options=helpers.generate_options(charts.get_review_categories()),
                        value="spring",
                        multi = True,
                        clearable = False
                    )
                ])
            ])
        ])
    ]),
    html.Div(className = 'mg-t-20', children = [
        html.Div(className = 'row', children = [
            html.Div(className = 'col-lg-6', children = [
                html.Div(className = 'bar-chart-wp', children = [
                    html.B("No. of Pages"),
                    dcc.RangeSlider(
                        id = 'page_filter',
                        marks=helpers.generate_range_values(charts.get_num_pages_quantiles()),
                        min=0,
                        max=10,
                        value=[3, 7]
                    )
                ])
            ]),
            html.Div(className = 'col-lg-6', children = [
                html.Div(className = 'bar-chart-wp', children = [
                    html.B("Price"),
                    dcc.RangeSlider(
                        id = 'price_filter',
                        marks=helpers.generate_range_values(charts.get_price_quantiles()),
                        min=0,
                        max=10,
                        value=[3, 7]
                    )
                ])
            ])
        ])
    ]),
    html.Div(className = 'mg-t-20', children = [
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
    ])
]

@app.callback(
    Output("network", "figure"),
    [Input("chart_type_option", "value")],
)
def update_network_graph(chart_type_option):
    fig = charts.plot_graph(params = locals())
    return fig