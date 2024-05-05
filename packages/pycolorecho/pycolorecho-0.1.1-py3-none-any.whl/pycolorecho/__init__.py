__all__ = [
    "RESET",
    "Layer",
    "Color",
    "TextBackgroundColor",
    "TextColor",
    "TextEffect",
    "TextCase",
    "ColorMapper",
    "echo",
    "is_colorization_supported",
    "is_true_color_supported",
    "get_colorized_message",
    "get_colorized_message_by_regex_pattern",
    "get_colorized_message_by_mappings",
    "HEXCodes",
    "__author__",
    "__description__",
    "__name__",
    "__version__"
]
__author__ = "coldsofttech"
__description__ = """
Simple Python package for colorized terminal output
"""
__name__ = "pycolorecho"
__version__ = "0.1.1"

from pycolorecho.__main__ import RESET, Layer, Color, TextBackgroundColor, TextColor, TextEffect, TextCase, \
    ColorMapper, echo, HEXCodes, is_colorization_supported, is_true_color_supported, get_colorized_message, \
    get_colorized_message_by_regex_pattern, get_colorized_message_by_mappings
