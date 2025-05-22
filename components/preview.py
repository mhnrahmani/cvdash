# components/preview.py
from dash import html

def render():
    return html.Div([
        html.H4("Image Preview"),
        html.Img(id="image-preview", style={"maxWidth": "100%", "maxHeight": "100%"})
    ])
