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

import math
from typing import Optional, List, Tuple, Literal
from matplotlib.text import Text
from matplotlib.patches import Polygon
from matplotlib.path import Path
from matplotlib.patches import PathPatch

from drawlib.v0_1.private.util import error_handler, minus_2points
from drawlib.v0_1.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_1.private.core.util import ShapeUtil
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core_canvas.base import CanvasBase
from drawlib.v0_1.private.arg_validator import ArgValidator


class CanvasOriginalPolygonFeature(CanvasBase):
    def __init__(self) -> None:
        super().__init__()

    @error_handler
    def bubblespeech(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        tail_edge: Literal["left", "top", "right", "bottom"],
        tail_start: float,
        tail_vertex: Tuple[float, float],
        tail_width: float,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw bubble speech.

        Almost same to rectangle. But having tail.

        Args:
            xy: always left bottom. Aligns are ignored.
            width: width of rectangle
            height: height of rectangle
            tail_edge: which edge tail exist.
            tail_start: ratio where tail start
            tail_vertex: vertex xy of tail.
            tail_width: ratio where tail end (start + width)
            style: ShapeStyle
            text: text
            textstyle: ShapeTextStyle

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("width", width)
        ArgValidator.validate_float("height", height)
        if tail_edge not in ["left", "top", "right", "bottom"]:
            raise ValueError('Arg "tail_edge" must be one of ["left", "top", "right", "bottom"].')
        ArgValidator.validate_float("tail_start", tail_start)
        ArgValidator.validate_xy("tail_vertex", tail_vertex)
        ArgValidator.validate_float("tail_width", tail_width)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        if tail_start + tail_width > 1.0:
            raise ValueError(f"Sum of tail_start={tail_start} and tail_width={tail_width} must be less than 1.0")

        x, y = xy
        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_bubblespeech_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())

        xys = []
        xys.append((x, y))  # left bottom
        if tail_edge == "left":
            xys.append((x, y + height * tail_start))
            xys.append(tail_vertex)
            xys.append((x, y + height * (tail_start + tail_width)))
        xys.append((x, y + height))  # left top
        if tail_edge == "top":
            xys.append((x + width * tail_start, y + height))
            xys.append(tail_vertex)
            xys.append((x + width * (tail_start + tail_width), y + height))
        xys.append((x + width, y + height))  # right top
        if tail_edge == "right":
            xys.append((x + width, y + height * (tail_start + tail_width)))
            xys.append(tail_vertex)
            xys.append((x + width, y + height * tail_start))
        xys.append((x + width, y))  # right bottom
        if tail_edge == "bottom":
            xys.append((x + width * (tail_start + tail_width), y))
            xys.append(tail_vertex)
            xys.append((x + width * tail_start, y))

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(Polygon(xy=xys, closed=True, **options))

        if text:
            center_x = x + width / 2
            center_y = y + height / 2
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(center_x, center_y),
                    text=text,
                    angle=0,
                    style=textstyle,
                )
            )

    def triangle(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        topvertex_start: Optional[float] = None,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw triangle.

        Args:
            xy: default left bottom.
            width: width of triangle bottom
            height: height of traiangle
            topvertex_start(option): topvertex location from left side. default is center.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("width", width)
        ArgValidator.validate_float("height", height)
        if topvertex_start is not None:
            ArgValidator.validate_float("topvertex_width", topvertex_start)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        # apply default if styles are not specified

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_triangle_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())

        if topvertex_start is None:
            topvertex_start = width / 2
        p1 = (0, 0)
        p2 = (topvertex_start, height)
        p3 = (width, 0)
        self.shape(
            xy=xy,
            path_points=[p1, p2, p3],
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    def parallelogram(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        corner_angle: float,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ):
        """Draw parallelogram.

        Args:
            xy: default left bottom.
            width: width of triangle bottom
            height: height of traiangle
            corner_angle: left bottom corner angle.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("width", width)
        ArgValidator.validate_float("height", height)
        ArgValidator.validate_float("corner_angle", corner_angle)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        # apply default if styles are not specified

        def calculate_parallelogram_lefttop_coordinate():
            angle_rad = math.radians(corner_angle)
            x = height / math.tan(angle_rad)
            return x, height

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_parallelogram_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())

        p1 = (0, 0)
        p2 = calculate_parallelogram_lefttop_coordinate()
        p3 = (p2[0] + width, height)
        p4 = (width, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4],
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    def trapezoid(
        self,
        xy: Tuple[float, float],
        height: float,
        bottom_width: float,
        top_width: float,
        top_start: Optional[float] = None,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ):
        """Draw triangle.

        Args:
            xy: default left bottom.
            height: height of traiangle
            bottom_width: width of bottom
            top_width: width of top
            top_start(optional): start point of top. Default makes top center.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("height", height)
        ArgValidator.validate_float("bottom_width", bottom_width)
        ArgValidator.validate_float("top_width", top_width)
        if top_start is not None:
            ArgValidator.validate_float("topvertex_width", top_start)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        # apply default if styles are not specified

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_trapezoid_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())

        if top_start is None:
            top_start = (bottom_width - top_width) / 2
        p1 = (0, 0)
        p2 = (top_start, height)
        p3 = (top_start + top_width, height)
        p4 = (bottom_width, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4],
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    def rhombus(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ):
        """Draw rhombus.

        Args:
            xy: default left bottom.
            width: width of rhombus
            height: height of rhombus
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
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

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_rhombus_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())

        p1 = (0, height / 2)
        p2 = (width / 2, height)
        p3 = (width, height / 2)
        p4 = (width / 2, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4],
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    def chevron(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        corner_angle: float,
        mirror: bool = False,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw chevron.

        Vertex is right on default. Provide True for mirror makes left side vertex.

        Args:
            xy: default left bottom.
            width: width of bottom of chevron
            height: height of chevron
            corner_angle: left bottom corner angle. 0.0 ~ 90.0.
            mirror(optional): make vertex left side.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_float("width", width)
        ArgValidator.validate_float("height", height)
        ArgValidator.validate_float("corner_angle", corner_angle)
        if not 0.0 <= corner_angle <= 90.0:
            raise ValueError(f"corner_angles supports 0.0 ~ 90.0. But {corner_angle} is given.")
        ArgValidator.validate_bool("mirror", mirror)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_chevron_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())

        if mirror:
            corner_angle = 180 - corner_angle

        p1 = (0, 0)
        p2x = height / 2 * math.cos(math.radians(corner_angle))
        p2 = (p2x, height / 2)
        p3 = (0, height)
        p4 = (width, height)
        p5 = (width + p2x, height / 2)
        p6 = (width, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4, p5, p6],
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    def star(
        self,
        xy: Tuple[float, float],
        num_vertex: int,
        radius_ext: float,
        radius_int: float,
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
    ) -> None:
        """Draw star.

        Args:
            xy: default center, center.
            num_vertex: numver of external vertex. 3 ~.
            radius_ext: radius of external vertex.
            radius_int: raidus of internal vertex.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_int("num_vertex", num_vertex)
        ArgValidator.validate_float("radius_ext", radius_ext)
        ArgValidator.validate_float("radius_int", radius_int)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)

        if num_vertex < 3:
            raise ValueError()
        if radius_ext < radius_int:
            raise ValueError()

        # helper

        def get_rotate_point(x: float, y: float, angle: Optional[float], move_x: float, move_y: float):
            if angle is None:
                angle = 0.0
            angle_rad = math.radians(angle)
            x_rotated = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            y_rotated = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            return x_rotated + move_x, y_rotated + move_y

        # apply default style

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_star_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())

        # calculate points

        points = []
        start_angle = math.pi / 2
        for i in range(2 * num_vertex):
            r = radius_ext if i % 2 == 0 else radius_int
            point_angle = start_angle + i * 2 * math.pi / (2 * num_vertex)
            x = r * math.cos(point_angle)
            y = r * math.sin(point_angle)
            points.append((x, y))

        # move x, y which fit to alignment

        width = radius_ext * 2
        height = radius_ext * 2
        x, y = xy
        x -= width / 2
        y -= height / 2
        xy = (x, y)
        ((x, y), style) = ShapeUtil.apply_alignment(
            xy,
            width,
            height,
            angle,
            style,
            is_default_center=True,
        )

        # shift

        cx = x + width / 2
        cy = y + height / 2
        points2 = []
        for pp in points:
            x1, y1 = get_rotate_point(x=pp[0], y=pp[1], angle=angle, move_x=cx, move_y=cy)
            points2.append((x1, y1))

        # create Path

        vertices = [points2[0]]
        codes = [Path.MOVETO]
        for p in points2[1:]:
            vertices.append((p[0], p[1]))
            codes.append(Path.LINETO)
        vertices.append(points2[0])
        codes.append(Path.CLOSEPOLY)
        path = Path(vertices=vertices, codes=codes)

        # create PathPatch

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

        if text is not None:
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=textstyle,
                )
            )
