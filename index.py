import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import charts
import statistics
import analytics

from app import app

app.title = "Amazon Books Network Analysis"

app.layout = html.Div(children=[
    html.Header(id = "header", children = [
        html.Div(className = "inner", children = [
            html.A("Amazon Books Network Analysis", className = "logo"),
            html.Nav(className = "nav", children = [
                html.A("Statistics", href = "/"),
                html.A("Analytics", href = "/analytics")
            ])
        ])
    ]),

    html.Section(id = "banner", children = [
        html.Div(className = "inner", children = [
            html.Header(children = [
                html.H1(id = "common_title")
            ]),
            html.Div(className = "flex", children = [
                html.Div(children = [
                    html.Span(className = "icon fa-globe"),
                    html.H3(len(charts.generate_unique_countries())),
                    html.P("Countries")
                ]),
                html.Div(children = [
                    html.Span(className = "icon fa-building"),
                    html.H3(len(charts.generate_unique_cities())),
                    html.P("Cities")
                ]),
                html.Div(children = [
                    html.Span(className = "icon fa-industry"),
                    html.H3(len(charts.generate_unique_retailers())),
                    html.P("Retailers")
                ]),
                html.Div(children = [
                    html.Span(className = "icon fa-home"),
                    html.H3(len(charts.generate_unique_stores())),
                    html.P("Stores")
                 ])
            ])
        ])
    ]),
    dcc.Location(id='url', refresh=False),
    html.Section(id = "page_content", className = "wrapper")
])

@app.callback([Output('page_content', 'children'),
                Output('common_title', 'children')],
              [Input('url', 'pathname')])
def show_content(page):
    if page == None:
        page = "/"
    path_map = {
        "/" : statistics.content,
        "/analytics" : analytics.content
    }
    title_map = {
        "/" : "Statistics",
        "/analytics" : "Analytics"
    }
    return [path_map[page], title_map[page]]


if __name__ == "__main__":
    app.run_server(debug=True)