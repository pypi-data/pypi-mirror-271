# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Wrapper of matplotlib image draw

Matplotlib is difficult for just drawing image.
This module wraps it and provides easy to use interfaces.

"""

from typing import Optional, Union, Any, Tuple
from PIL.Image import Image
import numpy
from matplotlib import offsetbox
from drawlib.v0_1.private.core.model import ImageStyle, ShapeStyle
from drawlib.v0_1.private.util import error_handler
from drawlib.v0_1.private.core.dimage import Dimage
from drawlib.v0_1.private.core.colors import Colors
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core.util import ImageUtil
from drawlib.v0_1.private.core_canvas.patches import CanvasPatchesFeature
from drawlib.v0_1.private.logging import logger
from drawlib.v0_1.private.arg_validator import ArgValidator


class CanvasImageFeature(CanvasPatchesFeature):
    def __init__(self) -> None:
        super().__init__()

    @error_handler
    def image(
        self,
        xy: Tuple[float, float],
        width: float,
        image: Union[str, Image, Dimage],
        angle: Optional[float] = None,
        style: Optional[ImageStyle] = None,
    ) -> None:
        """Draw image

        Args:
            xy: Left bottom of image
            width: Width of image. Height is calculated automatically.
            image: Image path or image itself.
            angle: Rotation degree.
            style: Image style.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_int("width", width)
        ArgValidator.validate_image_objects("image", image)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_imagestyle("style", style)

        # standadize

        x, y = xy
        pimg = Dimage(image, copy=True)
        image_width, image_height = pimg.get_image_size()
        height = image_height / image_width * width
        zoom = self.get_image_zoom_from_width(pimg, width)

        # set default alignment if not specified
        style = ImageUtil.get_merged_style(style, dtheme.imagestyle_get())
        if style.halign is None:
            if angle is None:
                style.halign = "left"
            else:
                style.halign = "center"
        if style.valign is None:
            if angle is None:
                style.valign = "bottom"
            else:
                style.valign = "center"

        # rotate image
        if angle is not None:
            has_wrong_style = False
            if style.halign != "center":
                has_wrong_style = True
                style.halign = "center"
            if style.valign != "center":
                has_wrong_style = True
                style.valign = "center"
            if has_wrong_style:
                logger.warn("image() with angle only accepts ShapeTextStyle alignment center.")
            pimg = pimg.rotate(angle)

        # xy shift
        if style.halign != "center" or style.valign != "center":
            #
            # memo. calculation
            # (image_width / 2) * (zoom / 0.72) * (canvas_width / 100)
            #   -> image_width * zoom * self._width / 1440

            image_width, image_height = pimg.get_image_size()
            x_shift = image_width * zoom * self._width / 1440
            y_shift = image_height * zoom * self._width / 1440

            if style.halign == "left":
                x += x_shift
            elif style.halign == "center":
                ...
            elif style.halign == "right":
                x -= x_shift
            else:
                raise ValueError(f'halign "{style.halign}" is not supported.')

            if style.valign == "bottom":
                y += y_shift
            elif style.valign == "center":
                ...
            elif style.valign == "top":
                y -= y_shift
            else:
                raise ValueError(f'valign "{style.valign}" is not supported.')

        # create image drawing object
        pil_image = pimg.get_pil_image()
        im = numpy.array(pil_image)
        imagebox = offsetbox.OffsetImage(im, zoom=zoom)
        ab = offsetbox.AnnotationBbox(imagebox, (x, y), frameon=False)

        # draw later
        self._artists.append(ab)

        # border
        if style.lwidth is None:
            return
        if style.lwidth == 0:
            return
        shapestyle = ShapeStyle(
            halign=style.halign,
            valign=style.valign,
            lstyle=style.lstyle,
            lwidth=style.lwidth,
            lcolor=style.lcolor,
            fcolor=Colors.Transparent,
        )
        self.rectangle(xy=xy, width=width, height=height, angle=angle, style=shapestyle)
