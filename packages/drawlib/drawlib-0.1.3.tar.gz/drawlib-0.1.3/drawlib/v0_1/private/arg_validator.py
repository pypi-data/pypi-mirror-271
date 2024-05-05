from typing import Tuple, Union, List
from PIL.Image import Image

from drawlib.v0_1.private.core.dimage import Dimage
from drawlib.v0_1.private.core.model_validator import ColorValidator, CoordinateValidator
from drawlib.v0_1.private.core.model import (
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
    ImageStyle,
    IconStyle,
)
from drawlib.v0_1.private.core.fonts import FontSourceCode


class ArgValidator:

    # basic type

    @staticmethod
    def validate_bool(name: str, value: bool):
        if not isinstance(value, bool):
            raise ValueError(f'Arg "{name}" requires int value. But type {type(value)} "{value}" is given.')

    @staticmethod
    def validate_int(name: str, value: int):
        if not isinstance(value, int):
            raise ValueError(f'Arg "{name}" requires int value. But "{value}" is given.')

    @staticmethod
    def validate_float(name: str, value: Union[int, float]):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError(f'Arg "{name}" requires int/float value. But "{value}" is given.')

    @staticmethod
    def validate_str(name: str, value: int):
        if not isinstance(value, str):
            raise ValueError(f'Arg "{name}" requires str value. But "{value}" is given.')

    # drawlib coordinate system

    @staticmethod
    def validate_xy(name: str, value: Tuple[float, float]):
        try:
            CoordinateValidator.validate_xy(value)
        except ValueError:
            raise ValueError(f'Arg "{name}" requires coordinate (x, y). But "{value}" is given.')

    @staticmethod
    def validate_xys(name: str, value: List[Tuple[float, float]]):
        try:
            CoordinateValidator.validate_xys(value)
        except ValueError:
            raise ValueError(
                f'Arg "{name}" requires list of coordinates [(x, y), (x, y), ...] '
                f'at least 2 elements. But "{value}" is given.'
            )

    @staticmethod
    def validate_path_points(
        name: str,
        value: List[
            Union[
                Tuple[float, float],
                Tuple[float, float, float, float],
                Tuple[float, float, float, float, float, float],
            ]
        ],
    ):
        try:
            CoordinateValidator.validate_path_points(value)
        except ValueError:
            raise ValueError(f'Arg "{name}" requires list of path_points. Your input value has problem.')

    @staticmethod
    def validate_angle(name: str, value: int):
        try:
            CoordinateValidator.validate_angle(value)
        except ValueError:
            raise ValueError(f'Arg "{name}" requires angle 0.0 ~ 360.0. But {value} is given.')

    # drawlib color

    @staticmethod
    def validate_color(name: str, value: Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
        try:
            ColorValidator.validate_color(value)
        except ValueError:
            raise ValueError(
                f'Arg "{name}" requires color value(tuple[int, int, int] | '
                f"tuple[int, int, int, float]). But {value} is given."
            )

    @staticmethod
    def validate_alpha(name: str, value: Union[int, float]):
        try:
            ColorValidator.validate_alpha(value)
        except ValueError:
            raise ValueError(f'Arg "{name}" requires alpha value 0.0 ~ 1.0. But {value} is given.')

    # drawlib style

    @staticmethod
    def validate_iconstyle(name: str, value: IconStyle):
        if not isinstance(value, IconStyle):
            raise ValueError(f'Arg "{name}" requires IconStyle. But "{value}" is given.')

    @staticmethod
    def validate_imagestyle(name: str, value: ImageStyle):
        if not isinstance(value, ImageStyle):
            raise ValueError(f'Arg "{name}" requires ImageStyle. But "{value}" is given.')

    @staticmethod
    def validate_linestyle(name: str, value: LineStyle):
        if not isinstance(value, LineStyle):
            raise ValueError(f'Arg "{name}" requires LineStyle. But "{value}" is given.')

    @staticmethod
    def validate_linearrowstyle(name: str, value: LineArrowStyle):
        if not isinstance(value, LineArrowStyle):
            raise ValueError(f'Arg "{name}" requires LineArrowStyle. But "{value}" is given.')

    @staticmethod
    def validate_linestyle_or_linearrowstyle(name: str, value: Union[LineStyle, LineArrowStyle]):
        if isinstance(value, LineStyle):
            return
        if isinstance(value, LineArrowStyle):
            return
        raise ValueError(f'Arg "{name}" requires LineStyle or LineArrowStyle. But "{value}" is given.')

    @staticmethod
    def validate_shapestyle(name: str, value: ShapeStyle):
        if not isinstance(value, ShapeStyle):
            raise ValueError(f'Arg "{name}" requires ShapeStyle. But "{value}" is given.')

    @staticmethod
    def validate_shapetextstyle(name: str, value: ShapeTextStyle):
        if not isinstance(value, ShapeTextStyle):
            raise ValueError(f'Arg "{name}" requires ShapeTextStyle. But "{value}" is given.')

    @staticmethod
    def validate_textstyle(name: str, value: TextStyle):
        if not isinstance(value, TextStyle):
            raise ValueError(f'Arg "{name}" requires TextStyle. But "{value}" is given.')

    # others
    @staticmethod
    def validate_image_objects(name: str, value: Union[str, Image, Dimage]):
        if isinstance(value, str):
            return
        if isinstance(value, Image):
            return
        if isinstance(value, Dimage):
            return

        raise ValueError(f'Arg "{name}" requires str or PIL.Image.Image or ShapeTextStyle. But {value} is given.')

    @staticmethod
    def validate_fontsourcecode(name, str, value: FontSourceCode):
        if not isinstance(value, FontSourceCode):
            raise ValueError(f'Arg "{name}" requirest FontSourcecode. But {value} is given.')
