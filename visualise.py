import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_cytoscape as cyto
cyto.load_extra_layouts()

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
                        value="cose",
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
                        value=[0, 10]
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
                        value=[0, 10]
                    )
                ])
            ])
        ])
    ]),
    html.Div(className = 'mg-t-20', children = [
        html.Div(className = 'row', children = [
            html.Div(className = 'col-lg-6', children = [
                html.H3("Overall"),
                html.Div(className = 'bar-chart-wp', children = [
                    cyto.Cytoscape(
                        id='cyto-network',
                        layout={'name': 'cose'},
                        style={'width': '100%', 'height': '55vh'},
                        elements = charts.plot_cyto_graph(),
                        stylesheet=[
                            {
                                'selector': 'edge',
                                'style': {
                                    'width': 'data(weight)'
                                }
                            },
                            {
                                'selector': 'node',
                                'style': {
                                    'label': 'data(id)'
                                }
                            }
                        ]
                    )
                ]),
            ]),
            html.Div(className = 'col-lg-6', children = [
                html.Div(className = "row", children = [
                    html.Div(className = 'col-lg-8', children = [
                        html.H3("Cliques")
                    ]),
                    html.Div(className = 'col-lg-4', children = [
                        dcc.Slider(
                            id = 'nclique_filter',
                            min = 0,
                            max = 3,
                            marks = helpers.generate_range_values(helpers.clique_sizes()),
                            value = 1
                        )
                    ])
                ]),
                html.Div(className = 'bar-chart-wp', children = [
                    cyto.Cytoscape(
                        id='cyto-clique-network',
                        layout={'name': 'cose'},
                        style={'width': '100%', 'height': '30vh'},
                        elements = charts.plot_cyto_nclique_graph(),
                        stylesheet=[
                            {
                                'selector': 'edge',
                                'style': {
                                    'width': 'data(weight)'
                                }
                            },
                            {
                                'selector': 'node',
                                'style': {
                                    'label': 'data(id)'
                                }
                            }
                        ]
                    )
                ]),
                html.Div(className = 'mg-t-20', children = [
                    html.H3("Egos"),
                    html.Div(className = "row", children = [
                        html.Div(className = 'col-lg-4', children = [
                            html.Div(className = 'bar-chart-wp', children = [
                                cyto.Cytoscape(
                                    id='cyto-ego-network-1',
                                    layout={'name': 'cose'},
                                    style={'width': '100%', 'height': '20vh'},
                                    elements = [],
                                    stylesheet=[
                                        {
                                            'selector': 'edge',
                                            'style': {
                                                'width': 'data(weight)'
                                            }
                                        },
                                        {
                                            'selector': 'node',
                                            'style': {
                                                'label': 'data(id)'
                                            }
                                        }
                                    ]
                                )
                            ])
                        ]),
                        html.Div(className = 'col-lg-4', children = [
                            html.Div(className = 'bar-chart-wp', children = [
                                cyto.Cytoscape(
                                    id='cyto-ego-network-2',
                                    layout={'name': 'cose'},
                                    style={'width': '100%', 'height': '20vh'},
                                    elements = [],
                                    stylesheet=[
                                        {
                                            'selector': 'edge',
                                            'style': {
                                                'width': 'data(weight)'
                                            }
                                        },
                                        {
                                            'selector': 'node',
                                            'style': {
                                                'label': 'data(id)'
                                            }
                                        }
                                    ]
                                )
                            ])
                        ]),
                        html.Div(className = 'col-lg-4', children = [
                            html.Div(className = 'bar-chart-wp', children = [
                                cyto.Cytoscape(
                                    id='cyto-ego-network-3',
                                    layout={'name': 'cose'},
                                    style={'width': '100%', 'height': '20vh'},
                                    elements = [],
                                    stylesheet=[
                                        {
                                            'selector': 'edge',
                                            'style': {
                                                'width': 'data(weight)'
                                            }
                                        },
                                        {
                                            'selector': 'node',
                                            'style': {
                                                'label': 'data(id)'
                                            }
                                        }
                                    ]
                                )
                            ])
                        ])
                    ])
                ])
            ])
        ])
    ])
]

@app.callback(
    [Output("cyto-network", "elements"),
    Output("cyto-clique-network", "elements"),
    Output("cyto-ego-network-1", "elements"),
    Output("cyto-ego-network-2", "elements"),
    Output("cyto-ego-network-3", "elements")],
    [Input("genre_filter", "value"),
    Input("rating_filter", "value"),
    Input("sales_rank_filter", "value"),
    Input("reviews_filter", "value"),
    Input("page_filter", "value"),
    Input("price_filter", "value"),
    Input("nclique_filter", "value")],
)
def update_network_graphs(genre_filter, rating_filter, sales_rank_filter, reviews_filter, page_filter, price_filter, nclique_filter):
    return [
        charts.plot_cyto_graph(params = locals()),
        charts.plot_cyto_nclique_graph(params = locals()),
        *charts.plot_cyto_ego_graphs(params = locals())
        ]

@app.callback(
    [Output("cyto-network", "layout"),
    Output("cyto-clique-network", "layout"),
    Output("cyto-ego-network-1", "layout"),
    Output("cyto-ego-network-2", "layout"),
    Output("cyto-ego-network-3", "layout")],
    [Input("chart_type_option", "value")]
)
def update_graph_layout(chart_type_option):
    layout = {"name" : chart_type_option}
    return [layout] * 5