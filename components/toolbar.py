# components/toolbar.py
from dash import html

def render():
    return html.Div(
        children=[
            html.Div("Toolbar (Placeholder)", style={
                "textAlign": "center",
                "padding": "10px",
                "backgroundColor": "#f8f9fa",
                "borderTop": "1px solid #dee2e6"
            })
        ],
        style={"width": "100%"}
    )
