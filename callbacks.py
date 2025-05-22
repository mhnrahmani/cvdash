# callbacks.py
import dash
from dash import Input, Output, State, ctx, html
from dash import MATCH, ALL
from dash.exceptions import PreventUpdate
import base64
import io
from PIL import Image
import numpy as np
import cv2
import uuid
from operations import operation_renderers
from operations.blur import PARAMS as BLUR_PARAMS
from operations.canny import PARAMS as CANNY_PARAMS

def register_callbacks(app: dash.Dash):

    @app.callback(
        Output("upload-status", "children"),
        Output("original-image-store", "data"),
        Input("upload-image", "contents"),
        prevent_initial_call=True
    )
    def store_image(contents):
        if contents is None:
            return "No image uploaded", None

        content_type, content_string = contents.split(',')
        return "Image successfully uploaded!", content_string

    @app.callback(
        Output("operation-list", "children"),
        Input("operation-stack", "data"),
        Input("selected-operation", "data"),
    )
    def update_operation_list(stack, selected_id):
        if not stack:
            return html.Div("No operations added yet.")

        def render_item(op):
            style = {"padding": "5px", "marginBottom": "5px", "border": "1px solid #ddd", "borderRadius": "5px"}
            if op["id"] == selected_id:
                style["backgroundColor"] = "#e0f7fa"
            return html.Div(op["type"].capitalize(), style=style, id={"type": "op-item", "index": op["id"]})

        return [render_item(op) for op in stack]

    @app.callback(
        Output("operation-stack", "data", allow_duplicate=True),
        Output("selected-operation", "data", allow_duplicate=True),
        Input("add-blur-btn", "n_clicks"),
        Input("add-canny-btn", "n_clicks"),
        State("operation-stack", "data"),
        prevent_initial_call=True
    )
    def add_operation(n_blur, n_canny, stack):
        button_id = ctx.triggered_id
        if stack is None:
            stack = []

        new_op = None
        if button_id == "add-blur-btn":
            new_op = {"id": str(uuid.uuid4()), "type": "blur", "params": BLUR_PARAMS.copy()}
        elif button_id == "add-canny-btn":
            new_op = {"id": str(uuid.uuid4()), "type": "canny", "params": CANNY_PARAMS.copy()}

        if new_op:
            stack.append(new_op)
            return stack, new_op["id"]

        return stack, dash.no_update

    @app.callback(
        Output("selected-operation", "data"),
        Input({"type": "op-item", "index": ALL}, "n_clicks"),
        State("operation-stack", "data"),
        prevent_initial_call=True
    )
    def select_operation(n_clicks_list, stack):
        triggered = ctx.triggered_id
        if not triggered or not stack:
            return dash.no_update
        return triggered["index"]

    @app.callback(
        Output("operation-stack", "data"),
        Output("selected-operation", "data", allow_duplicate=True),
        Input("delete-operation-btn", "n_clicks"),
        State("operation-stack", "data"),
        State("selected-operation", "data"),
        prevent_initial_call=True
    )
    def delete_selected(n_clicks, stack, selected_id):
        if not stack or not selected_id:
            return dash.no_update, dash.no_update

        new_stack = [op for op in stack if op["id"] != selected_id]
        new_selected = new_stack[-1]["id"] if new_stack else None

        return new_stack, new_selected

    @app.callback(
        Output("modifier-pane", "children"),
        Input("selected-operation", "data"),
        State("operation-stack", "data"),
        prevent_initial_call=True
    )
    def update_modifier_ui(selected_id, stack):
        if not selected_id or not stack:
            return "No operation selected."

        operation = next((op for op in stack if op["id"] == selected_id), None)
        if not operation:
            return "Invalid selection."

        renderer = operation_renderers.get(operation["type"])
        if not renderer:
            return f"No UI for operation type '{operation['type']}'."

        return renderer(operation["id"], operation["params"])

    @app.callback(
        Output("operation-stack", "data", allow_duplicate=True),
        Input({"type": "param", "op_id": ALL, "param": ALL}, "value"),
        State({"type": "param", "op_id": ALL, "param": ALL}, "id"),
        State("operation-stack", "data"),
        prevent_initial_call=True
    )
    def update_operation_params(values, ids, stack):
        if not stack or not values or not ids:
            raise PreventUpdate

        for value, id_ in zip(values, ids):
            op_id = id_["op_id"]
            param = id_["param"]

            for op in stack:
                if op["id"] == op_id:
                    # Checkbox (like L2gradient) comes as list
                    if param == "L2gradient":
                        op["params"][param] = "L2" in value
                    else:
                        op["params"][param] = value
                    break

        return stack
    

    # Callback to output stack
    @app.callback(
        Output("debug-output", "children"),
        Input("operation-stack", "data")
    )
    def show_stack(data):
        import json
        return json.dumps(data, indent=2)
