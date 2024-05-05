# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Wrapper of matplotlib shape draw

Matplotlib is difficult for just drawing shapes.
This module wraps it and provides easy to use interfaces.

"""

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

from typing import Optional, List, Tuple
import math
from matplotlib.patches import (
    Arc,
    Circle,
    Ellipse,
    Polygon,
    RegularPolygon,
    FancyBboxPatch,
    Wedge,
)
import matplotlib as mpl

from drawlib.v0_1.private.logging import logger
from drawlib.v0_1.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_1.private.core.util import ShapeUtil
from drawlib.v0_1.private.util import error_handler, get_center_and_size
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core_canvas.base import CanvasBase
from drawlib.v0_1.private.arg_validator import ArgValidator


class CanvasPatchesFeature(CanvasBase):
    def __init__(self) -> None:
        super().__init__()

    @error_handler
    def arc(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        theta_begin: int = 0,
        theta_end: int = 360,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw arc.

        Args:
            xy: center of arc.
            width: width of arc.
            height: height of arc.
            theta_begin(optional): where drawing arc start. default is angle 0.0
            theta_end(optional): where drawing arc end. default is angle 360.0
            angle(optional): rotate arc with specified angle
            style(optional): style of arc.
            text(optional): text which is shown at center of arc.
            textstyle(optional): style of text.

        Returns:
            None.

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("width", width)
        ArgValidator.validate_float("height", height)
        ArgValidator.validate_angle("theta_begin", theta_begin)
        ArgValidator.validate_angle("theta_end", theta_end)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        # apply default if style not specified

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_arc_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())
        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        if angle is None:
            angle = 0

        options = ShapeUtil.get_shape_options(style, default_no_line=False)
        self._artists.append(
            Arc(
                xy,
                width=width,
                height=height,
                angle=angle,
                theta1=theta_begin,
                theta2=theta_end,
                **options,
            )
        )
        if text:
            self._artists.append(ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=textstyle))

    @error_handler
    def circle(
        self,
        xy: Tuple[float, float],
        radius: float,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw cicle.

        Args:
            xy: center of circle.
            radius: radius of circle.
            angle(optional): rotate inside text with specified angle
            style(optional): style of circle.
            text(optional): text which is shown at center of arc.
            textstyle(optional): style of text.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("radius", radius)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_circle_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())
        width = radius * 2
        height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(Circle(xy, radius, **options))
        if text:
            self._artists.append(ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=textstyle))

    @error_handler
    def ellipse(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw ellipse

        Args:
            xy: center of ellipse
            width: width of ellipse.
            height: height of ellipse.
            angle(optional): rotate ellipse with specified angle.
            style(optional): style of arc.
            text(optional): text which is shown at center of ellipse.
            textstyle(optional): style of text.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("width", width)
        ArgValidator.validate_float("height", height)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        # apply default if styles are not specified

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_ellipse_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())
        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        if angle is None:
            angle = 0
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(Ellipse(xy, width=width, height=height, angle=angle, **options))
        if text:
            self._artists.append(ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=textstyle))

    @error_handler
    def polygon(
        self,
        xys: List[Tuple[float, float]],
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw polygon.

        Args:
            xys: List of points. [(x1, y1), ...(x_n, y_n)].
            style(optional): style of polygon.
            text(optional): text which is shown at center of ellipse.
            textstyle(optional): style of text.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xys("xys", xys)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_polygon_get())
        style.halign = None
        style.valign = None
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(Polygon(xy=xys, closed=True, **options))

        if text:
            center, (_, _) = get_center_and_size(xys)
            self._artists.append(ShapeUtil.get_shape_text(center, text=text, angle=0, style=textstyle))

    @error_handler
    def regularpolygon(
        self,
        xy: Tuple[float, float],
        radius: float,
        num_vertex: int,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw regular polygon.

        Args:
            xy: center of regular polygon
            radius: radius of regular polygon's vertex.
            num_vertex: number of vertex.
            style(optional): style of regular polygon.
            angle(optional): rotation angle
            text(optional): text which is shown at center of regular polygon.
            textstyle(optional): style of text.

        Returns:
            None

        """

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("radius", radius)
        ArgValidator.validate_int("num_vertex", num_vertex)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_regularpolygon_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())
        width = radius * 2
        height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        if angle is None:
            angle = 0

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            RegularPolygon(
                xy,
                radius=radius,
                numVertices=num_vertex,
                orientation=math.radians(angle),
                **options,
            )
        )
        if text:
            self._artists.append(ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=textstyle))

    @error_handler
    def rectangle(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        r: float = 0.0,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw rectangle

        Args:
            xy: left bottom of rectangle.
            width: width of rounded rectangle.
            height: height of rounded rectangle.
            r(optional): size of R. default is 0.0.
            angle(optional): rotate rectangle with specified angle. Requires Matplotlib's ax to achieve it.
            style(optional): style of rounded rectangle.
            text(optional): text which is shown at center of rounded rectangle.
            textstyle(optional): style of text.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("width", width)
        ArgValidator.validate_float("height", height)
        ArgValidator.validate_float("r", r)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        # apply default if styles are not specified

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_rectangle_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())
        (x, y), style = ShapeUtil.apply_alignment(xy, width, height, angle, style)

        options = ShapeUtil.get_shape_options(style)
        rectangle = FancyBboxPatch(
            (x + r, y + r),
            width - r * 2,
            height - r * 2,
            boxstyle=f"round,pad={r}",
            **options,
        )

        if angle is not None:
            cx = x + width / 2
            cy = y + height / 2
            t2 = mpl.transforms.Affine2D().rotate_deg_around(cx, cy, angle) + self._ax.transData
            rectangle.set_transform(t2)
        else:
            angle = 0.0

        self._artists.append(rectangle)

        if text is not None:
            center_x = x + width / 2
            center_y = y + height / 2
            self._artists.append(
                ShapeUtil.get_shape_text(xy=(center_x, center_y), text=text, angle=angle, style=textstyle)
            )

    @error_handler
    def wedge(
        self,
        xy: Tuple[float, float],
        radius: float,
        width: Optional[float] = None,
        theta_begin: float = 0,
        theta_end: float = 360,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw wedge

        Args:
            xy: center of wedge
            radius: radius of wedge.
            width(optional): length from outer to inner circumference. default is same to radius value.
            theta_begin(optional): where drawing arc start. default is angle 0.0
            theta_end(optional): where drawing arc end. default is angle 360.0
            angle(optional): rotate wedge with specified angle
            style(optional): style of wedge.
            text(optional): text which is shown at center of wedge.
            textstyle(optional): style of text.

        Returns:
            None.

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("radius", radius)
        if width is not None:
            ArgValidator.validate_float("width", width)
        ArgValidator.validate_angle("theta_begin", theta_begin)
        ArgValidator.validate_angle("theta_end", theta_end)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        # apply default if style not specified

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_wedge_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())
        ext_width = radius * 2
        ext_height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, ext_width, ext_height, angle, style, is_default_center=True)
        if angle is None:
            angle = 0

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Wedge(
                center=xy,
                r=radius,
                width=width,  # None makes no hole
                theta1=theta_begin + angle,
                theta2=theta_end + angle,
                **options,
            )
        )

        if text:
            self._artists.append(ShapeUtil.get_shape_text(xy=xy, text=text, angle=angle, style=textstyle))

    @error_handler
    def donuts(
        self,
        xy: Tuple[float, float],
        radius: float,
        width: Optional[float] = None,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw donuts

        Args:
            xy: center of donuts
            radius: radius of donuts.
            width(optional): length from outer to inner circumference. default is same to radius value.
            angle(optional): rotate wedge with specified angle
            style(optional): style of wedge.
            text(optional): text which is shown at center of wedge.
            textstyle(optional): style of text.

        Returns:
            None.

        """
        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_donuts_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())
        self.wedge(
            xy=xy,
            radius=radius,
            width=width,
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    @error_handler
    def fan(
        self,
        xy: Tuple[float, float],
        radius: float,
        theta_begin: float = 0,
        theta_end: float = 180,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw fan

        Args:
            xy: center of fan
            radius: radius of fan.
            theta_begin(optional): where drawing arc start. default is angle 0.0
            theta_end(optional): where drawing arc end. default is angle 360.0
            angle(optional): rotate wedge with specified angle
            style(optional): style of wedge.
            text(optional): text which is shown at center of wedge.
            textstyle(optional): style of text.

        Returns:
            None.

        """

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_fan_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())
        self.wedge(
            xy=xy,
            radius=radius,
            width=None,
            theta_begin=theta_begin,
            theta_end=theta_end,
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )
