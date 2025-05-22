# operations/__init__.py

from .blur import render_ui as blur_ui
from .canny import render_ui as canny_ui

operation_renderers = {
    "blur": blur_ui,
    "canny": canny_ui
}
