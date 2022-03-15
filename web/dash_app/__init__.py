from dash import Dash, html


def create_dash_application(flask_app):
    dash_app = Dash(server=flask_app,
                    name="Dashboard",
                    url_base_pathname='/dash/'
                    )

    dash_app.layout = html.Div(children=[
        html.H1(children='Por favor, vuelva a la página principal y suba los archivos.')
    ])

    return dash_app
