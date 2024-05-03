# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Aggregate Canvas features

Drawlib's canvas is complex and holds many methods.
Those features are implemented in CanvasFeature classes.
This module's Canvas aggregate them.

"""

from drawlib.v0_1.private.core_canvas.image import CanvasImageFeature
from drawlib.v0_1.private.core_canvas.line import CanvasLineFeature
from drawlib.v0_1.private.core_canvas.original_polygon import CanvasOriginalPolygonFeature
from drawlib.v0_1.private.core_canvas.original_arrow import CanvasOriginalArrowFeature
from drawlib.v0_1.private.core_canvas.patches import CanvasPatchesFeature
from drawlib.v0_1.private.core_canvas.text import CanvasTextFeature


class Canvas(
    CanvasImageFeature,
    CanvasLineFeature,
    CanvasOriginalPolygonFeature,
    CanvasOriginalArrowFeature,
    CanvasPatchesFeature,
    CanvasTextFeature,
):
    """Drawlib's canvas class"""

    def __init__(self) -> None:
        super().__init__()


__c = Canvas()

# basics
clear = __c.clear
config = __c.config
save = __c.save
shape = __c.shape

# image
image = __c.image

# line
line = __c.line
line_curved = __c.line_curved
line_bezier1 = __c.line_bezier1
line_bezier2 = __c.line_bezier2
lines = __c.lines
lines_bezier = __c.lines_bezier

# original
rhombus = __c.rhombus
trapezoid = __c.trapezoid
parallelogram = __c.parallelogram
triangle = __c.triangle
arrow = __c.arrow
bubblespeech = __c.bubblespeech
star = __c.star
chevron = __c.chevron

# patches
arc = __c.arc
circle = __c.circle
ellipse = __c.ellipse
polygon = __c.polygon
rectangle = __c.rectangle
regularpolygon = __c.regularpolygon
wedge = __c.wedge
donuts = __c.donuts
fan = __c.fan

# text
text = __c.text
text_vertical = __c.text_vertical

# dutil
get_image_zoom_original = __c.get_image_zoom_original
get_image_zoom_from_width = __c.get_image_zoom_from_width
get_charwidth_from_fontsize = __c.get_charwidth_from_fontsize
get_fontsize_from_charwidth = __c.get_fontsize_from_charwidth
