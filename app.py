# app.py
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from layout import get_layout
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder="assets")
app.title = "Image Processing Dashboard"

# Store the image at the app level
app.layout = html.Div([
    dcc.Store(id="original-image-store"),  # Store the image globally here
    get_layout()
])

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
