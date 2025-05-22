# callbacks.py
import dash
from dash import Input, Output, State, ctx, html
from dash import MATCH, ALL
import base64
import io
from PIL import Image
import numpy as np
import cv2
import uuid

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
        Input("add-blur-btn", "n_clicks"),
        Input("add-canny-btn", "n_clicks"),
        State("operation-stack", "data"),
        prevent_initial_call="initial_duplicate"
    )
    def add_operation(n_blur, n_canny, stack):
        button_id = ctx.triggered_id
        if stack is None:
            stack = []

        new_op = None
        if button_id == "add-blur-btn":
            new_op = {"id": str(uuid.uuid4()), "type": "blur", "params": {"ksize": 5}}
        elif button_id == "add-canny-btn":
            new_op = {"id": str(uuid.uuid4()), "type": "canny", "params": {"threshold1": 100, "threshold2": 200}}

        if new_op:
            stack.append(new_op)
        return stack

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
        return new_stack, None
