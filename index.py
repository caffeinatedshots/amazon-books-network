import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import charts
import statistics
import genre

from app import app

app.title = "Amazon Books Network Analysis"

app.layout = html.Div(children=[
    html.Div(className = "header-top-area", children = [
        html.Div(className = 'container', children = [
            html.Div(className = 'row', children = [
                html.Div(className = 'col-lg-6 col-md-6 col-sm-12 col-xs-12', children = [
                    html.Div(className = "logo-area", children = [
                        html.A(href = '/', children = [
                            html.Img(src = 'assets/img/logo/logo.png')
                        ])
                    ])
                ]),
                html.Div(className = 'col-lg-6 col-md-6 col-sm-12 col-xs-12', children = [
                    html.Div(className = "header-top-menu", children = [
                        html.Ul(className = "nav navbar-nav notika-top-nav", children = [
                            html.Li(className = 'nav-item', children = [
                                html.A(className = 'nav-link', href = "/genre", title = "Genre", children = [
                                    html.I(className = 'fa fa-book')
                                ])
                            ])
                        ])
                    ])
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
        "/genre" : genre.content
    }
    title_map = {
        "/" : "Statistics",
        "/genre" : "Genre"
    }
    return [path_map[page], title_map[page]]


if __name__ == "__main__":
    app.run_server(debug=True)