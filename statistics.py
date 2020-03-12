import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import charts
from app import app

content = html.Section(children = [
            html.Div(className = "inner", children = [
                html.H2("At a Glance", className = "align-center"),
                dcc.Graph(
                    id = 'sales_indicator',
                    figure = charts.generate_sales_indicator(),
                    config = {"displayModeBar" : False}
                ),
                dcc.Interval(
                    id = 'interval_component',
                    interval = 3500,
                    n_intervals = 0
                )
            ]),
            html.Section(className = "wrapper", style = {"background-color" : "#36454f"}, children = [
                html.Div(className = "inner", children = [
                    html.H2("Filters", style = {"color" : "white"}, className = "align-center"),
                    html.Div(className = "row", children = [
                        html.Div(className = "3u 12u(small)", children = [
                            dcc.Dropdown(
                                id = 'country_filter',
                                options = [{"label": "All Countries", "value" : "All"}] + [{"label": country, "value": country} for country in charts.generate_unique_countries()],
                                value = "All",
                                clearable = False
                            )
                        ]),
                        html.Div(className = "3u 12u(small)", children = [
                            dcc.Dropdown(
                                id = 'flash_cat_filter',
                                options = [{"label": "All Flash Categories", "value" : "All"}] + [{"label": flash_cat, "value": flash_cat} for flash_cat in charts.generate_unique_flash_categories()],
                                value = "All",
                                clearable = False
                            )
                        ]),
                        html.Div(className = "3u 12u(small)", children = [
                            dcc.Dropdown(
                                id = 'product_cat_filter',
                                options = [{"label": "All Product Categories", "value" : "All"}] + [{"label": product_cat, "value": product_cat} for product_cat in charts.generate_unique_product_categories()],
                                value = "All",
                                clearable = False
                            )
                        ]),
                        html.Div(className = "3u 12u$(small)", children = [
                            dcc.Dropdown(
                                id = 'year_filter',
                                options = [{"label": "All Years", "value" : "All"}] + [{"label": year, "value": year} for year in charts.generate_unique_years()],
                                value = "All",
                                clearable = False
                            )
                        ])
                    ])
                ])
            ]),
            html.Br(),
            html.Div(className = "inner", children = [
                html.H2("Historical", className = "align-center"),
                html.H4("Quantity over Time"),
                charts.include_loader(dcc.Graph(
                    id = 'qty_over_time',
                    figure = charts.generate_qty_over_time(),
                    config = {"displayModeBar" : False}
                )),
                html.H4("Performance per Quarter"),
                charts.include_loader(dcc.Graph(
                    id = 'qty_rev_per_quarter',
                    figure = charts.generate_qty_rev_per_quarter(),
                    config = {"displayModeBar" : False}
                )),
                html.Div(className = "row", children = [
                    html.Div(className = "6u 12u(medium)", children = [
                        html.H4("Quantity per Country over Time"),
                        charts.include_loader(dcc.Graph(
                            id = 'qty_by_country_over_time',
                            figure = charts.generate_qty_by_country_over_time(),
                            config = {"displayModeBar" : False}
                        ))
                    ]),
                    html.Div(className = "6u 12u$(medium)", children = [
                        html.H4("Quantity per Flash Category over Time"),
                        charts.include_loader(dcc.Graph(
                            id = 'qty_by_flash_cat_over_time',
                            figure = charts.generate_qty_by_flash_cat_over_time(),
                            config = {"displayModeBar" : False}
                        ))
                    ])
                ]),
                html.Hr(className = "major"),
                html.H2("Sales Breakdown", className = "align-center"),
                html.Div(className = "row", children = [
                    html.Div(className = "6u 12u(medium)", children = [
                        html.H3("Sales Quantity", className = "align-center"),
                        html.H4("By Country"),
                        charts.include_loader(dcc.Graph(
                            id = 'qty_by_country_map',
                            figure = charts.generate_qty_by_country_map(),
                            config = {"displayModeBar":False},
                        )),
                        html.Div(className = "row", children = [
                            html.Div(className = "6u 12u(large)", children = [
                                html.H4("By Country, Retailer"),
                                charts.include_loader(dcc.Graph(
                                    id = 'qty_by_country_retailer',
                                    figure = charts.generate_qty_by_country_retailer(),
                                    config = {"displayModeBar" : False}
                                ))
                            ]),
                            html.Div(className = "6u 12u$(large)", children = [
                                html.H4("By Flash, Product Category"),
                                charts.include_loader(dcc.Graph(
                                    id = 'qty_by_flashcat_productcat',
                                    figure = charts.generate_qty_by_flashcat_productcat(),
                                    config = {"displayModeBar" : False}
                                ))
                            ])
                        ]),
                        html.H4("By Country, Flash Category"),
                        charts.include_loader(dcc.Graph(
                            id = 'qty_by_country_flashcat_heatmap',
                            figure = charts.generate_qty_by_country_flashcat_heatmap(),
                            config = {"displayModeBar" : False}
                        ))
                    ]),
                    html.Div(className = "6u 12u$(medium)", children = [
                        html.H3("Sales ($)", className = "align-center"),
                        html.H4("By Country"),
                        charts.include_loader(dcc.Graph(
                            id = 'rev_by_country_map',
                            figure = charts.generate_rev_by_country_map(),
                            config = {"displayModeBar":False},
                        )),
                        html.Div(className = "row", children = [
                            html.Div(className = "6u 12u(large)", children = [
                                html.H4("By Country, Retailer"),
                                charts.include_loader(dcc.Graph(
                                    id = 'rev_by_country_retailer',
                                    figure = charts.generate_rev_by_country_retailer(),
                                    config = {"displayModeBar" : False}
                                ))
                            ]),
                            html.Div(className = "6u 12u$(large)", children = [
                                html.H4("By Flash, Product Category"),
                                charts.include_loader(dcc.Graph(
                                    id = 'rev_by_flashcat_productcat',
                                    figure = charts.generate_rev_by_flashcat_productcat(),
                                    config = {"displayModeBar" : False}
                                ))
                            ])
                        ]),
                        html.H4("By Country, Flash Category"),
                        charts.include_loader(dcc.Graph(
                            id = 'rev_by_country_flashcat_heatmap',
                            figure = charts.generate_rev_by_country_flashcat_heatmap(),
                            config = {"displayModeBar" : False}
                        ))
                    ])
                ])
            ])
        ])

@app.callback(
    [Output('qty_over_time', 'figure'),
    Output('qty_rev_per_quarter', 'figure'),
    Output('qty_by_flash_cat_over_time', 'figure'),
    Output('qty_by_country_over_time', 'figure'),
    Output('qty_by_country_retailer', 'figure'),
    Output('rev_by_country_retailer', 'figure'),
    Output('qty_by_country_map', 'figure'),
    Output('rev_by_country_map', 'figure'),
    Output('qty_by_flashcat_productcat', 'figure'),
    Output('rev_by_flashcat_productcat', 'figure'),
    Output('qty_by_country_flashcat_heatmap', 'figure'),
    Output('rev_by_country_flashcat_heatmap', 'figure')],
    [Input('country_filter', 'value'),
    Input('flash_cat_filter', 'value'),
    Input('product_cat_filter', 'value'),
    Input('year_filter', 'value')])
def filter_performance_charts(Country, FlashCategory, ProductCategory, FiscalYear):
    updated_figures = [
        charts.global_update("qty_over_time", locals()),
        charts.global_update("qty_rev_per_quarter", locals()),
        charts.global_update("qty_by_flash_cat_over_time", locals()),
        charts.global_update("qty_by_country_over_time", locals()),
        charts.global_update("qty_by_country_retailer", locals()),
        charts.global_update("rev_by_country_retailer", locals()),
        charts.global_update("qty_by_country_map", locals()),
        charts.global_update("rev_by_country_map", locals()),
        charts.global_update("qty_by_flashcat_productcat", locals()),
        charts.global_update("rev_by_flashcat_productcat", locals()),
        charts.global_update("qty_by_country_flashcat_heatmap", locals()),
        charts.global_update("rev_by_country_flashcat_heatmap", locals())]
    return updated_figures

@app.callback(
    Output('sales_indicator', 'figure'),
    [Input('interval_component', 'n_intervals')])
def generate_sales_notification(n):
    return charts.generate_sales_indicator(n_intervals = n)