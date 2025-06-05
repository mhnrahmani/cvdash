# operations/__init__.py

from .grayscale import render_ui as grayscale_ui
from .blur import render_ui as blur_ui
from .canny import render_ui as canny_ui
from .morphology import render_ui as morphology_ui
from .adaptive_threshold import render_ui as adaptive_threshold_ui

operation_renderers = {
    "grayscale": grayscale_ui,
    "blur": blur_ui,
    "canny": canny_ui,
    "morphology": morphology_ui,
    "adaptive_threshold": adaptive_threshold_ui
}
