# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Internal utility functions for drawing matplotlib objects

drawlib's style are different to matplotlib's style.
This module provides format converter utilities.
It is not designed to be used by library users.

"""

import math
from typing import Optional, Dict, Any, Union, Tuple
from copy import deepcopy
from matplotlib.font_manager import FontProperties
from matplotlib.text import Text

from drawlib.v0_1.private.download import download_if_not_exist
from drawlib.v0_1.private.core.colors import Colors
from drawlib.v0_1.private.core.model import (
    IconStyle,
    IconStyleDefault,
    ImageStyle,
    ImageStyleDefault,
    LineStyle,
    LineStyleDefault,
    LineArrowStyle,
    LineArrowStyleDefault,
    ShapeStyle,
    ShapeStyleDefault,
    ShapeTextStyle,
    ShapeTextStyleDefault,
    TextStyle,
    TextStyleDefault,
)
from drawlib.v0_1.private.core.fonts import (
    FontBase,
    FontFile,
)
from drawlib.v0_1.private.core.theme import dtheme


class IconUtil:

    @staticmethod
    def get_merged_style(
        primary: Optional[IconStyle],
        secondary: IconStyle,
    ) -> IconStyle:
        if primary is None:
            primary = IconStyle()
        else:
            primary = deepcopy(primary)

        # apply secondary (theme)
        if primary.style is None:
            primary.style = secondary.style
        if primary.color is None:
            primary.color = secondary.color
        if primary.alpha is None:
            primary.alpha = secondary.alpha
        if primary.halign is None:
            primary.halign = secondary.halign
        if primary.valign is None:
            primary.valign = secondary.valign

        # apply system default
        if primary.style is None:
            primary.style = IconStyleDefault.style
        if primary.color is None:
            primary.color = IconStyleDefault.color
        if primary.alpha is None:
            primary.alpha = IconStyleDefault.alpha
        if primary.halign is None:
            primary.halign = IconStyleDefault.haligh
        if primary.valign is None:
            primary.valign = IconStyleDefault.valign

        return primary


class ImageUtil:

    @staticmethod
    def get_merged_style(
        primary: Optional[ImageStyle],
        secondary: ImageStyle,
    ) -> IconStyle:
        if primary is None:
            primary = ImageStyle()
        else:
            primary = deepcopy(primary)

        # apply secondary (theme)
        if primary.lstyle is None:
            primary.lstyle = secondary.lstyle
        if primary.lcolor is None:
            primary.lcolor = secondary.lcolor
        if primary.lwidth is None:
            primary.lwidth = secondary.lwidth
        if primary.halign is None:
            primary.halign = secondary.halign
        if primary.valign is None:
            primary.valign = secondary.valign

        # apply system default
        if primary.lstyle is None:
            primary.lstyle = ImageStyleDefault.lstyle
        if primary.lcolor is None:
            primary.lcolor = ImageStyleDefault.lcolor
        if primary.lwidth is None:
            primary.lwidth = ImageStyleDefault.lwidth
        if primary.halign is None:
            primary.halign = ImageStyleDefault.halign
        if primary.valign is None:
            primary.valign = ImageStyleDefault.valign

        return primary


class ColorUtil:

    @staticmethod
    def get_mplot_rgba(
        rgb_or_rgba: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        alpha: Optional[float] = None,
    ) -> Tuple[float, float, float, float]:
        """Convert 0~255 RGB/RGBA to 0.0 ~ 1.0 RGBA

        drawlib prefere 0~255 RGB/RGBA.
        matplotlib uses 0.0~1.0 RGB/RGBA.

        This function provides converter from drawlib format to matplotlib format.
        Alpha is determined this way.

        1. If having alpha arg, use it
        2. If original data is RGBA, use its alpha value
        3. Set alpha 1.0

        Args:
            rgb_or_rgba: 0~255 for RGB. 0.0 ~ 1.0 for A if having alpha.
            alpha: Over write alpha value

        Returns:
            Tuple[float, float, float, float]: matplotlib's RGBA format.

        """

        r = round(rgb_or_rgba[0] / 255, 5)
        g = round(rgb_or_rgba[1] / 255, 5)
        b = round(rgb_or_rgba[2] / 255, 5)

        if alpha is not None:
            a = alpha
        elif len(rgb_or_rgba) == 3:
            a = 1.0
        else:
            a = rgb_or_rgba[3]

        return (r, g, b, a)

    @staticmethod
    def get_hexrgb(
        rgb_or_rgba: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
    ) -> str:
        r = rgb_or_rgba[0]
        g = rgb_or_rgba[1]
        b = rgb_or_rgba[2]
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("RGB values must be in the range 0 to 255.")
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        return hex_color

    @staticmethod
    def get_rgba_from_hex(hex_color: str) -> Tuple[int, int, int, float]:
        """
        Convert a hexadecimal color code to RGBA values.

        Args:
            hex_color (str): The hexadecimal color code (e.g., "#FF5733" or "#FFF").

        Returns:
            tuple[int, int, int, float]: A tuple containing the RGBA values (0-255 for R, G, B and 0.0-1.0 for A).
        """

        # Remove the '#' prefix if present
        hex_color = hex_color.lstrip("#")

        # Determine the length of the hex color code
        hex_length = len(hex_color)

        # Convert the hex code to RGB values
        if hex_length == 3:  # Short hex format (#RGB)
            r = int(hex_color[0] * 2, 16)
            g = int(hex_color[1] * 2, 16)
            b = int(hex_color[2] * 2, 16)
            a = 1.0
        elif hex_length in (6, 8):  # Full hex format (#RRGGBB)
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            if hex_length == 8:  # With alpha
                a = int(hex_color[6:8], 16)
            else:
                a = 1.0
        else:
            raise ValueError("Invalid hex color code format")

        return (r, g, b, a)


class LineUtil:

    @staticmethod
    def get_merged_style(
        primary: Union[LineStyle, LineArrowStyle],
        secondary_linestyle: LineStyle,
        secondary_linearrowstyle: LineArrowStyle,
    ) -> Union[LineStyle, LineArrowStyle]:
        if primary is None:
            primary = LineStyle()
        else:
            primary = deepcopy(primary)

        if isinstance(primary, LineStyle):
            secondary = secondary_linestyle

            # apply secondary (theme)
            if primary.width is None:
                primary.width = secondary.width
            if primary.color is None:
                primary.color = secondary.color
            if primary.style is None:
                primary.style = secondary.style
            if primary.alpha is None:
                primary.alpha = secondary.alpha

            # apply system default
            if primary.width is None:
                primary.width = LineStyleDefault.width
            if primary.color is None:
                primary.color = LineStyleDefault.color
            if primary.style is None:
                primary.style = LineStyleDefault.style
            if primary.alpha is None:
                primary.alpha = LineStyleDefault.alpha

            return primary

        # apply secondary (theme)
        secondary = secondary_linearrowstyle
        if primary.lstyle is None:
            primary.lstyle = secondary.lstyle
        if primary.lwidth is None:
            primary.lwidth = secondary.lwidth
        if primary.hstyle is None:
            primary.hstyle = secondary.hstyle
        if primary.hscale is None:
            primary.hscale = secondary.hscale
        if primary.color is None:
            primary.color = secondary.color
        if primary.alpha is None:
            primary.alpha = secondary.alpha

        # apply system default
        if primary.lstyle is None:
            primary.lstyle = LineArrowStyleDefault.lstyle
        if primary.lwidth is None:
            primary.lwidth = LineArrowStyleDefault.lwidth
        if primary.hstyle is None:
            primary.hstyle = LineArrowStyleDefault.hstyle
        if primary.hscale is None:
            primary.hscale = LineArrowStyleDefault.hscale
        if primary.color is None:
            primary.color = LineArrowStyleDefault.color
        if primary.alpha is None:
            primary.alpha = LineArrowStyleDefault.alpha

        return primary

    @staticmethod
    def get_fancyarrowpatch_options(
        style: Union[LineStyle, LineArrowStyle, None] = None,
    ) -> Dict[str, Any]:
        """Convert drawlib's LineStyle to matplotlib's line options

        Matplotlib handles line style at its args.
        This module convert drawlib's LineStyle to dict
        which fit to matplotlib's function.

        At caller side, please apply options(return value) as
        ``Line2D(arg1, ..., **options)``.
        It will apply LineStyle's style to matplotlib's function.

        Args:
            style: LineStyle or None

        Returns:
            dict: arg None makes {}. LineStyle makes appropriate options dict.

        """

        if style is None:
            return {"arrowstyle": "-"}

        color = None if style.color is None else ColorUtil.get_mplot_rgba(style.color)

        if isinstance(style, LineStyle):
            options = {
                "linewidth": style.width,
                "linestyle": style.style,
                "color": color,
                "alpha": style.alpha,
                "arrowstyle": "-",
            }
        elif isinstance(style, LineArrowStyle):
            options = {
                "linewidth": style.lwidth,
                "linestyle": style.lstyle,
                "color": color,
                "alpha": style.alpha,
                "arrowstyle": style.hstyle,
                "mutation_scale": style.hscale,
            }
        else:
            raise ValueError()

        return _get_dict_value_none_keys_removed(options)


class ShapeUtil:
    @staticmethod
    def apply_alignment(
        xy: Tuple[float, float],
        width: float,
        height: float,
        angle: Optional[float],
        style: ShapeStyle,
        is_default_center: bool = False,
    ) -> Tuple[Tuple[float, float], ShapeStyle]:

        x, y = xy
        if angle is None:
            if is_default_center:
                if style.halign is None:
                    style.halign = "center"
                if style.valign is None:
                    style.valign = "center"
            else:
                if style.halign is None:
                    style.halign = "left"
                if style.valign is None:
                    style.valign = "bottom"
        else:
            if style.halign is None:
                style.halign = "center"
            if style.valign is None:
                style.valign = "center"

        if is_default_center:
            if style.halign == "left":
                x = x + width / 2
            if style.halign == "right":
                x = x - width / 2
            if style.valign == "bottom":
                y = y + height / 2
            if style.valign == "top":
                y = y - height / 2
        else:
            if style.halign == "center":
                x = x - width / 2
            if style.halign == "right":
                x = x - width
            if style.valign == "center":
                y = y - height / 2
            if style.valign == "top":
                y = y - height

        return (x, y), style

    @staticmethod
    def get_shape_text(
        xy: Tuple[float, float],
        angle: Optional[float],
        text: str,
        style: Optional[ShapeTextStyle] = None,
    ) -> Text:
        """Get text object which is drawn inside shape.

        Few shape objects can have text in its center.
        This function helps creating text object inside shape.
        Specifically, try to align to center of shapes.

        Args:
            x: center of shape. center of text.
            y: center of shape. center of text.
            text: shown text
            angle(option): angle of shape. angle of text.
            style(option): style of text

        Returns:
            matplotlib.text.Text: shape center text

        """

        if style is None:
            style = ShapeTextStyle()

        shape_angle = angle
        if shape_angle is None:
            shape_angle = 0.0

        if style.angle is not None:
            text_angle = style.angle
        else:
            text_angle = shape_angle
        if style.flip is not None and style.flip:
            text_angle = (text_angle + 180) % 360

        x, y = xy
        if style.xy_shift is not None:
            x_shift, y_shift = style.xy_shift
            if shape_angle == 0:
                x += x_shift
                y += y_shift
            else:
                angle_rad = math.radians(shape_angle)
                rotated_x_shift = x_shift * math.cos(angle_rad) - y_shift * math.sin(angle_rad)
                rotated_y_shift = x_shift * math.sin(angle_rad) + y_shift * math.cos(angle_rad)
                x += rotated_x_shift
                y += rotated_y_shift

        # only check color. ignore alignment
        options = TextUtil.get_text_options(style)
        if "horizontalalignment" in options:
            del options["horizontalalignment"]
        if "verticalalignment" in options:
            del options["verticalalignment"]

        return Text(
            x,
            y,
            text,
            rotation=text_angle,
            rotation_mode="anchor",
            horizontalalignment="center",
            verticalalignment="center",
            fontproperties=TextUtil.get_font_properties(style),
            **options,
        )

    @staticmethod
    def get_merged_shapestyle(
        primary: Optional[ShapeStyle],
        secondary: ShapeStyle,
    ) -> ShapeStyle:
        if primary is None:
            primary = ShapeStyle()
        else:
            primary = deepcopy(primary)

        if primary.halign is None:
            primary.halign = secondary.halign
        if primary.valign is None:
            primary.valign = secondary.valign
        if primary.lwidth is None:
            primary.lwidth = secondary.lwidth
        if primary.lcolor is None:
            primary.lcolor = secondary.lcolor
        if primary.lstyle is None:
            primary.lstyle = secondary.lstyle
        if primary.fcolor is None:
            primary.fcolor = secondary.fcolor
        if primary.alpha is None:
            primary.alpha = secondary.alpha

        if primary.halign is None:
            primary.halign = ShapeStyleDefault.halign
        if primary.valign is None:
            primary.valign = ShapeStyleDefault.valign
        if primary.lwidth is None:
            primary.lwidth = ShapeStyleDefault.lwidth
        if primary.lcolor is None:
            primary.lcolor = ShapeStyleDefault.lcolor
        if primary.lstyle is None:
            primary.lstyle = ShapeStyleDefault.lstyle
        if primary.fcolor is None:
            primary.fcolor = ShapeStyleDefault.fcolor
        if primary.alpha is None:
            primary.alpha = ShapeStyleDefault.alpha

        return primary

    @staticmethod
    def get_merged_shapetextstyle(
        primary: Optional[ShapeTextStyle],
        secondary: ShapeTextStyle,
    ) -> TextStyle:
        if primary is None:
            primary = ShapeTextStyle()
        else:
            primary = deepcopy(primary)

        if primary.color is None:
            primary.color = secondary.color
        if primary.size is None:
            primary.size = secondary.size
        if primary.halign is None:
            primary.halign = secondary.halign
        if primary.valign is None:
            primary.valign = secondary.valign
        if primary.font is None:
            primary.font = secondary.font
        if primary.alpha is None:
            primary.alpha = secondary.alpha

        if primary.color is None:
            primary.color = ShapeTextStyleDefault.color
        if primary.size is None:
            primary.size = ShapeTextStyleDefault.size
        if primary.halign is None:
            primary.halign = ShapeTextStyleDefault.halign
        if primary.valign is None:
            primary.valign = ShapeTextStyleDefault.valign
        if primary.font is None:
            primary.font = ShapeTextStyleDefault.font
        if primary.alpha is None:
            primary.alpha = ShapeTextStyleDefault.alpha

        return primary

    @staticmethod
    def get_shape_options(
        style: Optional[ShapeStyle] = None,
        default_no_line: bool = True,
    ) -> Dict[str, Any]:
        """Convert drawlib's ShapeStyle to matplotlib's patches(shape) options

        Matplotlib handles shape style at its args.
        This module convert drawlib's ShapeStyle to dict
        which fit to matplotlib's function.

        At caller side, please apply options(return value) as
        ``Circle(arg1, arg2, **options)``.
        It will apply TextStyle's style to matplotlib's function.

        Args:
            style: ShapeStyle or None

        Returns:
            dict: arg None makes {}. ShapeStyle makes appropriate options dict.

        """

        if style is None:
            if default_no_line:
                return {"linewidth": 0}
            return {}

        lcolor = None if style.lcolor is None else ColorUtil.get_mplot_rgba(style.lcolor)
        fcolor = None if style.fcolor is None else ColorUtil.get_mplot_rgba(style.fcolor)

        # halign, valign will be used on shape. They are not in options.
        options = {
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.lstyle,
            "linewidth": style.lwidth,
            "alpha": style.alpha,
        }

        if options["linewidth"] is None:
            if default_no_line:
                options["linewidth"] = 0

        return _get_dict_value_none_keys_removed(options)


class TextUtil:

    @staticmethod
    def get_merged_textstyle(
        primary: Optional[TextStyle],
        secondary: TextStyle,
    ) -> TextStyle:
        if primary is None:
            primary = TextStyle()
        else:
            primary = deepcopy(primary)

        if primary.color is None:
            primary.color = secondary.color
        if primary.size is None:
            primary.size = secondary.size
        if primary.halign is None:
            primary.halign = secondary.halign
        if primary.valign is None:
            primary.valign = secondary.valign
        if primary.font is None:
            primary.font = secondary.font
        if primary.alpha is None:
            primary.alpha = secondary.alpha
        if primary.bgalpha is None:
            primary.bgalpha = secondary.bgalpha
        if primary.bglcolor is None:
            primary.bglcolor = secondary.bglcolor
        if primary.bglstyle is None:
            primary.bglstyle = secondary.bglstyle
        if primary.bglwidth is None:
            primary.bglwidth = secondary.bglwidth
        if primary.bgfcolor is None:
            primary.bgfcolor = secondary.bgfcolor

        if primary.color is None:
            primary.color = TextStyleDefault.color
        if primary.size is None:
            primary.size = TextStyleDefault.size
        if primary.halign is None:
            primary.halign = TextStyleDefault.halign
        if primary.valign is None:
            primary.valign = TextStyleDefault.valign
        if primary.font is None:
            primary.font = TextStyleDefault.font
        if primary.alpha is None:
            primary.alpha = TextStyleDefault.alpha
        if primary.bgalpha is None:
            primary.bgalpha = TextStyleDefault.bgalpha
        if primary.bgfcolor is None:
            primary.bgfcolor = TextStyleDefault.bgfcolor
        if primary.bglcolor is not None or primary.bglstyle is not None or primary.bglwidth is not None:
            if primary.bglcolor is None:
                primary.bglcolor = TextStyleDefault.bglcolor
            if primary.bglstyle is None:
                primary.bglstyle = TextStyleDefault.bglstyle
            if primary.bglwidth is None:
                primary.bglwidth = TextStyleDefault.bglwidth

        return primary

    @staticmethod
    def get_text_options(
        style: Union[TextStyle, ShapeTextStyle, None],
    ) -> Dict[str, Any]:
        """Convert drawlib's TextStyle to matplotlib's text options

        Matplotlib handles text style at its args.
        This module convert drawlib's TextStyle to dict
        which fit to matplotlib's function.

        At caller side, please apply options(return value) as
        ``Text(arg1, ..., **options)``.
        It will apply TextStyle's style to matplotlib's function.

        Args:
            style: TextStyle or None

        Returns:
            dict: arg None makes {}. TextStyle makes appropriate options dict.

        """

        if style is None:
            return {}

        # convert rgb -> matplot rgb
        color = None if style.color is None else ColorUtil.get_mplot_rgba(style.color)

        options = {
            "color": color,
            "horizontalalignment": style.halign,
            "verticalalignment": style.valign,
        }

        return _get_dict_value_none_keys_removed(options)

    @staticmethod
    def get_font_properties(
        style: Union[TextStyle, ShapeTextStyle, None],
    ) -> Optional[FontProperties]:
        """Create matplotlib's FontProperties from TextStyle

        Arg:
            style: TextStyle or None

        Returns:
            Optional[FontProperties]: return None if arg is None.

        """

        if style is None or isinstance(style, TextStyle):
            default = dtheme.textstyle_get()
            if default.size is None:
                default.size = TextStyleDefault.size
            if default.font is None:
                default.font = TextStyleDefault.font

        if isinstance(style, ShapeTextStyle):
            default = dtheme.shapetextstyle_get()
            if default.size is None:
                default.size = ShapeTextStyleDefault.size
            if default.font is None:
                default.font = ShapeTextStyleDefault.font

        DEFAULT_SIZE = default.size
        DEFAULT_FONT = default.font

        # use user font file

        if isinstance(style.font, FontFile):
            if style.size is None:
                style.size = DEFAULT_SIZE
            return FontProperties(size=style.size, fname=style.font.file)

        # use default font

        file_path, download_url, md5_hash = DEFAULT_FONT.value
        download_if_not_exist(file_path=file_path, download_url=download_url, md5_hash=md5_hash)

        if style is None:
            return FontProperties(size=DEFAULT_SIZE, fname=file_path)

        if style.font is None:
            if style.size is None:
                style.size = DEFAULT_SIZE
            return FontProperties(size=style.size, fname=file_path)

        # use specified font

        if isinstance(style.font, FontBase):
            # get True for all BaseFont subclasses
            if style.size is None:
                style.size = DEFAULT_SIZE

            file_path, download_url, md5_hash = style.font.value
            download_if_not_exist(file_path=file_path, download_url=download_url, md5_hash=md5_hash)
            return FontProperties(size=style.size, fname=file_path)

        raise ValueError(f"font type {type(style.font)} is not supported")

    @staticmethod
    def get_bbox_dict(
        style: Optional[TextStyle] = None,
    ) -> Optional[Dict[str, Any]]:
        """Convert drawlib's TextStyle to matplotlib's text background options.

        Matplotlib handles text background style at its arg ``bbox`` as dict.
        This module convert drawlib's TextBackgroundStyle to dict
        which fit to matplotlib's function.

        Note:
            ``{}`` doesn't mean no style at matplotlib's bbox.
            If you want have no style, need to apply ``None``.

        At caller side please provide return value to arg ``bbox``.
        It is not same to other style ways. Please be careful.

        Args:
            style: TextBackgroundStyle or None

        Returns:
            Optional[dict]: arg None makes None. TextBackgroundStyle makes appropriate bbox dict.

        """

        # {} doesn't mean no style.
        # requires returning None when no style.

        if style is None:
            return None

        all_none = True
        for e in [style.bgfcolor, style.bglcolor, style.bglstyle]:
            if e is not None:
                all_none = False
        if all_none:
            return None

        # background exist

        lcolor = None if style.bglcolor is None else ColorUtil.get_mplot_rgba(style.bglcolor)
        fcolor = None if style.bgfcolor is None else ColorUtil.get_mplot_rgba(style.bgfcolor)

        if lcolor is None:
            lcolor = Colors.Transparent
        if fcolor is None:
            fcolor = Colors.Transparent

        bbox_dict = {
            "boxstyle": "square",
            "facecolor": fcolor,
            "edgecolor": lcolor,
            "linestyle": style.bglstyle,
            "linewidth": style.bglwidth,
            "alpha": style.bgalpha,
        }
        if bbox_dict["linewidth"] is None:
            bbox_dict["linewidth"] = 0

        return _get_dict_value_none_keys_removed(bbox_dict)


def _get_dict_value_none_keys_removed(options: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in options.items() if value is not None}
