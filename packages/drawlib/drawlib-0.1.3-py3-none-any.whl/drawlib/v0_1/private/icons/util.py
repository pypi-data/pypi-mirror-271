# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawing icon utility module

If you want to draw your specific font icon, please use function dicon

"""

import typing
from drawlib.v0_1.private.core.fonts import FontFile
from drawlib.v0_1.private.core.model import IconStyle, TextStyle
from drawlib.v0_1.private.core.util import IconUtil
from drawlib.v0_1.private.core_canvas.canvas import text, get_fontsize_from_charwidth
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.arg_validator import ArgValidator


def icon(
    xy: typing.Tuple[float, float],
    width: float,
    code: str,
    file: str,
    angle: typing.Optional[float] = None,
    style: typing.Optional[IconStyle] = None,
) -> None:
    """Draw provided iconfont's icon.

    Args:
        code: code point
        font_file: font file path
        x: default align left if angle is not specified. center if specified.
        y: default align bottom if angle is not specified. center if specified.
        width: icon width. icon might have transparent space on itself.
        angle(optional): rotation angle. 0.0 ~ 360.0.
        style(optional): icon style. Allignment etc.

    Returns:
        None

    """

    # validate args

    ArgValidator.validate_xy("xy", xy)
    ArgValidator.validate_float("width", width)
    ArgValidator.validate_str("code", code)
    ArgValidator.validate_str("file", file)
    if angle is not None:
        ArgValidator.validate_angle("angle", angle)
    if style is not None:
        ArgValidator.validate_iconstyle("style", style)

    # set default parameters if not provided

    style = IconUtil.get_merged_style(style, dtheme.iconstyle_get())
    if style.halign is None:
        style.halign = "left" if angle is None else "center"
    if style.valign is None:
        style.valign = "bottom" if angle is None else "center"

    # get good font size from width

    font_size = get_fontsize_from_charwidth(width)

    # convert IconStyle to TextStyle
    textstyle = TextStyle(
        color=style.color,
        size=font_size,
        font=FontFile(file),
        halign=style.halign,
        valign=style.valign,
    )

    # draw icon as text
    text(xy=xy, text=code, angle=angle, style=textstyle)
