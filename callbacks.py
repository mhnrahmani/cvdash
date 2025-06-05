# callbacks.py

import dash
from dash import Input, Output, State, ctx, html
from dash import ALL
from dash.exceptions import PreventUpdate
import uuid
from operations import operation_renderers
from operations.blur import PARAMS as BLUR_PARAMS
from operations.canny import PARAMS as CANNY_PARAMS
from operations.grayscale import PARAMS as GRAYSCALE_PARAMS
from operations.morphology import PARAMS as MORPHOLOGY_PARAMS
from operations.adaptive_threshold import PARAMS as ADAPTIVE_THRESHOLD_PARAMS
# ^^ Add new operation params ^^
import base64
import io
from PIL import Image
import numpy as np
import cv2
import warnings

def apply_operations(image: np.ndarray, operations: list) -> np.ndarray:
    img = image.copy()
    for op in operations:
        op_type = op["type"]
        params = op["params"]

        if op_type == "grayscale":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif op_type == "blur":
            k = params.get("ksize", 5)
            img = cv2.blur(img, (k, k))
        elif op_type == "canny":
            # TODO: Must be grayscale
            # if len(img.shape) == 3 and img.shape[2] == 3:
            #     warnings.warn("Canny edge detection was applied to a color image.", UserWarning)
            t1 = params.get("threshold1", 100)
            t2 = params.get("threshold2", 200)
            l2 = params.get("L2gradient", False)
            img = cv2.Canny(img, t1, t2, L2gradient=l2)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # keep 3-channel
        elif op_type == "morphology":
            op_map = {
                "dilate": cv2.dilate,
                "erode": cv2.erode
            }
            kernel = np.ones((params["kernel_size"], params["kernel_size"]), np.uint8)
            operation_fn = op_map.get(params["operation"])
            if operation_fn:
                img = operation_fn(img, kernel, iterations=params["iterations"])
        elif op_type == "adaptive_threshold":
            # TODO: Must be grayscale
            method = cv2.ADAPTIVE_THRESH_MEAN_C if params["adaptiveMethod"] == "mean" else cv2.ADAPTIVE_THRESH_GAUSSIAN_C
            thresh_type = cv2.THRESH_BINARY if params["thresholdType"] == "binary" else cv2.THRESH_BINARY_INV
            img = cv2.adaptiveThreshold(
                img,
                maxValue=params["maxValue"],
                adaptiveMethod=method,
                thresholdType=thresh_type,
                blockSize=params["blockSize"],
                C=params["C"]
            )
        # ^^ Add new operation logic ^^

    return img

def register_callbacks(app: dash.Dash):
    # -----------------------------
    # Image Upload
    # -----------------------------
    @app.callback(
        Output("upload-status", "children"),
        Output("original-image-store", "data"),
        Input("upload-image", "contents"),
        prevent_initial_call=True
    )
    def store_image(contents):
        if contents is None:
            return "No image uploaded", None

        _, content_string = contents.split(',')
        return "Image successfully uploaded!", content_string
    
    @app.callback(
        Output("image-preview", "src"),
        Input("original-image-store", "data"),
        Input("operation-stack", "data"),
        prevent_initial_call=True
    )
    def render_processed_image(base64_img, stack):
        if not base64_img:
            raise PreventUpdate

        # Decode uploaded base64 image to NumPy array
        img_data = base64.b64decode(base64_img)
        img_pil = Image.open(io.BytesIO(img_data)).convert("RGB")
        img_np = np.array(img_pil)[:, :, ::-1]  # RGB (PIL) → BGR (OpenCV)

        # Apply operation stack
        if stack:
            img_np = apply_operations(img_np, stack)

        # Encode back to base64 for display
        _, buffer = cv2.imencode('.jpg', img_np)
        encoded = base64.b64encode(buffer).decode()
        return f"data:image/jpeg;base64,{encoded}"


    # -----------------------------
    # Operation List UI Update
    # -----------------------------
    @app.callback(
        Output("operation-list", "children"),
        Input("operation-stack", "data"),
        Input("selected-operation", "data"),
        prevent_initial_call=True
    )
    def update_operation_list(stack, selected_id):
        if not stack:
            return html.Div("No operations added yet.")

        def render_item(op):
            style = {
                "padding": "5px", "marginBottom": "5px",
                "border": "1px solid #ddd", "borderRadius": "5px"
            }
            if op["id"] == selected_id:
                style["backgroundColor"] = "#e0f7fa"
            return html.Div(op["type"].capitalize(), style=style,
                            id={"type": "op-item", "index": op["id"]})

        return [render_item(op) for op in stack]

    # -----------------------------
    # Add Operation
    # -----------------------------
    @app.callback(
        Output("operation-stack", "data", allow_duplicate=True),
        Input("add-grayscale-btn", "n_clicks"),
        Input("add-blur-btn", "n_clicks"),
        Input("add-canny-btn", "n_clicks"),
        Input("add-morphology-btn", "n_clicks"),
        Input("add-adaptive-threshold-btn", "n_clicks"),
        # ^^ Add new operation as Input ^^
        State("operation-stack", "data"),
        prevent_initial_call=True
    )
    def add_operation(n_grayscale, n_blur, n_canny, n_morph, n_adaptive_threshold, stack):
        button_id = ctx.triggered_id
        if stack is None:
            stack = []

        new_op = None
        if button_id == "add-grayscale-btn":
            new_op = {"id": str(uuid.uuid4()), "type": "grayscale", "params": GRAYSCALE_PARAMS.copy()}
        elif button_id == "add-blur-btn":
            new_op = {"id": str(uuid.uuid4()), "type": "blur", "params": BLUR_PARAMS.copy()}
        elif button_id == "add-canny-btn":
            new_op = {"id": str(uuid.uuid4()), "type": "canny", "params": CANNY_PARAMS.copy()}
        elif button_id == "add-morphology-btn":
            new_op = {"id": str(uuid.uuid4()), "type": "morphology", "params": MORPHOLOGY_PARAMS.copy()}
        elif button_id == "add-adaptive-threshold-btn":
            new_op = {"id": str(uuid.uuid4()), "type": "adaptive_threshold", "params": ADAPTIVE_THRESHOLD_PARAMS.copy()}
        # ^^ Add new operation ^^

        if new_op:
            stack.append(new_op)
            return stack 

        return dash.no_update

    # -----------------------------
    # Select Operation
    # -----------------------------
    @app.callback(
        Output("selected-operation", "data"),
        Input({"type": "op-item", "index": ALL}, "n_clicks"),
        State("operation-stack", "data"),
        prevent_initial_call=True
    )
    def select_operation(n_clicks_list, stack):
        # Guard clause: check for None or all-None values
        if not n_clicks_list or all(click is None for click in n_clicks_list) or not stack:
            raise PreventUpdate

        # Find the maximum n_clicks value, ignoring None
        valid_clicks = [(i, click) for i, click in enumerate(n_clicks_list) if click is not None]
        max_index, _ = max(valid_clicks, key=lambda x: x[1])
        return stack[max_index]["id"]

    # if written based on context instead of n_clicks_list:
    # def select_operation(n_clicks_list, stack):
    #     print("n_clicks_list:", n_clicks_list)  # Debug output

    #     triggered = ctx.triggered_id
    #     if not triggered or not stack:
    #         raise PreventUpdate
    #     return triggered["index"]

    # -----------------------------
    # Delete Selected Operation
    # -----------------------------
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
            raise PreventUpdate

        new_stack = [op for op in stack if op["id"] != selected_id]
        return new_stack, None

    # -----------------------------
    # Update Modifier UI
    # -----------------------------
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

    # -----------------------------
    # Update Parameters of Selected Operation
    # -----------------------------
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
                    if param == "L2gradient":
                        op["params"][param] = "L2" in value
                    else:
                        op["params"][param] = value
                    break

        return stack

    # -----------------------------
    # Debug Output
    # -----------------------------
    @app.callback(
        Output("debug-output", "children"),
        Input("operation-stack", "data")
    )
    def show_stack(data):
        import json
        return json.dumps(data, indent=2)
