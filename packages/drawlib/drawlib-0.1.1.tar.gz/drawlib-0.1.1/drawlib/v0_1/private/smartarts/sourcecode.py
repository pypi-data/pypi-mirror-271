# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from typing import Final, Tuple, Literal
import io
from PIL import Image
from pygments import highlight
from pygments.lexers import (
    get_lexer_by_name,
    guess_lexer,
)
from pygments.lexer import Lexer
from pygments.lexers.special import TextLexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name

from drawlib.v0_1.private.util import error_handler
from drawlib.v0_1.private.core.util import ColorUtil
from drawlib.v0_1.private.core.model import *
from drawlib.v0_1.private.core_canvas.canvas import *
from drawlib.v0_1.private.core.dimage import Dimage
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.download import download_if_not_exist

PYGMENTS_LINENUM_TEXT_COLOR: Final[Tuple[int, int, int]] = (136, 136, 102)
PYGMENTS_LINENUM_BACKGROUND_COLOR: Final[Tuple[int, int, int]] = (238, 238, 221)


class SourceCode:
    """Draw Source Code Image which is created on Pygments

    Configure style at constructor.
    Provide code and size/location at render() method.
    If you want to customize image by your self, call get_image().

    """

    @error_handler
    def __init__(
        self,
        language: Optional[
            Literal[
                "bash",
                "c",
                "c#",
                "c++",
                "coffeescript",
                "css",
                "dart",
                "docker",
                "go",
                "groovy",
                "haskell",
                "html",
                "ini",
                "java",
                "javascript",
                "json",
                "julia",
                "kotlin",
                "less",
                "markdown",
                "none",
                "objective-c",
                "perl",
                "php",
                "plain",
                "powershell",
                "promql",
                "protobuf",
                "python",
                "restructuredtext",
                "ruby",
                "rust",
                "sql",
                "swift",
                "tex",
                "text",
                "toml",
                "typescript",
                "verilog",
                "xml",
                "yaml",
            ]
        ] = None,
        style: Literal[
            "bw",
            "sas",
            "staroffice",
            "xcode",
            "default",
            "monokai",
            "lightbulb",
            "github-dark",
            "rrt",
            # not recommended. but gray scale might be important
            "algol",
            "algol_nu",
            "friendly_grayscale",
        ] = "default",
        font: Union[
            FontSourceCode,
            FontFile,
            None,
        ] = None,
        show_linenum: bool = False,
        linenum_textcolor: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
        ] = PYGMENTS_LINENUM_TEXT_COLOR,
        linenum_bgcolor: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
        ] = PYGMENTS_LINENUM_BACKGROUND_COLOR,
    ):

        def get_lexer() -> Optional[Lexer]:
            if language is None:
                # guess lexer at method draw()
                return None
            elif language in ["none", "plain", "text"]:
                return TextLexer()
            else:
                return get_lexer_by_name(language)

        def get_formatter():
            pygments_style = get_style_by_name(style)

            if font is None:
                file_path, download_url, md5_hash = dtheme.sourcecodefont_get().value
                download_if_not_exist(
                    file_path=file_path,
                    download_url=download_url,
                    md5_hash=md5_hash,
                )
            elif isinstance(font, FontFile):
                file_path = font.file
            elif isinstance(font, FontSourceCode):
                file_path, download_url, md5_hash = font.value
                download_if_not_exist(
                    file_path=file_path,
                    download_url=download_url,
                    md5_hash=md5_hash,
                )
            else:
                raise ValueError(f'font type "{type(font)}" is not supported.')

            lnoptions = {"line_numbers": show_linenum}
            if show_linenum:
                lnoptions["line_number_fg"] = ColorUtil.get_hexrgb(linenum_textcolor)
                lnoptions["line_number_bg"] = ColorUtil.get_hexrgb(linenum_bgcolor)

            return ImageFormatter(
                style=pygments_style,
                font_name=file_path,
                **lnoptions,
            )

        self._lexer: Optional[Lexer] = get_lexer()
        self._formatter = get_formatter()

    @error_handler
    def get_image(self, code: str) -> Dimage:
        if self._lexer is None:
            lexer = guess_lexer(code)
        else:
            lexer = self._lexer

        # create image data
        image_buffer = io.BytesIO()
        highlight(code, lexer, self._formatter, image_buffer)
        image_buffer.seek(0)
        return Dimage(Image.open(image_buffer))

    @error_handler
    def draw(
        self,
        xy: Tuple[float, float],
        width: float,
        code: str,
        style: Optional[ImageStyle] = None,
    ) -> None:
        image_ = self.get_image(code=code)
        image(xy=xy, width=width, image=image_, style=style)

        """
        if not self._show_border:
            return

        im_width, im_height = image_.get_image_size()
        height = (im_height / im_width) * width
        if self._borderstyle is None:
            self._borderstyle = LineStyle()

        default = dtheme.shapestyle_get()
        if self._borderstyle.color is None:
            self._borderstyle.color = default.lcolor
        if self._borderstyle.width is None:
            self._borderstyle.width = default.lwidth
        if self._borderstyle.style is None:
            self._borderstyle.style = default.lstyle

        rect_style = ShapeStyle(
            lcolor=self._borderstyle.color,
            lwidth=self._borderstyle.width,
            lstyle=self._borderstyle.style,
            fcolor=Colors.Transparent,
        )
        rectangle(xy=xy, width=width, height=height, style=rect_style)
        """
