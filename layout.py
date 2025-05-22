# layout.py
from dash import html
import dash_bootstrap_components as dbc
from components import cascader, modifier, preview, toolbar

def get_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(cascader.render(), width=3, style={"borderRight": "1px solid #ccc", "padding": "10px"}),
            dbc.Col([
                html.Div(modifier.render(), style={"height": "40%", "borderBottom": "1px solid #ccc", "padding": "10px"}),
                html.Div(preview.render(), style={"height": "60%", "padding": "10px"})
            ], width=9)
        ], style={"height": "90vh"}),
        html.Pre(id="debug-output")
    ], fluid=True)
