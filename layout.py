# layout.py
from dash import html
import dash_bootstrap_components as dbc
from components import cascader, modifier, preview, toolbar

def get_layout():
    return dbc.Container([
        dbc.Row([
            # Left Panel
            dbc.Col(cascader.render(), width=3, style={
                "borderRight": "1px solid #ccc",
                "padding": "10px"
            }),

            # Middle Panel
            dbc.Col([
                html.Div(modifier.render(), style={
                    "height": "40%",
                    "borderBottom": "1px solid #ccc",
                    "padding": "10px"
                }),
                html.Div(preview.render(), style={
                    "height": "60%",
                    "padding": "10px"
                })
            ], width=7),

            # Right Panel - Output Text Area
            dbc.Col(html.Div(
                id="debug-output",
                style={
                    "height": "100%",
                    "overflowY": "auto",
                    "backgroundColor": "black",
                    "color": "white",
                    "padding": "10px",
                    "whiteSpace": "pre-wrap"
                }
            ), width=2)
        ], style={"height": "100vh"})
    ], fluid=True)
