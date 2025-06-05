# operations/morphology.py

from dash import html, dcc

PARAMS = {
    "operation": "dilate",  # dilate or erode
    "kernel_size": 3,
    "iterations": 1
}

def render_ui(op_id, params):
    return html.Div([
        html.H5("Morphology Parameters"),
        dcc.Dropdown(
            id={"type": "param", "op_id": op_id, "param": "operation"},
            options=[
                {"label": "Dilation", "value": "dilate"},
                {"label": "Erosion", "value": "erode"},
            ],
            value=params["operation"],
            placeholder="Select Operation",
            style={"marginBottom": "10px"},
        ),
        html.Label("Kernel Size (odd number):"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "kernel_size"},
            min=1, max=15, step=2, value=params["kernel_size"],
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.Label("Iterations:"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "iterations"},
            min=1, max=10, step=1, value=params["iterations"],
            tooltip={"placement": "bottom", "always_visible": True},
        ),
    ])
