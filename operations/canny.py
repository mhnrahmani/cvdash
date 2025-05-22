# operations/canny.py

from dash import html, dcc

def render_ui(op_id, params):
    return html.Div([
        html.Label("Threshold 1 (lower)"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "threshold1"},
            min=0, max=500, step=1,
            value=params.get("threshold1", 100),
            marks={i: str(i) for i in range(0, 501, 100)}
        ),
        html.Label("Threshold 2 (upper)"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "threshold2"},
            min=0, max=500, step=1,
            value=params.get("threshold2", 200),
            marks={i: str(i) for i in range(0, 501, 100)}
        ),
        html.Label("Aperture Size"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "apertureSize"},
            min=3, max=7, step=2,
            value=params.get("apertureSize", 3),
            marks={i: str(i) for i in range(3, 8, 2)}
        ),
        html.Label("Use L2 Gradient"),
        dcc.Checklist(
            options=[{"label": "L2 Gradient", "value": "L2"}],
            value=["L2"] if params.get("L2gradient", False) else [],
            id={"type": "param", "op_id": op_id, "param": "L2gradient"}
        )
    ])

PARAMS = {
    "threshold1": 100,
    "threshold2": 200,
    "apertureSize": 3,
    "L2gradient": False
}
