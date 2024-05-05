# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base canvas features.

This modules define CanvasBase which is base class of Canvas features.
Each canvas features are aggregated on Canvas.

"""

# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods

# !!! Temporary Lint Escape !!!
# pylint: disable=unnecessary-ellipsis
# pylint: disable=unused-argument

import os
import math
from typing import Final, Union, Optional, List, Tuple, Literal
import matplotlib.font_manager
import matplotlib.artist
import matplotlib.lines
import matplotlib.text
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib import pyplot
import PIL.Image

from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.util import (
    error_handler,
    get_script_path,
    get_script_relative_path,
    get_center_and_size,
    minus_2points,
)
from drawlib.v0_1.private.core.model import (
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
)
from drawlib.v0_1.private.core.colors import Colors
from drawlib.v0_1.private.core.dimage import Dimage
from drawlib.v0_1.private.core.util import ColorUtil, ShapeUtil
from drawlib.v0_1.private.arg_validator import ArgValidator


class CanvasBase:
    """Base class of Canvas and its features.

    This class is designed for diamond inheritance.

    """

    DEFAULT_WIDTH: Final[int] = 100
    DEFAULT_HEIGHT: Final[int] = 100
    DEFAULT_DPI: Final[int] = 100
    DEFAULT_GRID: Final[bool] = False
    DEFAULT_GRID_ONLY: Final[bool] = False
    DEFAULT_GRID_STYLE: Final[LineStyle] = LineStyle(width=1, color=Colors.Gray, style="dashed")
    DEFAULT_GRID_CENTERSTYLE: Final[LineStyle] = LineStyle(width=2, color=Colors.Gray, style="dashed")
    SYSTEM_FONTS = ["serif", "sanserif"]

    @error_handler
    def __init__(self) -> None:
        """Initialize Canvas instance with default params.

        Not only first initialization, it is called from ``clear()``.
        Variables are updated on ``config()``.

        Returns:
            None

        """

        self._width = self.DEFAULT_WIDTH
        self._height = self.DEFAULT_HEIGHT
        self._dpi = self.DEFAULT_DPI
        self._background_color: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
            None,
        ] = None  # apply theme default later if no update
        self._background_alpha: Optional[float] = None  # apply theme default later if no update
        self._grid = self.DEFAULT_GRID
        self._grid_only = self.DEFAULT_GRID_ONLY
        self._grid_style = self.DEFAULT_GRID_STYLE
        self._grid_centerstyle = self.DEFAULT_GRID_CENTERSTYLE
        self._artists: List[matplotlib.artist.Artist] = []

        # it is decleared only for typing system
        self._fig = pyplot.figure()
        self._ax = self._fig.add_subplot(1, 1, 1)

        # initialize fig and ax
        self.config()

    ##############
    ### basics ###
    ##############

    @error_handler
    def clear(self) -> None:
        """Initialize drawlib Canvas config

        Initialize drawlib Canvas completely.
        It will wipe params which are set by config().
        And also, all drawing states.

        Returns:
            None

        Note:
            ``dtheme`` is not initialized.

        """

        pyplot.close()
        # pylint: disable=unnecessary-dunder-call
        CanvasBase.__init__(self)  # type: ignore[misc]
        # pylint: enable=unnecessary-dunder-call

    @error_handler
    def config(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        dpi: Optional[int] = None,
        theme: Optional[
            Literal[
                "default",
                "gray",
            ]
        ] = None,
        background_color: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
            None,
        ] = None,
        background_alpha: Optional[float] = None,
        grid: Optional[bool] = None,
        grid_only: Optional[bool] = None,
        grid_style: Optional[LineStyle] = None,
        grid_centerstyle: Optional[LineStyle] = None,
    ) -> None:
        """Configure drawlib Canvas

        Configure drawlib canvas parameters.
        Parameters will be wiped when ``clear()`` method is called except ``theme``.
        You can call this function many times.

        Args:
            width(optional): Width of canvas. default is 100
            height(optional): Height of canvas. default is 100
            dpi(optional): Output image resolution. default is 100
            theme(optional): Choose draw theme. ``clear()`` doesn't initialize this.
            background_color(optional): Background color. default is "white"
            background_alpha(optional): Background alpha. between 0~1. default is 1.0
            grid(optional): show grid for checking coordinate on True
            grid_style(optional): Style of grid line. default is dashed gray. Setting this will set `grid=True` automatically.
            grid_centerstyle(optional): Style of grid line. default is thick dashed gray. Setting this will set `grid=True` automatically.

        Returns:
            None

        Note:
            Calling config after drawing raise RuntimeError.
            It is because few drawing action uses Canvas size and dpi etc.
            Changing them after drawing will mess the drawing status.
            You can call config() again after calling clear().

        """

        # This method config() can be called repeatedly.
        # Please don't set default value in args
        # but set it at __init__() at first and clear().

        # validate args

        if width is not None:
            ArgValidator.validate_int("width", width)
        if height is not None:
            ArgValidator.validate_int("height", height)
        if dpi is not None:
            ArgValidator.validate_int("dpi", dpi)
        if theme is not None:
            # check it later in this method
            ...
        if background_color is not None:
            ArgValidator.validate_color("background_color", background_color)
        if background_alpha is not None:
            ArgValidator.validate_alpha("background_alpha", background_alpha)
        if grid is not None:
            ArgValidator.validate_bool("grid", grid)
        if grid_style is not None:
            ArgValidator.validate_linestyle("grid_style", grid_style)
        if grid_centerstyle is not None:
            ArgValidator.validate_linestyle("grid_centerstyle", grid_centerstyle)

        # validate status

        if len(self._artists) != 0:
            raise RuntimeError(
                "config() must be called before drawing. "
                "Please call clear() first if you want to "
                "initialize drawing configs and states."
            )

        def config_size_dpi():
            size_dpi_changed = False
            if width is not None:
                self._width = width
            if height is not None:
                self._height = height
            if dpi is not None:
                self._dpi = dpi

            # set fig size. width is always 10
            fig_width = 10
            fig_hight = self._height * 10 / self._width
            self._fig = pyplot.figure(
                figsize=(fig_width, fig_hight),
                dpi=self._dpi,
            )

            # set ax size
            self._ax = self._fig.add_subplot(1, 1, 1)
            self._ax.set_xlim(0, self._width)
            self._ax.set_ylim(0, self._height)
            self._ax.set_aspect("equal")
            self._ax.axis("off")
            self._ax.margins(0, 0)

        def config_theme():
            if theme is None:
                return

            if theme == "default":
                dtheme.theme_default()
            elif theme == "gray":
                dtheme.theme_gray()
            else:
                raise ValueError(f'Theme "{theme}" is not supported.')

        def config_background():
            if background_color is not None:
                self._background_color = background_color
            if background_alpha is not None:
                self._background_alpha = background_alpha

        def config_grid():
            if grid_style is not None:
                self._grid = True
                self._grid_style = grid_style
                if grid_centerstyle is None:
                    self._grid_centerstyle = grid_style

            if grid_centerstyle is not None:
                self._grid = True
                self._grid_centerstyle = grid_centerstyle

            if grid_only is not None:
                self._grid_only = grid_only
                if grid_only:
                    self._grid = True

            if grid is not None:
                self._grid = grid

            # grid is drawn at method _render()

        pyplot.close()
        config_size_dpi()
        config_theme()
        config_background()
        config_grid()

    @error_handler
    def save(
        self,
        file: Optional[str] = None,
        format: Optional[Literal["jpg", "png", "webp", "pdf"]] = None,
    ) -> None:
        """Save canvas illustration to file.

        Args:
            file(optional): saving image file path. Default is "<script-name>.png".
            format(optional): supported image format. default is "png".

        Returns:
            None

        Note:
            Without arg, save to "<scriptfilename>.png" on script dir.
            For example, calling "save()" at script "mydir/image1.py" will
            generate "mydir/image1.png"

        """

        # validate args

        if file is not None:
            ArgValidator.validate_str("file", file)
        if format is not None:
            if file is not None:
                raise ValueError('Can not specify format when arg "file" is provided.')
            supported = ["jpg", "png", "webp", "pdf"]
            if format not in supported:
                raise ValueError(f'Save format supports only {supported}. But "{format}" is provided.')

        # create save file path

        if file is None:
            script_path = get_script_path()
            parent_dir = os.path.dirname(script_path)
            name = os.path.basename(script_path)
            name_without_ext = os.path.splitext(name)[0]
            ext = "png" if format is None else format
            file_path = f"{os.path.join(parent_dir, name_without_ext)}.{ext}"
        else:
            file_path = get_script_relative_path(file)

        # set background

        has_color_alpha = False
        if self._background_color is not None:
            background_color = self._background_color
            if len(background_color) == 4:
                has_color_alpha
        else:
            background_color = dtheme.background_color_get()

        if self._background_alpha is not None:
            background_alpha = self._background_alpha
        elif has_color_alpha:
            # set user specified alpha in color as alpha-value
            background_alpha = background_color[3]
        else:
            background_alpha = dtheme.background_alpha_get()

        mplot_rgba = ColorUtil.get_mplot_rgba(background_color, background_alpha)
        self._fig.patch.set_facecolor(mplot_rgba)
        self._ax.patch.set_alpha(0)

        # draw artist (image, patches, line, text)

        zorder = 0
        for artist in self._artists:
            artist.zorder = zorder
            zorder += 1
            self._ax.add_artist(artist)
        self._artists = []

        # remove margin

        self._fig.tight_layout()
        self._fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        # save to file

        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)

        if not self._grid_only:
            pyplot.savefig(file_path)
            if not self._grid:
                return

        # draw grid
        grid_width = self._width / 10
        grid_height = self._height / 10
        for i in range(1, 10):
            style = self._grid_centerstyle if i == 5 else self._grid_style
            self.line(
                xy1=(i * grid_width, 0),
                xy2=(i * grid_width, self._height),
                style=style,
            )
        for i in range(1, 10):
            style = self._grid_centerstyle if i == 5 else self._grid_style
            self.line(
                xy1=(0, i * grid_height),
                xy2=(self._width, i * grid_height),
                style=style,
            )

        for artist in self._artists:
            artist.zorder = zorder
            zorder += 1
            self._ax.add_artist(artist)
        self._artists = []

        # save to file
        if self._grid_only:
            pyplot.savefig(file_path)
        else:
            name, extension = os.path.splitext(file_path)
            pyplot.savefig(f"{name}_grid{extension}")

    #######################
    ### low level shape ###
    #######################

    def shape(
        self,
        xy: Tuple[float, float],
        path_points: List[
            Union[
                Tuple[float, float],
                Tuple[float, float, float, float],
                Tuple[float, float, float, float, float, float],
            ]
        ],
        angle: Optional[float] = None,
        style: Optional[ShapeStyle] = None,
        text: Optional[str] = None,
        textstyle: Optional[ShapeTextStyle] = None,
        is_default_center: bool = False,
    ) -> None:
        """Draw basic shape.

        This function is useful for drawing user original shapes.
        Please check document and example for details.

        Args:
            xy: start point
            path_points: xy and bezier control points.
            angle(optional): shape angle.
            style(optional): shape style.
            text(optional): text of shape.
            textstyle(optional): text style.
            is_default_center: make (x, y) center of shape.

        Returns:
            None

        """

        # validate args

        ArgValidator.validate_xy("xy", xy)
        ArgValidator.validate_path_points("path_points", path_points)
        if angle is not None:
            ArgValidator.validate_angle("angle", angle)
        if style is not None:
            ArgValidator.validate_shapestyle("style", style)
        if text is not None:
            ArgValidator.validate_str("text", text)
        if textstyle is not None:
            ArgValidator.validate_shapetextstyle("textstyle", textstyle)
        if is_default_center is not None:
            ArgValidator.validate_bool("is_default_center", is_default_center)

        # helper

        def get_rotate_point(x: float, y: float, angle: Optional[float], move_x: float, move_y: float):
            if angle is None:
                angle = 0.0
            angle_rad = math.radians(angle)
            x_rotated = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            y_rotated = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            return x_rotated + move_x, y_rotated + move_y

        # apply default style

        style = ShapeUtil.get_merged_shapestyle(style, dtheme.shapestyle_get())
        textstyle = ShapeUtil.get_merged_shapetextstyle(textstyle, dtheme.shapetextstyle_get())

        # shift to center (0, 0)

        points_without_cp = []
        for pp in path_points:
            points_without_cp.append(pp[-2:])
        center, (width, height) = get_center_and_size(points_without_cp)
        path_points2 = []
        for pp in path_points:
            x1, y1 = minus_2points(pp[:2], center)
            if len(pp) == 2:
                path_points2.append((x1, y1))
                continue
            x2, y2 = minus_2points(pp[2:4], center)
            if len(pp) == 4:
                path_points2.append((x1, y1, x2, y2))
                continue
            x3, y3 = minus_2points(pp[4:6], center)
            path_points2.append((x1, y1, x2, y2, x3, y3))

        # alignment

        if is_default_center:
            # move to center
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
            is_default_center=is_default_center,
        )

        # rotate and move

        cx = x + width / 2
        cy = y + height / 2
        path_points3 = []
        for pp in path_points2:
            x1, y1 = get_rotate_point(x=pp[0], y=pp[1], angle=angle, move_x=cx, move_y=cy)
            if len(pp) == 2:
                path_points3.append((x1, y1))
                continue
            x2, y2 = get_rotate_point(x=pp[2], y=pp[3], angle=angle, move_x=cx, move_y=cy)
            if len(pp) == 4:
                path_points3.append((x1, y1, x2, y2))
                continue
            x3, y3 = get_rotate_point(x=pp[4], y=pp[5], angle=angle, move_x=cx, move_y=cy)
            path_points3.append((x1, y1, x2, y2, x3, y3))

        # create Path

        vertices = [path_points3[0]]
        codes = [Path.MOVETO]
        for p in path_points3[1:]:
            length = len(p)
            if length not in [2, 4, 6]:
                raise ValueError()
            if length == 2:
                vertices.append((p[0], p[1]))
                codes.append(Path.LINETO)
            elif length == 4:
                vertices.extend([(p[0], p[1]), (p[2], p[3])])
                codes.extend([Path.CURVE3] * 2)
            else:
                vertices.extend([(p[0], p[1]), (p[2], p[3]), (p[4], p[5])])
                codes.extend([Path.CURVE4] * 3)
        vertices.append(path_points3[0])
        codes.append(Path.CLOSEPOLY)
        path = Path(vertices=vertices, codes=codes)

        # create PathPatch

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

        # create Text

        if text is not None:
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=textstyle,
                )
            )

    #############
    ### dutil ###
    #############

    @error_handler
    def get_image_zoom_original(
        self,
    ) -> float:
        """Get matplot image zoom which keeps original pixel size.

        Returns:
            float: zoom

        """

        #
        # calcuration
        # 0.72 * 100 / dpi
        #

        zoom = 72 / self._dpi
        return zoom

    @error_handler
    def get_image_zoom_from_width(
        self,
        image: Union[str, PIL.Image.Image, Dimage],
        width: float,
    ) -> float:
        """Get matplot image zoom which is fit to specified width.

        Returns:
            float: zoom

        """

        #
        # calcuration
        # 0.72 * 10 * 100 * target_width / canvas_width / image_width
        #

        if not isinstance(image, Dimage):
            image = Dimage(image)

        image_width, _ = image.get_image_size()
        zoom = 720 * width / self._width / image_width
        return zoom

    @error_handler
    def get_charwidth_from_fontsize(
        self,
        size: float,
    ) -> float:
        """Get character width from font size..

        Args:
            size: font size

        Returns:
            float: width

        """

        MAGIC_NUMBER = 460  # todo: requires better calcuration
        width = size * 0.72 * self._width / MAGIC_NUMBER
        return width

    @error_handler
    def get_fontsize_from_charwidth(
        self,
        width: float,
    ) -> float:
        """Get font size which fit to provided width.

        Args:
            width: character width

        Returns:
            int: size

        """

        MAGIC_NUMBER = 540  # todo: requires better calcuration
        size = MAGIC_NUMBER * width / 0.72 / self._width
        return int(size)
