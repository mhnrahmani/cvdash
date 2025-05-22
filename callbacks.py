# callbacks.py
import dash
from dash import Input, Output, State
import base64
import io
from PIL import Image
import numpy as np
import cv2

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
        
        # Strip the base64 header
        content_type, content_string = contents.split(',')
        
        # Decode the image
        img_data = base64.b64decode(content_string)
        img = Image.open(io.BytesIO(img_data))
        
        # Convert to a format OpenCV can work with (NumPy array)
        img = np.array(img)
        
        # Optionally, convert to grayscale (or handle as needed)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # Store image in dcc.Store
        return "Image successfully uploaded!", content_string

    @app.callback(
        Output("image-preview", "src"),
        Input("original-image-store", "data"),
        prevent_initial_call=True
    )
    def update_image_display(image_base64):
        if image_base64 is None:
            return None
        return f"data:image/png;base64,{image_base64}"
