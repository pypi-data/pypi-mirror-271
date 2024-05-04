from typing import Tuple, Union, List
from drawlib.v0_1.private.core.fonts import FontBase, FontFile


class ColorValidator:
    ERROR_MESSAGE_ALPHA = 'Alpha must be float/int between 0.0~1.0. But "{value}" is given.'
    ERROR_MESSAGE_COLOR_FORMAT = 'Color format must be (R,G,B) or (R,G,B,A). But "{value}" is given.'
    ERROR_MESSAGE_RGB_VALUE = 'Each RGB color must be int between 0~255. But "{value}" is given.'

    @staticmethod
    def validate_alpha(value: float):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError(ColorValidator.ERROR_MESSAGE_ALPHA.format(value=value))
        if not 0.0 <= value <= 1.0:
            raise ValueError(ColorValidator.ERROR_MESSAGE_ALPHA.format(value=value))

    @staticmethod
    def validate_color(value: Union[Tuple[int, int, int], Tuple[int, int, int, float]]):
        if not isinstance(value, tuple):
            raise ValueError(ColorValidator.ERROR_MESSAGE_COLOR_FORMAT.format(value=value))
        if len(value) not in [3, 4]:
            raise ValueError(ColorValidator.ERROR_MESSAGE_COLOR_FORMAT.format(value=value))

        r = value[0]
        g = value[1]
        b = value[2]
        a = 1.0 if len(value) == 3 else value[3]

        for c in [r, g, b]:
            if not isinstance(c, int):
                raise ValueError(ColorValidator.ERROR_MESSAGE_RGB_VALUE.format(value=c))
            if not 0 <= c <= 255:
                raise ValueError(ColorValidator.ERROR_MESSAGE_RGB_VALUE.format(value=c))

        if not (isinstance(a, float) or isinstance(a, int)):
            raise ValueError(ColorValidator.ERROR_MESSAGE_ALPHA.format(value=a))
        if not 0.0 <= a <= 1.0:
            raise ValueError(ColorValidator.ERROR_MESSAGE_ALPHA.format(value=a))


class AlignValidator:

    @staticmethod
    def validate_halign(value: str):
        supported = ["left", "center", "right"]
        if value not in supported:
            raise ValueError(f'Supported horizontal aligns are {supported}. But "{value}" is given.')

    @staticmethod
    def validate_valign(value: str):
        supported = ["bottom", "center", "top"]
        if value not in supported:
            raise ValueError(f'Supported vertical aligns are {supported}. But "{value}" is given.')


class LineValidator:
    ERROR_MESSAGE_WIDTH = 'Line width must be between 0.0 ~ 100.0. But "{value}" is given.'
    ERROR_MESSAGE_SCALE = 'Line arrow head scale must be between 0.0 ~ 100.0. But "{value}" is given.'

    @staticmethod
    def validate_width(value: float):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError(LineValidator.ERROR_MESSAGE_WIDTH.format(value=value))
        if not 0.0 <= value <= 100.0:
            raise ValueError(LineValidator.ERROR_MESSAGE_WIDTH.format(value=value))

    @staticmethod
    def validate_style(value: str):
        supported = ["solid", "dashed", "dotted", "dashdot"]
        if value not in supported:
            raise ValueError(f'Supported line styles are {supported}. But "{value}" is given.')

    @staticmethod
    def validate_arrowhead_style(value: str):
        supported = ["->", "<-", "<->", "-|>", "<|-", "<|-|>"]
        if value not in supported:
            raise ValueError(f'Supported arrow head styles are {supported}. But "{value}" is given.')

    @staticmethod
    def validate_arrowhead_scale(value: float):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError(LineValidator.ERROR_MESSAGE_SCALE.format(value=value))
        if not 0.0 <= value <= 100.0:
            raise ValueError(LineValidator.ERROR_MESSAGE_SCALE.format(value=value))


class TextValidator:
    ERROR_MESSAGE_SIZE = 'Text size must be between 0.0 ~ 1000.0. But "{value}" is given.'
    ERROR_MESSAGE_FLIP = 'Text flip must be False/True. But "{value}" is given.'

    @staticmethod
    def validate_size(value: float):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError(TextValidator.ERROR_MESSAGE_SIZE.format(value=value))
        if not 0.0 <= value <= 1000.0:
            raise ValueError(TextValidator.ERROR_MESSAGE_SIZE.format(value=value))

    @staticmethod
    def validate_font(value: Union[FontBase, FontFile]):
        if isinstance(value, FontBase):
            return
        if isinstance(value, FontFile):
            return

        raise ValueError(f'Font must be "instance of FontFile" or "member of Font classes". But "{value}" is given.')

    @staticmethod
    def validate_flip(value: bool):
        if not isinstance(value, bool):
            raise ValueError(TextValidator.ERROR_MESSAGE_FLIP.format(value=value))


class CoordinateValidator:
    ERROR_MESSAGE_XY = 'xy must be (int/float, int/float) format. But "{value}" is given.'
    ERROR_MESSAGE_XYS = "xys must be list of coordinate."
    ERROR_MESSAGE_PATH_POINTS = "path_points must be list of path_point. (x,y) or (x1,y1,x2,y2) or (x1,y1,x2,y2,x3,y3)."
    ERROR_MESSAGE_ANGLE = 'Angle must be between 0.0 ~ 360.0. But "{value}" is given.'

    @staticmethod
    def validate_xy(value: Tuple[float, float]):
        if not isinstance(value, tuple):
            raise ValueError(CoordinateValidator.ERROR_MESSAGE_XY.format(value=value))
        if len(value) != 2:
            raise ValueError(CoordinateValidator.ERROR_MESSAGE_XY.format(value=value))

        x, y = value
        for c in [x, y]:
            if not (isinstance(c, float) or isinstance(c, int)):
                raise ValueError(CoordinateValidator.ERROR_MESSAGE_XY.format(value=value))

    @staticmethod
    def validate_xys(value: List[Tuple[float, float]]):
        if not isinstance(value, list):
            raise ValueError()

        for e in value:
            if not isinstance(e, tuple):
                raise ValueError()
            if len(e) != 2:
                raise ValueError()

            x, y = e
            for c in [x, y]:
                if not (isinstance(c, float) or isinstance(c, int)):
                    raise ValueError()

    @staticmethod
    def validate_path_points(
        value: List[
            Union[
                Tuple[float, float],
                Tuple[float, float, float, float],
                Tuple[float, float, float, float, float, float],
            ]
        ],
    ):
        if not isinstance(value, list):
            raise ValueError()

        for e in value:
            if not isinstance(e, tuple):
                raise ValueError()
            if len(e) not in [2, 4, 6]:
                raise ValueError()

            for c in e:
                if not (isinstance(c, float) or isinstance(c, int)):
                    raise ValueError()

    @staticmethod
    def validate_angle(value: float):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError(CoordinateValidator.ERROR_MESSAGE_ANGLE.format(value=value))
        if not 0.0 <= value <= 360.0:
            raise ValueError(CoordinateValidator.ERROR_MESSAGE_ANGLE.format(value=value))
