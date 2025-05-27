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
                html.Div(preview.render(), style={
                    "flex": "7",
                    "overflow": "hidden",
                    "borderBottom": "1px solid #ccc",
                    "padding": "10px",
                    "display": "flex",
                    "flexDirection": "column"
                }),
                html.Div(modifier.render(), style={
                    "flex": "3",
                    "padding": "10px",
                    "overflowY": "auto"
                }),
            ], width=7, style={"display": "flex", "flexDirection": "column", "height": "100%"}),

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
