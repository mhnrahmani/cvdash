# layout.py
from dash import html
from components import cascader, preview, modifier

def get_layout():
    return html.Div([
        html.Div([
            html.Div(cascader.render(), className="pane-left"),

            html.Div([
                html.Div(modifier.render(), className="pane-modifier"),
                html.Div(preview.render(), className="pane-preview"),
            ], className="pane-right"),
        ], className="main-pane-container"),

        html.Div("Toolbar / Footer Placeholder", className="pane-bottom")
    ])
