import pandas as pd
import calendar
import numpy as np
import random
import plotly.graph_objs as go
import dash_table
import dash_core_components as dcc


def get_generic_insights(data_df:pd.DataFrame):
	most_common_genre = data_df['genre'].mode()[0]
	
	min_pages = data_df['num_pages'].min()
	max_pages = data_df['num_pages'].max()
	avg_pages = data_df['num_pages'].mean()

	min_price = data_df['price'].min()
	max_price = data_df['price'].max()
	avg_price = data_df['price'].mean()
	
	min_reviews = data_df['num_reviews'].min()
	max_reviews = data_df['num_reviews'].max()
	avg_reviews = round(data_df['num_reviews'].mean())
	
	avg_rating = round(data_df['avg_rating'].mean())
	

	figure = {
		'data' : [
			go.Indicator(
			    domain = {'x': [0, 0.33], 'y': [0.5, 1]},
				value = avg_pages,
				mode = "gauge+number",
				title = {'text': "(Min, Max, Avg) Pages"},
				gauge = {
					'axis': {'range': [min_pages, max_pages]},
					'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': max_pages}
				}
			),
			go.Indicator(
			    domain = {'x': [0.33, 0.66], 'y': [0.5, 1]},
				value = avg_price,
				mode = "gauge+number",
				number = {'prefix': "$"},
				title = {'text': "(Min, Max, Avg) Prices"},
				gauge = {
					'axis': {'range': [min_price, max_price]},
					'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': max_price}
				}
			),
			go.Indicator(
			    domain = {'x': [0.66, 1], 'y': [0.5, 1]},
				value = avg_reviews,
				mode = "gauge+number",
				title = {'text': "(Min, Max, Avg) Reviews"},
				gauge = {
					'axis': {'range': [min_reviews, max_reviews]},
					'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': max_reviews}
				}
			),
			go.Indicator(
			    domain = {'x': [0.5, 1], 'y': [0, 0.3]},
				value = avg_rating,
				mode = "number",
				title = {'text': "Avg Rating"},
				gauge = {
					'axis': {'range': [0, 5]},
					'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 5}
				}
			),
			go.Indicator(
			    domain = {'x': [0, 0.5], 'y': [0, 0.3]},
				value = most_common_genre,
				mode = "number",
				title = {'text': "Top Genre"},
				gauge = {
					'axis': {'range': [0, 5]},
					'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 5}
				}
			)
		],
		'layout' : {
			"margin" : {"l": 0, "r" : 0, "t" : 50, "b" : 50}
		}
	}
	return figure


def get_stats_table(data_df: pd.DataFrame):
	"""
	Returns filterable table
	"""
	stats_table = dash_table.DataTable(
		id = "stats_table",
		columns = [
			{"name": i, "id": i, "deletable": False, "selectable": True} for i in data_df
		],
		data = data_df.to_dict('records'),
		filter_action="custom",
		filter_query="",
		sort_action="native",
		sort_mode="multi",
		style_as_list_view = True,
		merge_duplicate_headers = True,
		page_size = 20,
		style_header = {
			'backgroundColor': 'white',
			'fontWeight': 'bold',
			'textAlign' : 'center'
		},
		style_table = {
			'overflowX': 'auto'
		},
		style_cell = {
			"padding" : "5px",
			"font-family" : "Source Sans Pro",
			"fontSize" : 16,
		},
		style_data={
			'height': 'auto'
		},
		style_data_conditional = [
			{
				'if': {'row_index': 'odd'},
				'backgroundColor': 'rgb(248, 248, 248)'
			}
		] + [{'if': {'column_id': c},'textAlign': 'center'} for c in data_df.columns]
		,
		css = [
			{"selector": ".cell-1-1", "rule": "width: 100%;"},
			{"selector": 'td.cell--selected, td.focused', "rule": 'background-color: #6cc091 !important; color: #ffffff !important'}
		]
	)
	return stats_table

raw_df = pd.DataFrame([{'a' : 1, 'b' : 2}])

def generate_df_columns(dataframe = raw_df):
	return list(dataframe.columns)

def generate_unique_years(dataframe = raw_df):
	return dataframe['FiscalYear'].unique()

def generate_unique_countries(dataframe = raw_df):
	return dataframe['Country'].unique()

def generate_unique_cities(dataframe = raw_df):
	return dataframe['City'].unique()

def generate_unique_retailers(dataframe = raw_df):
	return dataframe['RetailerName'].unique()

def generate_unique_stores(dataframe = raw_df):
	return dataframe['StoreName'].unique()

def generate_unique_flash_categories(dataframe = raw_df):
	return dataframe['FlashCategory'].unique()

def generate_unique_product_categories(dataframe = raw_df):
	return dataframe['ProductCategory'].unique()

def generate_latest_sales_item(dataframe = raw_df):
	sample_purchase = dataframe.sample()
	while sample_purchase['SalesQuantity'].values[0] == 0 or sample_purchase['Sales'].values[0] <= 0 or not sample_purchase['Sales'].values[0] or np.isnan(sample_purchase['Sales'].values)[0]:
		sample_purchase = dataframe.sample()
	qty = int(sample_purchase['SalesQuantity'].values[0])
	part_no = sample_purchase['PartNumber'].values[0]
	flashcat = sample_purchase['FlashCategory'].values[0]
	productcat = sample_purchase['ProductCategory'].values[0]
	sales = sample_purchase['Sales'].values[0]
	country = sample_purchase['Country'].values[0]
	retailer = sample_purchase['RetailerName'].values[0]
	store = sample_purchase['StoreName'].values[0]
	message_string = f"<b>{qty}x {part_no} ({flashcat}, {productcat})</b> sold<br>{country}, {retailer}, {store}"
	return [message_string, sales]

def generate_sales_indicator(dataframe = raw_df, n_intervals = 0):
	sales_item_sample = generate_latest_sales_item()

	sales_over_day = dataframe.groupby(['SaleDate'])['Sales'].sum()
	sales_per_second = sales_over_day[-1] / 24 / 60 / 60
	latest_day_sales = (sales_over_day[-1] / 2) + (n_intervals * sales_per_second * 3.5) + sales_item_sample[1]

	sales_over_mth = dataframe.groupby(["FiscalYear", "FiscalQuarter", "FiscalMonthInt"])['Sales'].sum()
	sales_over_qtr = sales_over_mth.groupby(['FiscalYear', 'FiscalQuarter']).sum()

	flashcat_over_mth = raw_df.groupby(["FlashCategory", "FiscalYear", "FiscalMonthInt"])['SalesQuantity', 'Sales'].sum().reset_index().groupby("FlashCategory")['SalesQuantity', 'Sales']
	flashcat_over_mth_comparison = pd.DataFrame({"qty_prev": flashcat_over_mth.nth(-2)['SalesQuantity'],
													"qty_curr" : flashcat_over_mth.nth(-1)['SalesQuantity'],
													"rev_prev": flashcat_over_mth.nth(-2)['Sales'],
													"rev_curr" : flashcat_over_mth.nth(-1)['Sales']})
	flashcat_over_mth_comparison["qty_diff"] = (flashcat_over_mth_comparison["qty_curr"] - flashcat_over_mth_comparison["qty_prev"]) / flashcat_over_mth_comparison["qty_prev"]
	flashcat_over_mth_comparison["rev_diff"] = (flashcat_over_mth_comparison["rev_curr"] - flashcat_over_mth_comparison["rev_prev"]) / flashcat_over_mth_comparison["rev_prev"]

	country_over_mth = raw_df.groupby(["Country", "FiscalYear", "FiscalMonthInt"])['SalesQuantity', 'Sales'].sum().reset_index().groupby("Country")['SalesQuantity', 'Sales']
	country_over_mth_comparison = pd.DataFrame({"qty_prev": country_over_mth.nth(-2)['SalesQuantity'],
													"qty_curr" : country_over_mth.nth(-1)['SalesQuantity'],
													"rev_prev": country_over_mth.nth(-2)['Sales'],
													"rev_curr" : country_over_mth.nth(-1)['Sales']})
	country_over_mth_comparison["qty_diff"] = (country_over_mth_comparison["qty_curr"] - country_over_mth_comparison["qty_prev"]) / country_over_mth_comparison["qty_prev"]
	country_over_mth_comparison["rev_diff"] = (country_over_mth_comparison["rev_curr"] - country_over_mth_comparison["rev_prev"]) / country_over_mth_comparison["rev_prev"]

	figure = {
		'data' : [
			go.Indicator(
			    mode = "number+delta",
			    value = latest_day_sales,
			    number = {'prefix': "$"},
			    delta = {'position': "top", 'reference': sales_over_day[-2], 'relative' : True},
			    title = {'text' : 'Daily Sales'},
			    domain = {"x" : [0, 0.25]}
			),
			go.Indicator(
			    mode = "number+delta",
			    value = sales_over_mth[-1],
			    number = {'prefix': "$"},
			    delta = {'position': "top", 'reference': sales_over_mth[-2], 'relative' : True},
			    title = {'text' : 'Monthly Sales'},
			    domain = {"x" : [0.26, 0.5], "y" : [0.51, 1]}
			),
			go.Indicator(
			    mode = "number+delta",
			    value = sales_over_qtr[-1],
			    number = {'prefix': "$"},
			    delta = {'position': "top", 'reference': sales_over_qtr[-2], 'relative' : True},
			    title = {'text' : 'Quarterly Sales'},
			    domain = {"x" : [0.26, 0.5], "y" : [0, 0.5]}
			),
			go.Indicator(
			    mode = "number+delta",
			    value = flashcat_over_mth_comparison["rev_curr"][0],
			    number = {'prefix': "$"},
			    delta = {'position': "top", 'reference': flashcat_over_mth_comparison["rev_prev"][0], 'relative' : True},
			    title = {'text' : 'Top Flash Category<br />' + flashcat_over_mth_comparison.sort_values("rev_diff", ascending = False).index[0]},
			    domain = {"x" : [0.51, 0.75], "y" : [0.5, 1]}
			),
			go.Indicator(
			    mode = "number+delta",
			    value = country_over_mth_comparison["rev_curr"][0],
			    number = {'prefix': "$"},
			    delta = {'position': "top", 'reference': country_over_mth_comparison["rev_prev"][0], 'relative' : True},
			    title = {'text' : 'Top Country<br />' + country_over_mth_comparison.sort_values("rev_diff", ascending = False).index[0]},
			    domain = {"x" : [0.76, 1], "y" : [0.5, 1]}
			),
			go.Indicator(
				mode = "number",
			    title = {'text' : sales_item_sample[0]},
			    value = sales_item_sample[1],
			    number = {'prefix' : "$"},
			    domain = {"x" : [0.51, 1], "y" : [0, 0.3]}
			)
		],
		'layout' : {
			"margin" : {"l": 0, "r" : 0, "t" : 50, "b" : 50}
		}
	}
	return figure

def generate_qty_over_time(dataframe = raw_df):
	qty_over_time = dataframe.groupby("SaleDate")['SalesQuantity'].sum()
	figure={
		'data': [
			go.Scatter(
				x = qty_over_time.index,
				y = qty_over_time.values
			)
		],
		'layout' : {
			"margin" : {"l": 30, "r" : 30, "t" : 0, "b" : 50},
			"xaxis" : {"rangeslider" : {"visible" : True}}
		}
	}
	return figure

def generate_qty_rev_per_quarter(dataframe = raw_df):
	qty_per_quarter = dataframe.groupby(["FiscalYear", "FiscalQuarter"])['SalesQuantity'].sum()
	rev_per_quarter = dataframe.groupby(["FiscalYear", "FiscalQuarter"])['Sales'].sum()
	figure = {
		'data' : [
			go.Bar(
				name = "Quantity",
				x = list(map(lambda x : x[0] + " " + x[1], qty_per_quarter.index)),
				y = list(qty_per_quarter.values)
			),
			go.Bar(
				name = "Sales ($)",
				x = list(map(lambda x : x[0] + " " + x[1], rev_per_quarter.index)),
				y = list(rev_per_quarter.values),
				width = [0.3] * len(list(rev_per_quarter)),
				yaxis = "y2"
			)
		],
		'layout' : {
			"barmode" : "group",
			"margin" : {"l": 30, "r" : 30, "t" : 0, "b" : 50},
			"yaxis2" : {"side" : "right", "overlaying" : "y", "showgrid" : False}
		}
	}
	return figure

def generate_qty_by_country_over_time(dataframe = raw_df):
	qty_by_country_over_time = pd.pivot_table(dataframe, index = ["SaleDate"], columns = ["Country"], values = ["SalesQuantity"], aggfunc = np.sum)
	figure = {
		'data' : [
			go.Scatter(
				x = qty_by_country_over_time.index,
				y = qty_by_country_over_time[('SalesQuantity', country)].rolling(window = 90).mean(),
				mode = "lines",
				name = country
			)
			for country in qty_by_country_over_time.columns.get_level_values(1)
		],
		'layout' : {
			"margin" : {"l": 30, "r" : 30, "t" : 0, "b" : 50},
			"legend" : {"orientation" : "h"}
		}
	}
	return figure

def generate_qty_by_flash_cat_over_time(dataframe = raw_df):
	qty_by_flash_cat_over_time = pd.pivot_table(dataframe, index = ["SaleDate"], columns = ["FlashCategory"], values = ["SalesQuantity"], aggfunc = np.sum)
	figure = {
		'data' : [
			go.Scatter(
				x = qty_by_flash_cat_over_time.index,
				y = qty_by_flash_cat_over_time[('SalesQuantity', flash_category)].rolling(window = 28).mean(),
				mode = "lines",
				name = flash_category
			)
			for flash_category in qty_by_flash_cat_over_time.columns.get_level_values(1)
		],
		'layout' : {
			"margin" : {"l": 30, "r" : 30, "t" : 0, "b" : 50},
			"legend" : {"orientation" : "h"}
		}
	}
	return figure

def generate_qty_by_country_map(dataframe = raw_df):
	qty_by_country = dataframe.groupby("Country")['SalesQuantity'].sum().reset_index()
	figure = {
		'data' : [
			go.Choropleth(
				locations = qty_by_country['Country'],
				z = qty_by_country['SalesQuantity'],
				locationmode = 'country names',
				colorscale = 'Blues',
				colorbar = {"thickness" : 10},
				showscale = True,
				marker_line_color = "white"
			)
		],
		'layout' : {
			"geo" : {
				"resolution" : 50,
				"showcountries" : False,
				"scope" : "asia",
				"lonaxis" : {"range" : [93, 143]},
				"lataxis" : {"range" : [-10, 25]}
			},
			"margin" : {"l": 0, "r" : 0, "t" : 0, "b" : 50}
		}
	}
	return figure

def generate_rev_by_country_map(dataframe = raw_df):
	rev_by_country = dataframe.groupby("Country")['Sales'].sum().reset_index()
	figure = {
		'data' : [
			go.Choropleth(
				locations = rev_by_country['Country'],
				z = rev_by_country['Sales'],
				locationmode = 'country names',
				colorscale = 'Blues',
				colorbar = {"thickness" : 10},
				showscale = True,
				marker_line_color = "white"
			)
		],
		'layout' : {
			"geo" : {
				"resolution" : 50,
				"showcountries" : False,
				"scope" : "asia",
				"lonaxis" : {"range" : [93, 143]},
				"lataxis" : {"range" : [-10, 25]}
			},
			"margin" : {"l": 0, "r" : 0, "t" : 0, "b" : 50}
		}
	}
	return figure

def generate_qty_by_country_retailer(dataframe = raw_df):
	qty_by_country_retailer = dataframe.groupby(["Country", "RetailerName"])['SalesQuantity'].sum().reset_index()
	figure={
		'data': [
			go.Sunburst(
				labels=["Quantity"] + list(qty_by_country_retailer.groupby("Country")['SalesQuantity'].sum().index) + list(map(lambda row : row[0] + " " + row[1].split()[1], qty_by_country_retailer[['Country', 'RetailerName']].values)),
				parents=[""] + ["Quantity"] * len(qty_by_country_retailer['Country'].unique()) + list(qty_by_country_retailer['Country']),
				values=[qty_by_country_retailer.groupby("Country")['SalesQuantity'].sum().sum()] + list(qty_by_country_retailer.groupby("Country")['SalesQuantity'].sum()) + list(qty_by_country_retailer['SalesQuantity']),
				branchvalues = "total"
			)
		],
		'layout' : {"margin" : {"l": 0, "r" : 0, "t" : 0, "b" : 50}}
	}
	return figure

def generate_rev_by_country_retailer(dataframe = raw_df):
	rev_by_country_retailer = dataframe.groupby(["Country", "RetailerName"])['Sales'].sum().reset_index()
	figure={
		'data': [
			go.Sunburst(
				labels=["Sales"] + list(rev_by_country_retailer.groupby("Country")['Sales'].sum().index) + list(map(lambda row : row[0] + " " + row[1].split()[1], rev_by_country_retailer[['Country', 'RetailerName']].values)),
				parents=[""] + ["Sales"] * len(rev_by_country_retailer['Country'].unique()) + list(rev_by_country_retailer['Country']),
				values=[rev_by_country_retailer.groupby("Country")['Sales'].sum().sum()] + list(rev_by_country_retailer.groupby("Country")['Sales'].sum()) + list(rev_by_country_retailer['Sales']),
				branchvalues = "total"
			)
		],
		'layout' : {"margin" : {"l": 0, "r" : 0, "t" : 0, "b" : 50}}
	}
	return figure

def generate_qty_by_flashcat_productcat(dataframe = raw_df):
	qty_by_flashcat_productcat = dataframe.groupby(["FlashCategory", "ProductCategory"])['SalesQuantity'].sum().reset_index()
	figure={
		'data': [
			go.Sunburst(
				labels=["Quantity"] + list(qty_by_flashcat_productcat.groupby("FlashCategory")['SalesQuantity'].sum().index) + list(qty_by_flashcat_productcat[['FlashCategory', 'ProductCategory']]['ProductCategory']),
				parents=[""] + ["Quantity"] * len(qty_by_flashcat_productcat['FlashCategory'].unique()) + list(qty_by_flashcat_productcat['FlashCategory']),
				values=[qty_by_flashcat_productcat.groupby("FlashCategory")['SalesQuantity'].sum().sum()] + list(qty_by_flashcat_productcat.groupby("FlashCategory")['SalesQuantity'].sum()) + list(qty_by_flashcat_productcat['SalesQuantity']),
				branchvalues = "total"
			)
		],
		'layout' : {"margin" : {"l": 0, "r" : 0, "t" : 0, "b" : 50}}
	}
	return figure

def generate_rev_by_flashcat_productcat(dataframe = raw_df):
	rev_by_flashcat_productcat = dataframe.groupby(["FlashCategory", "ProductCategory"])['Sales'].sum().reset_index()
	figure={
		'data': [
			go.Sunburst(
				labels=["Sales"] + list(rev_by_flashcat_productcat.groupby("FlashCategory")['Sales'].sum().index) + list(rev_by_flashcat_productcat[['FlashCategory', 'ProductCategory']]['ProductCategory']),
				parents=[""] + ["Sales"] * len(rev_by_flashcat_productcat['FlashCategory'].unique()) + list(rev_by_flashcat_productcat['FlashCategory']),
				values=[rev_by_flashcat_productcat.groupby("FlashCategory")['Sales'].sum().sum()] + list(rev_by_flashcat_productcat.groupby("FlashCategory")['Sales'].sum()) + list(rev_by_flashcat_productcat['Sales']),
				branchvalues = "total"
			)
		],
		'layout' : {"margin" : {"l": 0, "r" : 0, "t" : 0, "b" : 50}}
	}
	return figure

def generate_qty_by_country_flashcat_heatmap(dataframe = raw_df):
	qty_country_flashcat = pd.pivot_table(dataframe, index = ["Country"], columns = ["FlashCategory"], values = ["SalesQuantity"], aggfunc = np.sum)
	figure = {
		'data' : [
			go.Heatmap(
				z = qty_country_flashcat.values,
				y = qty_country_flashcat.index,
				x = list(map(lambda x : x[1], qty_country_flashcat.columns)),
				colorscale = "Blues",
				colorbar = {"thickness" : 10},
				hovertemplate = 'Flash Category: <b>%{x}</b><br>Country: <b>%{y}</b><br>Quantity: <b>%{z:.3s}</b><extra></extra>'
			)
		],
		'layout' : {
			"margin" : {"l": 80, "r" : 0, "t" : 0, "b" : 50},
			"xaxis" : {"showgrid" : False},
			"yaxis" : {"showgrid" : False}
		}
	}
	return figure

def generate_rev_by_country_flashcat_heatmap(dataframe = raw_df):
	rev_country_flashcat = pd.pivot_table(dataframe, index = ["Country"], columns = ["FlashCategory"], values = ["Sales"], aggfunc = np.sum)
	figure = {
		'data' : [
			go.Heatmap(
				z = rev_country_flashcat.values,
				y = rev_country_flashcat.index,
				x = list(map(lambda x : x[1], rev_country_flashcat.columns)),
				colorscale = "Blues",
				colorbar = {"thickness" : 10},
				hovertemplate = 'Flash Category: <b>%{x}</b><br>Country: <b>%{y}</b><br>Sales ($): <b>%{z:$.3s}</b><extra></extra>'
			)
		],
		'layout' : {
			"margin" : {"l": 80, "r" : 0, "t" : 0, "b" : 50},
			"xaxis" : {"showgrid" : False},
			"yaxis" : {"showgrid" : False}
		}
	}
	return figure

def generate_qty_dow_by_week(dataframe = raw_df):
	dataframe = dataframe.copy()
	dataframe['DOW'] = pd.to_datetime(dataframe['SaleDate'], infer_datetime_format = True).dt.dayofweek
	dataframe['WeekNum'] = pd.to_datetime(dataframe['SaleDate'], infer_datetime_format = True).dt.week
	qty_dow_by_week = pd.pivot_table(dataframe, index = ['DOW'], columns = ['WeekNum'], values = ['SalesQuantity'], aggfunc = np.sum)
	qty_dow_by_week.columns = list(map(lambda x : x[1], qty_dow_by_week.columns))
	qty_dow_by_week.index = list(map(lambda x : calendar.day_abbr[x], qty_dow_by_week.index))
	qty_dow_by_week = qty_dow_by_week.reindex(list(calendar.day_abbr[-1:] + calendar.day_abbr[:-1])[::-1])
	figure = {
		'data' : [
			go.Heatmap(
				z = qty_dow_by_week.values,
				y = qty_dow_by_week.index,
				x = qty_dow_by_week.columns,
				colorscale = 'Greens',
				xgap = 5,
				ygap = 5,
				colorbar = {"thickness" : 10},
				hovertemplate = 'Week Number: <b>%{x}</b><br>Day of Week: <b>%{y}</b><br>Quantity: <b>%{z:.3s}</b><extra></extra>'
			)
		],
		'layout' : {
			"margin" : {"l": 50, "r" : 0, "t" : 0, "b" : 50},
			"xaxis" : {"showgrid" : False},
			"yaxis" : {"showgrid" : False}
		}
	}
	return figure

def generate_qty_dow_by_month(dataframe = raw_df):
	dataframe = dataframe.copy()
	dataframe['DOW'] = pd.to_datetime(dataframe['SaleDate'], infer_datetime_format = True).dt.dayofweek
	qty_dow_by_month = pd.pivot_table(dataframe, index = ['FiscalMonth'], columns = ['DOW'], values = ['SalesQuantity'], aggfunc = np.sum)
	qty_dow_by_month.columns = list(map(lambda x : calendar.day_abbr[x[1]], qty_dow_by_month.columns))
	qty_dow_by_month = qty_dow_by_month[list(calendar.day_abbr[-1:] + calendar.day_abbr[:-1])]
	qty_dow_by_month.index = list(map(lambda x : x[:3], qty_dow_by_month.index))
	qty_dow_by_month = qty_dow_by_month.reindex(list(calendar.month_abbr)[1:][::-1])
	figure = {
		'data' : [
			go.Heatmap(
				z = qty_dow_by_month.values,
				y = qty_dow_by_month.index,
				x = qty_dow_by_month.columns,
				colorscale = 'Greens',
				xgap = 5,
				ygap = 5,
				colorbar = {"thickness" : 10},
				hovertemplate = 'Day of Week: <b>%{x}</b><br>Month: <b>%{y}</b><br>Quantity: <b>%{z:.3s}</b><extra></extra>'
			)
		],
		'layout' : {
			"margin" : {"l": 50, "r" : 0, "t" : 0, "b" : 50},
			"xaxis" : {"showgrid" : False},
			"yaxis" : {"showgrid" : False}
		}
	}
	return figure

def generate_qty_dow_by_quarter(dataframe = raw_df):
	dataframe = dataframe.copy()
	dataframe['DOW'] = pd.to_datetime(dataframe['SaleDate'], infer_datetime_format = True).dt.dayofweek
	qty_dow_by_quarter = pd.pivot_table(dataframe, index = ['FiscalQuarter'], columns = ['DOW'], values = ['SalesQuantity'], aggfunc = np.sum)
	qty_dow_by_quarter.columns = list(map(lambda x : calendar.day_abbr[x[1]], qty_dow_by_quarter.columns))
	qty_dow_by_quarter = qty_dow_by_quarter[list(calendar.day_abbr[-1:] + calendar.day_abbr[:-1])]
	qty_dow_by_quarter = qty_dow_by_quarter.reindex(sorted(qty_dow_by_quarter.index, reverse = True))
	figure = {
		'data' : [
			go.Heatmap(
				z = qty_dow_by_quarter.values,
				y = qty_dow_by_quarter.index,
				x = qty_dow_by_quarter.columns,
				colorscale = 'Greens',
				xgap = 5,
				ygap = 5,
				colorbar = {"thickness" : 10},
				hovertemplate = 'Week Number: <b>%{x}</b><br>Quarter: <b>%{y}</b><br>Quantity: <b>%{z:.3s}</b><extra></extra>'
			)
		],
		'layout' : {
			"margin" : {"l": 50, "r" : 0, "t" : 0, "b" : 50},
			"xaxis" : {"showgrid" : False},
			"yaxis" : {"showgrid" : False}
		}
	}
	return figure

def generate_country_corr_heatmap(dataframe = raw_df):
	country = pd.pivot_table(dataframe, index = ['SaleDate'], columns = ['Country'], values = ['SalesQuantity'], aggfunc = np.sum)
	country.columns = list(map(lambda x : x[1], country.columns))
	country_corr = country.corr(method = "spearman")
	figure = {
		'data' : [
			go.Heatmap(
				z = country_corr.values,
				y = country_corr.index,
				x = country_corr.columns,
				zmin = -1,
				zmax = 1,
				colorscale = "rdbu",
				colorbar = {"thickness" : 10},
				hovertemplate = "Countries: <b>%{x} - %{y}</b><br>Spearman's Correlation: <b>%{z:.5f}</b><extra></extra>"
			)
		],
		'layout' : {
			"margin" : {"l": 80, "r" : 0, "t" : 0, "b" : 80},
			"xaxis" : {"showgrid" : False},
			"yaxis" : {"showgrid" : False}
		}
	}
	return figure

def generate_flash_cat_corr_heatmap(dataframe = raw_df):
	flash_cat = pd.pivot_table(dataframe, index = ['SaleDate'], columns = ['FlashCategory'], values = ['SalesQuantity'], aggfunc = np.sum)
	flash_cat.columns = list(map(lambda x : x[1], flash_cat.columns))
	flash_cat_corr = flash_cat.corr(method = "spearman")
	figure = {
		'data' : [
			go.Heatmap(
				z = flash_cat_corr.values,
				y = flash_cat_corr.index,
				x = flash_cat_corr.columns,
				zmin = -1,
				zmax = 1,
				colorscale = "rdbu",
				colorbar = {"thickness" : 10},
				hovertemplate = "Flash Categories: <b>%{x} - %{y}</b><br>Spearman's Correlation: <b>%{z:.5f}</b><extra></extra>"
			)
		],
		'layout' : {
			"margin" : {"l": 80, "r" : 0, "t" : 0, "b" : 80},
			"xaxis" : {"showgrid" : False},
			"yaxis" : {"showgrid" : False}
		}
	}
	return figure

def generate_country_flash_cat_corr_heatmap(dataframe = raw_df):
	country_flash_cat = pd.pivot_table(dataframe, index = ['SaleDate'], columns = ['Country', 'FlashCategory'], values = ['SalesQuantity'], aggfunc = np.sum)
	country_flash_cat.columns = list(map(lambda x : x[1] + "_" + x[2], country_flash_cat.columns))
	country_flash_cat_corr = country_flash_cat.corr(method = "spearman")
	figure = {
		'data' : [
			go.Heatmap(
				z = country_flash_cat_corr.values,
				y = country_flash_cat_corr.index,
				x = country_flash_cat_corr.columns,
				zmin = -1,
				zmax = 1,
				colorscale = "rdbu",
				colorbar = {"thickness" : 10},
				hovertemplate = "Pair: <b>%{x} - %{y}</b><br>Spearman's Correlation: <b>%{z:.5f}</b><extra></extra>"
			)
		],
		'layout' : {
			"margin" : {"l": 100, "r" : 0, "t" : 0, "b" : 100},
			"xaxis" : {"showgrid" : False},
			"yaxis" : {"showgrid" : False}
		}
	}
	return figure

def generate_country_flashcat_distribution_histogram(dataframe = raw_df):
	country_over_time = pd.pivot_table(dataframe, index = ['SaleDate'], columns = ['Country'], values = ['SalesQuantity'], aggfunc = np.sum)
	flashcat_over_time = pd.pivot_table(dataframe, index = ['SaleDate'], columns = ['FlashCategory'], values = ['SalesQuantity'], aggfunc = np.sum)
	country_over_time.columns = list(map(lambda x : x[1], country_over_time.columns))
	flashcat_over_time.columns = list(map(lambda x : x[1], flashcat_over_time.columns))
	figure = {
		'data' : [
			go.Histogram2d(
				x = country_over_time[country_over_time.columns[i // len(flashcat_over_time.columns)]],
				y = flashcat_over_time[flashcat_over_time.columns[i % len(flashcat_over_time.columns)]],
				colorscale = "fall",
				xaxis = "x" + str(i + 1),
				yaxis = "y" + str(i + 1),
				hovertemplate = "<b>" + country_over_time.columns[i // len(flashcat_over_time.columns)] + " - " + flashcat_over_time.columns[i % len(flashcat_over_time.columns)] + \
								"</b><br>FlashCategory Qty: <b>%{x}</b><br>Country Qty: <b>%{y}</b><br>Count: <b>%{z}</b><extra></extra>",
				showscale = False
			) for i in range(len(country_over_time.columns) * len(flashcat_over_time.columns))
		],
		'layout' : dict(
			[
				["margin", {"l": 30, "r" : 30, "t" : 0, "b" : 30}]
			]
			+
			[
				["xaxis" + str(j + 1), {
					"title" : flashcat_over_time.columns[j % len(flashcat_over_time.columns)],
					"domain" : [(j % len(flashcat_over_time.columns)) / len(flashcat_over_time.columns), ((j % len(flashcat_over_time.columns)) + 1) / len(flashcat_over_time.columns)],
					"showgrid" : False,
					"showticklabels" : False
				}]
				for j in range(len(country_over_time.columns) * len(flashcat_over_time.columns))
			]
			+
			[
				["yaxis" + str(k + 1), {
					"title" : country_over_time.columns[k // len(flashcat_over_time.columns)],
					"domain" : [(k // len(flashcat_over_time.columns)) / len(country_over_time.columns), ((k // len(flashcat_over_time.columns)) + 1) / len(country_over_time.columns)],
					"showgrid" : False,
					"showticklabels" : False
				}]
				for k in range(len(country_over_time.columns) * len(flashcat_over_time.columns))
			]
		)
	}
	return figure

def generate_unit_sales_by_country_over_time(dataframe = raw_df):
	sales_qty_by_country_over_time = pd.pivot_table(dataframe, index = ['SaleDate'], columns = ['Country'], values = ['Sales', 'SalesQuantity'], aggfunc = np.sum)
	unit_sales_by_country_over_time = sales_qty_by_country_over_time['Sales'] / sales_qty_by_country_over_time['SalesQuantity']
	figure = {
		'data' : [
			go.Scatter(
				x = unit_sales_by_country_over_time.index,
				y = unit_sales_by_country_over_time[country].rolling(window = 56).mean(),
				mode = "lines",
				name = country
			)
			for country in unit_sales_by_country_over_time.columns
		],
		'layout' : {
			"margin" : {"l": 30, "r" : 30, "t" : 0, "b" : 50},
			"legend" : {"orientation" : "h"}
		}
	}
	return figure

def generate_unit_sales_by_flashcat_over_time(dataframe = raw_df):
	sales_qty_by_flashcat_over_time = pd.pivot_table(dataframe, index = ['SaleDate'], columns = ['FlashCategory'], values = ['Sales', 'SalesQuantity'], aggfunc = np.sum)
	unit_sales_by_flashcat_over_time = sales_qty_by_flashcat_over_time['Sales'] / sales_qty_by_flashcat_over_time['SalesQuantity']
	figure = {
		'data' : [
			go.Scatter(
				x = unit_sales_by_flashcat_over_time.index,
				y = unit_sales_by_flashcat_over_time[flashcat].rolling(window = 56).mean(),
				mode = "lines",
				name = flashcat
			)
			for flashcat in unit_sales_by_flashcat_over_time.columns
		],
		'layout' : {
			"margin" : {"l": 30, "r" : 30, "t" : 0, "b" : 50},
			"legend" : {"orientation" : "h"}
		}
	}
	return figure

def generate_product_segmentation_scatter(dataframe = raw_df):
	product_list = dataframe.groupby(['FlashCategory', 'ProductCategory', 'PartNumber'])['Sales', 'SalesQuantity'].sum()
	product_list['UnitSales'] = product_list['Sales'] / product_list['SalesQuantity']
	unique_flashcats = sorted(list(set(list(map(lambda x : x[0], product_list.index)))))
	figure = {
		'data' : [
			go.Scatter(
				x = product_list['SalesQuantity'],
				y = product_list['Sales'],
				mode = "markers",
				marker = {
					'color' : list(map(lambda x : unique_flashcats.index(x[0]), product_list.index)),
					'colorscale' : 'Portland'
				},
				text = list(map(lambda x : " / ".join(x[0]) + f" (${round(x[1], 2)})", zip(product_list.index, product_list['UnitSales']))),
				hovertemplate = "Sales ($): <b>%{y:$.3s}</b><br>Quantity: <b>%{x:.3s}</b><br><b>%{text}</b><extra></extra>"
			)
		],
		'layout' : {
			"margin" : {"l": 30, "r" : 30, "t" : 0, "b" : 50},
			"xaxis" : {"title" : "Sales Quantity", "type" : "log", "showgrid" : False},
			"yaxis" : {"title" : "Sales", "type" : "log", "showgrid" : False},
			"hovermode" : "closest"
		}
	}
	return figure

def generate_country_dow_flashcat_parcats(dataframe = raw_df):
	dataframe = dataframe.copy()
	dataframe['DOW'] = pd.to_datetime(dataframe['SaleDate'], infer_datetime_format = True).dt.dayofweek
	dataframe['DOW'] = dataframe['DOW'].apply(lambda x : calendar.day_abbr[x])
	country_dow_flashcat = dataframe.groupby(['Country', 'DOW', 'FlashCategory'])['SalesQuantity'].sum()
	figure = {
		'data' : [
			go.Parcats(
				dimensions = [
					{
						'label' : country_dow_flashcat.index.names[i],
						'values' : list(map(lambda x : x[i], country_dow_flashcat.index))
					}
					for i in range(len(country_dow_flashcat.index.names))
				],
				counts = country_dow_flashcat.values,
				arrangement = "freeform",
				line = {"color" : country_dow_flashcat.values, "colorscale" : "Greens"}
			)
		],
		'layout' : {
			"margin" : {"l": 20, "r" : 20, "t" : 20, "b" : 50}
		}
	}
	return figure

def global_update(chart, filters):
	chart_func_map = {
		"qty_over_time" : generate_qty_over_time,
		"qty_rev_per_quarter" : generate_qty_rev_per_quarter,
		"qty_by_flash_cat_over_time" : generate_qty_by_flash_cat_over_time,
		"qty_by_country_over_time" : generate_qty_by_country_over_time,
		"qty_by_country_retailer" : generate_qty_by_country_retailer,
		"rev_by_country_retailer" : generate_rev_by_country_retailer,
		"qty_by_country_map" : generate_qty_by_country_map,
		"rev_by_country_map" : generate_rev_by_country_map,
		"qty_by_flashcat_productcat" : generate_qty_by_flashcat_productcat,
		"rev_by_flashcat_productcat" : generate_rev_by_flashcat_productcat,
		"qty_by_country_flashcat_heatmap" : generate_qty_by_country_flashcat_heatmap,
		"rev_by_country_flashcat_heatmap" : generate_rev_by_country_flashcat_heatmap,
		"qty_dow_by_week" : generate_qty_dow_by_week,
		"qty_dow_by_month" : generate_qty_dow_by_month,
		"qty_dow_by_quarter" : generate_qty_dow_by_quarter,
		"country_corr_heatmap" : generate_country_corr_heatmap,
		"flash_cat_corr_heatmap" : generate_flash_cat_corr_heatmap,
		"country_flash_cat_corr_heatmap" : generate_country_flash_cat_corr_heatmap,
		"country_flashcat_distribution_histogram" : generate_country_flashcat_distribution_histogram,
		"unit_sales_by_country_over_time" : generate_unit_sales_by_country_over_time,
		"unit_sales_by_flashcat_over_time" : generate_unit_sales_by_flashcat_over_time,
		"product_segmentation_scatter" : generate_product_segmentation_scatter,
		"country_dow_flashcat_parcats" : generate_country_dow_flashcat_parcats
	}
	filtered_df = raw_df.copy()
	for filter_arg, filter_val in filters.items():
		if filter_val != "All":
			filtered_df = filtered_df[filtered_df[filter_arg] == filter_val]
	return chart_func_map[chart](filtered_df)

def include_loader(graph_component):
	return dcc.Loading(type = "cube", color = "#36454f", children = [graph_component])