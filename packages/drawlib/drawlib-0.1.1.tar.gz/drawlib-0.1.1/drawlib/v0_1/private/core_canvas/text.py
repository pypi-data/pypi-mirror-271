# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Wrapper of matplotlib text draw

Matplotlib is difficult for just drawing text.
This module wraps it and provides easy to use interfaces.

"""

# pylint: disable=too-many-arguments

from typing import Optional, Tuple
from matplotlib.text import Text

from drawlib.v0_1.private.core.model import TextStyle
from drawlib.v0_1.private.core.util import TextUtil
from drawlib.v0_1.private.util import error_handler
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core_canvas.base import CanvasBase
from drawlib.v0_1.private.arg_validator import ArgValidator


class CanvasTextFeature(CanvasBase):
    def __init__(self) -> None:
        super().__init__()

    @error_handler
    def text(
        self,
        xy: Tuple[float, float],
        text: str,
        angle: Optional[float] = None,
        style: Optional[TextStyle] = None,
    ) -> None:
        """Draw text

        Args:
            xy: left bottom
            text: text
            angle: angle of texts
            style: text style.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_str("text", text)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_textstyle("style", style)

        # apply default if style not specified

        x, y = xy
        style = TextUtil.get_merged_textstyle(style, dtheme.textstyle_get())

        options = TextUtil.get_text_options(style)
        fp = TextUtil.get_font_properties(style)
        bx = TextUtil.get_bbox_dict(style)

        # set default alignment
        if angle is None or angle == 0:
            angle = 0
            if "horizontalalignment" not in options:
                options["horizontalalignment"] = "left"
            if "verticalalignment" not in options:
                options["verticalalignment"] = "bottom"
        else:
            if "horizontalalignment" not in options:
                options["horizontalalignment"] = "center"
            if "verticalalignment" not in options:
                options["verticalalignment"] = "center"

        self._artists.append(
            Text(
                x=x,
                y=y,
                text=text,
                rotation=angle,
                rotation_mode="anchor",
                fontproperties=fp,
                bbox=bx,
                **options,
            )
        )

    @error_handler
    def text_vertical(
        self,
        xy: Tuple[float, float],
        text: str,
        angle: Optional[float] = None,
        style: Optional[TextStyle] = None,
    ) -> None:
        """Draw text vertically.

        Args:
            xy: center, center
            text: text
            angle: angle of texts
            style: text style.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_str("text", text)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_textstyle("style", style)

        # change text

        style = TextUtil.get_merged_textstyle(style, dtheme.textstyle_get())
        vertical_text = "\n".join(text)

        # call text()

        self.text(xy=xy, text=vertical_text, angle=angle, style=style)
