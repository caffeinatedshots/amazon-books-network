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
                        elements = charts.plot_cyto_graph()
                    )
                ]),
                html.Br(),
                html.Div(className = 'bar-chart-wp', children = [
                    charts.include_loader(cyto.Cytoscape(
                        id='cyto-ego-network',
                        layout={'name': 'cose'},
                        style={'width': '100%', 'height': '50vh'},
                        elements = charts.plot_cyto_ego_graph()
                    )),
                ]),
            ])
        ])
    ]),
    html.Div(className = 'mg-t-20', children = [
        html.Div(className = 'row', children = [
            html.Div(className = 'col-lg-3'),
            html.Div(className = 'col-lg-6', children = [
                html.Div(className = 'bar-chart-wp', children = [
                    html.B("N-Clique Network"),
                    dcc.Dropdown(
                        id="nclique_filter",
                        options=helpers.generate_options(charts.get_nclique_options()),
                        multi = False,
                        clearable = False,
                        value=0
                    )
                ])
            ]),
            html.Div(className = 'col-lg-3')
        ])
    ]),
    html.Div(className = 'mg-t-20', children = [
        html.Div(className = 'row', children = [
            html.Div(className = 'col-lg-12', children = [
                html.Div(className = 'bar-chart-wp', children = [
                    charts.include_loader(cyto.Cytoscape(
                        id='cyto-clique-network',
                        layout={'name': 'cose'},
                        style={'width': '100%', 'height': '50vh'},
                        elements = charts.plot_cyto_nclique_graph()
                    )),
    #                 ),
    #                 # charts.include_loader(dcc.Graph(
    #                 #     id = 'network',
    #                 #     figure = charts.plot_graph(),
    #                 #     config = {"displayModeBar" : False},
    #                 #     style = {'height' : '60vh'}
    #                 # ))
    #             ])
    #         ]),
    #         html.Div(className = 'col-lg-6', children = [
    #             html.Div(className = "row", children = [
    #                 html.Div(className = 'col-lg-8', children = [
    #                     html.H3("Cliques")
    #                 ]),
    #                 html.Div(className = 'col-lg-4', children = [
    #                     dcc.Slider(
    #                         min = 0,
    #                         max = 3,
    #                         marks = helpers.generate_range_values([2,3,4,5]),
    #                         value = 1
    #                     )
    #                 ])
    #             ]),
    #             html.Div(className = 'bar-chart-wp', children = [
    #                 cyto.Cytoscape(
    #                     id='cyto-network-1',
    #                     layout={'name': 'cose'},
    #                     style={'width': '100%', 'height': '30vh'},
    #                     elements = []
    #                 ),
    #                 # charts.include_loader(dcc.Graph(
    #                 #     id = 'network',
    #                 #     figure = charts.plot_graph(),
    #                 #     config = {"displayModeBar" : False},
    #                 #     style = {'height' : '60vh'}
    #                 # ))
    #             ]),
    #             html.Div(className = 'mg-t-20', children = [
    #                 html.H3("Egos"),
    #                 html.Div(className = "row", children = [
    #                     html.Div(className = 'col-lg-4', children = [
    #                         html.Div(className = 'bar-chart-wp', children = [
    #                             cyto.Cytoscape(
    #                                 id='cyto-network-1',
    #                                 layout={'name': 'cose'},
    #                                 style={'width': '100%', 'height': '20vh'},
    #                                 elements = []
    #                             )
    #                         ])
    #                     ]),
    #                     html.Div(className = 'col-lg-4', children = [
    #                         html.Div(className = 'bar-chart-wp', children = [
    #                             cyto.Cytoscape(
    #                                 id='cyto-network-1',
    #                                 layout={'name': 'cose'},
    #                                 style={'width': '100%', 'height': '20vh'},
    #                                 elements = []
    #                             )
    #                         ])
    #                     ]),
    #                     html.Div(className = 'col-lg-4', children = [
    #                         html.Div(className = 'bar-chart-wp', children = [
    #                             cyto.Cytoscape(
    #                                 id='cyto-network-1',
    #                                 layout={'name': 'cose'},
    #                                 style={'width': '100%', 'height': '20vh'},
    #                                 elements = []
    #                             )
    #                         ])
    #                     ])
                    ])
                ])
            ])
        ])
    ]

@app.callback(
    Output("cyto-network", "elements"),
    [Input("genre_filter", "value"),
    Input("rating_filter", "value"),
    Input("sales_rank_filter", "value"),
    Input("reviews_filter", "value"),
    Input("page_filter", "value"),
    Input("price_filter", "value")],
)
def update_network_graph(genre_filter, rating_filter, sales_rank_filter, reviews_filter, page_filter, price_filter):
    elements = charts.plot_cyto_graph(params = locals())
    return elements

@app.callback(
    Output("cyto-network", "layout"),
    [Input("chart_type_option", "value")]
)
def update_graph_layout(chart_type_option):
    layout = {"name" : chart_type_option}
    return layout

@app.callback(
    Output("cyto-ego-network", "elements"),
    [Input("genre_filter", "value"),
    Input("rating_filter", "value"),
    Input("sales_rank_filter", "value"),
    Input("reviews_filter", "value"),
    Input("page_filter", "value"),
    Input("price_filter", "value")],
)
def update_ego_network_graph(genre_filter, rating_filter, sales_rank_filter, reviews_filter, page_filter, price_filter):
    elements = charts.plot_cyto_ego_graph(params = locals())
    return elements

@app.callback(
    Output("cyto-ego-network", "layout"),
    [Input("chart_type_option", "value")]
)
def update_ego_graph_layout(chart_type_option):
    layout = {"name" : chart_type_option}
    return layout

@app.callback(
    Output("cyto-clique-network", "elements"),
    [Input("genre_filter", "value"),
    Input("rating_filter", "value"),
    Input("sales_rank_filter", "value"),
    Input("reviews_filter", "value"),
    Input("page_filter", "value"),
    Input("price_filter", "value"),
    Input("nclique_filter", "value")],
)
def update_nclique_network_graph(genre_filter, rating_filter, sales_rank_filter, reviews_filter, page_filter, price_filter, nclique_filter):
    elements = charts.plot_cyto_nclique_graph(params = locals())
    return elements

@app.callback(
    Output("cyto-nclique-network", "layout"),
    [Input("chart_type_option", "value")]
)
def update_nclique_graph_layout(chart_type_option):
    layout = {"name" : chart_type_option}
    return layout