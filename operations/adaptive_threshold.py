# operations/adaptive_threshold.py
from dash import html, dcc

PARAMS = {
    "maxValue": 255,
    "adaptiveMethod": "mean",  # 'mean' or 'gaussian'
    "thresholdType": "binary",  # 'binary' or 'binary_inv'
    "blockSize": 11,
    "C": 2
}

def render_ui(op_id, params):
    return html.Div([
        html.H5("Adaptive Threshold Parameters"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "maxValue"},
            min=0, max=255, step=1, value=params["maxValue"],
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.Label("Adaptive Method"),
        dcc.Dropdown(
            id={"type": "param", "op_id": op_id, "param": "adaptiveMethod"},
            options=[
                {"label": "Mean", "value": "mean"},
                {"label": "Gaussian", "value": "gaussian"}
            ],
            value=params["adaptiveMethod"],
            placeholder="Select Adaptive Method",
            clearable=False
        ),
        html.Label("Threshold Type"),
        dcc.Dropdown(
            id={"type": "param", "op_id": op_id, "param": "thresholdType"},
            options=[
                {"label": "Binary", "value": "binary"},
                {"label": "Binary Inverted", "value": "binary_inv"}
            ],
            value=params["thresholdType"],
            placeholder="Select Threshold Type",
            clearable=False
        ),
        html.Label("Block Size (must be odd)"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "blockSize"},
            min=3, max=31, step=2, value=params["blockSize"],
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.Label("C (constant subtracted from the mean or weighted mean)"),
        dcc.Slider(
            id={"type": "param", "op_id": op_id, "param": "C"},
            min=-20, max=20, step=1, value=params["C"],
            tooltip={"placement": "bottom", "always_visible": True},
        ),
    ])
