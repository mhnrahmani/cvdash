# app.py
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from layout import get_layout
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder="assets")
server = app.server
app.title = "The OpenCV Dashboard"

# Global stores for image and operation management
app.layout = html.Div([
    dcc.Store(id="original-image-store"),
    dcc.Store(id="operation-stack", data=[]),
    dcc.Store(id="selected-operation", data=None),
    get_layout()
])

register_callbacks(app)

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8050,
    )
