# components/cascader.py
from dash import dcc, html

def render():
    return html.Div([
        html.H4("Component Cascader"),

        html.Div([
            html.H5("Upload Image"),
            dcc.Upload(
                id="upload-image",
                children=html.Div(["Drag and Drop or ", html.A("Select File")]),
                style={
                    "width": "100%",
                    "height": "100px",
                    "lineHeight": "100px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "marginBottom": "10px"
                },
                multiple=False,
                accept="image/*"
            ),
            html.Div(id="upload-status", style={"color": "green", "marginTop": "10px"})
        ], style={"marginBottom": "20px"}),

        html.Div([
            html.H5("Operations List"),
            html.Div(id="operation-list")
        ]),

        html.Div([
            html.Button("Add Gaussian Blur", id="add-blur-btn", style={"marginTop": "10px", "marginRight": "5px"}),
            html.Button("Add Canny Edge", id="add-canny-btn", style={"marginTop": "10px"})
        ])
    ])
