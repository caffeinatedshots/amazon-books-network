import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import charts
from app import app

content = html.Section(children = [
			html.Section(className = "inner", children = [
	            html.H2("Filters", className = "align-center"),
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
	            ]),
	            html.Section(className = "inner" , children = [
	            	html.Br(),
		            html.H2("Time", className = "align-center"),
		            html.H4("Weekly Quantity"),
		            charts.include_loader(dcc.Graph(
		            	id = 'qty_dow_by_week',
		            	figure = charts.generate_qty_dow_by_week(),
		            	config = {"displayModeBar" : False},
		            	style = {"height" : "20vh", "max-height" : "15vw"}
		            )),
		            html.Div(className = "row", children = [
		            	html.Div(className = "6u 12u(medium)", children = [
		            		html.H4("Monthly Quantity"),
				            charts.include_loader(dcc.Graph(
				            	id = 'qty_dow_by_month',
				            	figure = charts.generate_qty_dow_by_month(),
				            	config = {"displayModeBar" : False},
				            	style = {"height" : "40vh", "max-height" : "30vw"}
				            ))
	            		]),
	            		html.Div(className = "6u 12u$(medium)", children = [
		            		html.H4("Quarterly Quantity"),
				            charts.include_loader(dcc.Graph(
				            	id = 'qty_dow_by_quarter',
				            	figure = charts.generate_qty_dow_by_quarter(),
				            	config = {"displayModeBar" : False},
				            	style = {"height" : "40vh", "max-height" : "30vw"}
				            ))
	            		])
	            	]),
		            html.Hr(className = "major"),
		            html.H2("Correlation", className = "align-center"),
		            html.Div(className = "row", children = [
		            	html.Div(className = "6u 12u(medium)", children = [
		            		html.H4("Country"),
				            charts.include_loader(dcc.Graph(
				            	id = 'country_corr_heatmap',
				            	figure = charts.generate_country_corr_heatmap(),
				            	config = {"displayModeBar" : False},
				            	style = {"height" : "30vw", "max-height" : "40vh"}
				            ))
				        ]),
				        html.Div(className = "6u 12u$(medium)", children = [
				            html.H4("Flash Category"),
				            charts.include_loader(dcc.Graph(
				            	id = 'flash_cat_corr_heatmap',
				            	figure = charts.generate_flash_cat_corr_heatmap(),
				            	config = {"displayModeBar" : False},
				            	style = {"height" : "30vw", "max-height" : "40vh"}
				            ))
		            	])
		            ]),
	            	html.H4("Country, Flash Category"),
		            charts.include_loader(dcc.Graph(
		            	id = 'country_flash_cat_corr_heatmap',
		            	figure = charts.generate_country_flash_cat_corr_heatmap(),
		            	config = {"displayModeBar" : False},
		            	style = {"height" : "60vh", "max-height" : "50vw"}
		            )),
		            html.Hr(className = "major"),
		            html.H2("Distributions", className = "align-center"),
		            charts.include_loader(dcc.Graph(
		            	id = 'country_flashcat_distribution_histogram',
		            	figure = charts.generate_country_flashcat_distribution_histogram(),
		            	config = {"displayModeBar" : False},
		            	style = {"height" : "70vw", "max-height" : "80vh"}
		            )),
		            html.Hr(className = "major"),
		            html.H2("Sale / Unit", className = "align-center"),
		            html.Div(className = "row", children = [
		            	html.Div(className = "6u 12u(medium)", children = [
		            		html.H4("By Country"),
				            charts.include_loader(dcc.Graph(
				            	id = "unit_sales_by_country_over_time",
				            	figure = charts.generate_unit_sales_by_country_over_time(),
				            	config = {"displayModeBar" : False}
				            ))
		            	]),
		            	html.Div(className = "6u 12u$(medium)", children = [
		            		html.H4("By Flash Category"),
				            charts.include_loader(dcc.Graph(
				            	id = "unit_sales_by_flashcat_over_time",
				            	figure = charts.generate_unit_sales_by_flashcat_over_time(),
				            	config = {"displayModeBar" : False}
				            ))
		            	])
		            ]),
		            html.Hr(className = "major"),
		            html.H2("Product Segmentation", className = "align-center"),
		            charts.include_loader(dcc.Graph(
		            	id = "product_segmentation_scatter",
		            	figure = charts.generate_product_segmentation_scatter(),
		            	config = {"displayModeBar" : False}
		            )),
		            html.Hr(className = "major"),
		            html.H2("Interaction", className = "align-center"),
		            html.H4("Between Country, Day of Week, Flash Category"),
		            charts.include_loader(dcc.Graph(
		            	id = "country_dow_flashcat_parcats",
		            	figure = charts.generate_country_dow_flashcat_parcats(),
		            	config = {"displayModeBar" : False}
		            ))
	            ])
	        ])
		])

@app.callback(
    [Output('qty_dow_by_week', 'figure'),
    Output('qty_dow_by_month', 'figure'),
    Output('qty_dow_by_quarter', 'figure'),
    Output('country_corr_heatmap', 'figure'),
    Output('flash_cat_corr_heatmap', 'figure'),
    Output('country_flash_cat_corr_heatmap', 'figure'),
    Output('country_flashcat_distribution_histogram', 'figure'),
    Output('unit_sales_by_country_over_time', 'figure'),
    Output('unit_sales_by_flashcat_over_time', 'figure'),
    Output('product_segmentation_scatter', 'figure'),
    Output('country_dow_flashcat_parcats', 'figure')],
    [Input('country_filter', 'value'),
    Input('flash_cat_filter', 'value'),
    Input('product_cat_filter', 'value'),
    Input('year_filter', 'value')])
def filter_performance_charts(Country, FlashCategory, ProductCategory, FiscalYear):
    updated_figures = [
        charts.global_update("qty_dow_by_week", locals()),
        charts.global_update("qty_dow_by_month", locals()),
        charts.global_update("qty_dow_by_quarter", locals()),
        charts.global_update("country_corr_heatmap", locals()),
        charts.global_update("flash_cat_corr_heatmap", locals()),
        charts.global_update("country_flash_cat_corr_heatmap", locals()),
        charts.global_update("country_flashcat_distribution_histogram", locals()),
        charts.global_update("unit_sales_by_country_over_time", locals()),
        charts.global_update("unit_sales_by_flashcat_over_time", locals()),
        charts.global_update("product_segmentation_scatter", locals()),
        charts.global_update("country_dow_flashcat_parcats", locals())]
    return updated_figures