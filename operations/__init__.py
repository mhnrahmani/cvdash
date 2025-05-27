# operations/__init__.py

from .grayscale import render_ui as grayscale_ui
from .blur import render_ui as blur_ui
from .canny import render_ui as canny_ui

operation_renderers = {
    "grayscale": grayscale_ui,
    "blur": blur_ui,
    "canny": canny_ui
}
