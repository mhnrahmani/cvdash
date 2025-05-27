# components/preview.py
from dash import html

def render():
    return html.Div([
        html.H4("Image Preview"),
        html.Div(
            html.Img(
                id="image-preview",
                style={
                    "width": "100%",
                    "height": "100%",
                    "objectFit": "contain"
                }
            ),
            style={"flex": "1", "overflow": "hidden"}
        )
    ], style={"display": "flex", "flexDirection": "column", "height": "100%"})