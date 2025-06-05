# operations/blur.py

from dash import html, dcc

def render_ui(op_id, params):
    return html.Div([
        html.Label("Kernel Size (odd int)"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "ksize"},
            min=1, max=31, step=2,
            value=params.get("ksize", 5),
            marks={i: str(i) for i in range(1, 32, 2)},
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.Label("Sigma X"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "sigmaX"},
            min=0, max=10, step=0.1,
            value=params.get("sigmaX", 1.0),
            marks={i: str(i) for i in range(0, 11)},
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.Label("Sigma Y"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "sigmaY"},
            min=0, max=10, step=0.1,
            value=params.get("sigmaY", 0.0),
            marks={i: str(i) for i in range(0, 11)},
            tooltip={"placement": "bottom", "always_visible": True},
        )
    ])


PARAMS = {
    "ksize": 5,
    "sigmaX": 1.0,
    "sigmaY": 0.0
}
