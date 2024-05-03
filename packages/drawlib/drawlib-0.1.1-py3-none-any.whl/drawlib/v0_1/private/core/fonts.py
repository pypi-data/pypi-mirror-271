# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Font define module

Support font defines here.
Class ``Font`` and ``FontSourceCode`` are provided to uses.

"""

from enum import Enum
import os
import drawlib.assets.v0_1.fonts
import dataclasses
from urllib.parse import urljoin
from typing import Optional, List, Tuple
from drawlib.v0_1.private.util import get_script_relative_path


def get_fontfile_tuple(path: str, md5_hash: str) -> Tuple[str, str, str]:
    paths = [p for p in path.split("/") if p]

    # font path
    dir_path = os.path.dirname(drawlib.assets.v0_1.fonts.__file__)
    font_path = os.path.join(dir_path, *paths)

    # url
    url = urljoin(
        "https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/v0_1/fonts/",
        "/".join(paths),
    )

    return (font_path, url, md5_hash)


class FontBase(Enum): ...


class Font(FontBase):
    """Drawlib Fonts.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    # sansserif
    SANSSERIF_LIGHT = get_fontfile_tuple("noto_sansserif_cjk/light.otf", "88ce9ab7e76fed605c822b52605ac2fd")
    SANSSERIF_REGULAR = get_fontfile_tuple("noto_sansserif_cjk/regular.otf", "6d57a40c6695bd46457315e2a9dc757a")
    SANSSERIF_BOLD = get_fontfile_tuple("noto_sansserif_cjk/bold.otf", "64d01f4e75814352cc9dea68074f4067")

    # serif
    SERIF_LIGHT = get_fontfile_tuple("noto_serif_cjk/light.otf", "0def63d37c63f0945d1046dae5ab4d83")
    SERIF_REGULAR = get_fontfile_tuple("noto_serif_cjk/regular.otf", "069123ca4dcbdee5cef81ef2f1d2ba8d")
    SERIF_BOLD = get_fontfile_tuple("noto_serif_cjk/bold.otf", "ea7175c0325777d126622340f9c94a66")

    # roboto
    ROBOTO_LIGHT = get_fontfile_tuple("roboto/light.ttf", "881e150ab929e26d1f812c4342c15a7c")
    ROBOTO_REGULAR = get_fontfile_tuple("roboto/regular.ttf", "8a36205bd9b83e03af0591a004bc97f4")
    ROBOTO_BOLD = get_fontfile_tuple("roboto/bold.ttf", "b8e42971dec8d49207a8c8e2b919a6ac")


class FontRoboto(FontBase):
    """Drawlib Fonts.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    # roboto
    ROBOTO_LIGHT = get_fontfile_tuple("roboto/light.ttf", "881e150ab929e26d1f812c4342c15a7c")
    ROBOTO_REGULAR = get_fontfile_tuple("roboto/regular.ttf", "8a36205bd9b83e03af0591a004bc97f4")
    ROBOTO_BOLD = get_fontfile_tuple("roboto/bold.ttf", "b8e42971dec8d49207a8c8e2b919a6ac")

    # robotoserif
    ROBOTO_SERIF_LIGHT = get_fontfile_tuple("roboto_serif/light.ttf", "4781a153250a8caf652b4f5b129c30ed")
    ROBOTO_SERIF_REGULAR = get_fontfile_tuple("roboto_serif/regular.ttf", "2fde5a4a0cef2c19b4b6a30763322847")
    ROBOTO_SERIF_BOLD = get_fontfile_tuple("roboto_serif/bold.ttf", "8ec6ab43edac2144cfd2494d522de733")

    # robotomono
    ROBOTO_MONO_LIGHT = get_fontfile_tuple("roboto_mono/light.ttf", "c9166464b1db95fc3cdf9b50fc7f98e2")
    ROBOTO_MONO_REGULAR = get_fontfile_tuple("roboto_mono/regular.ttf", "5b04fdfec4c8c36e8ca574e40b7148bb")
    ROBOTO_MONO_BOLD = get_fontfile_tuple("roboto_mono/bold.ttf", "90190d91283189e340b2a44fe560f2cd")

    # condensed
    ROBOTO_CONDENSED_LIGHT = get_fontfile_tuple("roboto_condensed/light.ttf", "68680c984f72eef7b2e2cf269382f2a6")
    ROBOTO_CONDENSED_REGULAR = get_fontfile_tuple("roboto_condensed/regular.ttf", "f1123f4b3d926ac4f72cc8091a4b5d19")
    ROBOTO_CONDENSED_BOLD = get_fontfile_tuple("roboto_condensed/bold.ttf", "0233b881b26ce6cc3884c6944940d11b")

    # slab
    ROBOTO_SLAB_LIGHT = get_fontfile_tuple("roboto_slab/light.ttf", "4c63608980b784c679bbadeb18d9acf4")
    ROBOTO_SLAB_REGULAR = get_fontfile_tuple("roboto_slab/regular.ttf", "2100b4a02ebb94c0aa18cabd642ee507")
    ROBOTO_SLAB_BOLD = get_fontfile_tuple("roboto_slab/bold.ttf", "2c44adc1ebd36820fd75012412e6f550")


class FontSanSerif(FontBase):
    """Drawlib Fonts.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    # nontserrat
    MONTSERRAT_LIGHT = get_fontfile_tuple("monstserrat/light.ttf", "94fbe93542f684134cad1d775947ca92")
    MONTSERRAT_REGULAR = get_fontfile_tuple("monstserrat/regular.ttf", "5e077c15f6e1d334dd4e9be62b28ac75")
    MONTSERRAT_BOLD = get_fontfile_tuple("monstserrat/bold.ttf", "ed86af2ed5bbaf879e9f2ec2e2eac929")

    # lato
    LATO_LIGHT = get_fontfile_tuple("lato/light.ttf", "2bcc211c05fc425a57b2767a4cdcf174")
    LATO_REGULAR = get_fontfile_tuple("lato/regular.ttf", "122dd68d69fe9587e062d20d9ff5de2a")
    LATO_BOLD = get_fontfile_tuple("lato/bold.ttf", "24b516c266d7341c954cb2918f1c8f38")

    # raleways
    RALEWAYS_LIGHT = get_fontfile_tuple("raleways/light.ttf", "a36750fa9f5530b0c2760267df04ae37")
    RALEWAYS_REGULAR = get_fontfile_tuple("raleways/regular.ttf", "d95649da7dfb965a289ac29105ce8771")
    RALEWAYS_BOLD = get_fontfile_tuple("raleways/bold.ttf", "21c82294041b1504a5cbe4f566c8acd6")

    # oswald
    OSWALD_LIGHT = get_fontfile_tuple("oswald/light.ttf", "fb3af9a7ffb259726bb3cb30b74ab7dc")
    OSWALD_REGULAR = get_fontfile_tuple("oswald/regular.ttf", "b299a657c45aa257f1458b327f491bfb")
    OSWALD_BOLD = get_fontfile_tuple("oswald/bold.ttf", "c95751378db3c5c8bfd993b164e13422")

    # poppins
    POPPINS_LIGHT = get_fontfile_tuple("poppins/light.ttf", "fcc40ae9a542d001971e53eaed948410")
    POPPINS_REGULAR = get_fontfile_tuple("poppins/regular.ttf", "093ee89be9ede30383f39a899c485a82")
    POPPINS_BOLD = get_fontfile_tuple("poppins/bold.ttf", "08c20a487911694291bd8c5de41315ad")


class FontSerif(FontBase):
    """Drawlib Fonts.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    # courier
    COURIER_REGULAR = get_fontfile_tuple("courier/regular.ttf", "fba4686ed1d1b4ef05ab14db78805dbe")
    COURIER_BOLD = get_fontfile_tuple("courier/bold.ttf", "4acfa45d29d240044e0075a8e58f0862")

    # merriweather
    MERRIWEATHER_LIGHT = get_fontfile_tuple("merriweather/light.ttf", "eccb6c6a243a3d44219648b6cdbc58ce")
    MERRIWEATHER_REGULAR = get_fontfile_tuple("merriweather/regular.ttf", "e2f219e63a575a41e10f991e9c95819a")
    MERRIWEATHER_BOLD = get_fontfile_tuple("merriweather/bold.ttf", "79ea53fed59f391498dfc6f2fbea97c2")

    # playfairdisplay
    PLAYFAIRDISPLAY_REGULAR = get_fontfile_tuple("playfairdisplay/regular.ttf", "1a28efdbd2876d90e554a67faabad24b")
    PLAYFAIRDISPLAY_BOLD = get_fontfile_tuple("playfairdisplay/bold.ttf", "9b38798112efb7cf6eca1de031cec4ca")

    # platypi
    PLATYPI_LIGHT = get_fontfile_tuple("platypi/light.ttf", "113ff25ffa6c98594583200398ab5c71")
    PLATYPI_REGULAR = get_fontfile_tuple("platypi/regular.ttf", "a7f199dd97ff6567df8978b579213e3d")
    PLATYPI_BOLD = get_fontfile_tuple("platypi/bold.ttf", "344e0525c3f473c8959c66e1df44e2e1")


class FontJapanese(FontBase):
    """Drawlib Fonts.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    # sansserif
    SANSSERIF_LIGHT = get_fontfile_tuple("noto_sansserif_cjk/light.otf", "88ce9ab7e76fed605c822b52605ac2fd")
    SANSSERIF_REGULAR = get_fontfile_tuple("noto_sansserif_cjk/regular.otf", "6d57a40c6695bd46457315e2a9dc757a")
    SANSSERIF_BOLD = get_fontfile_tuple("noto_sansserif_cjk/bold.otf", "64d01f4e75814352cc9dea68074f4067")

    # serif
    SERIF_LIGHT = get_fontfile_tuple("noto_serif_cjk/light.otf", "0def63d37c63f0945d1046dae5ab4d83")
    SERIF_REGULAR = get_fontfile_tuple("noto_serif_cjk/regular.otf", "069123ca4dcbdee5cef81ef2f1d2ba8d")
    SERIF_BOLD = get_fontfile_tuple("noto_serif_cjk/bold.otf", "ea7175c0325777d126622340f9c94a66")

    # mplus1p
    MPLUS1P_LIGHT = get_fontfile_tuple("mplus_1p/light.ttf", "01fea1cae2979588652514d83e9c0423")
    MPLUS1P_REGULAR = get_fontfile_tuple("mplus_1p/regular.ttf", "bfab3ff358a7fa14c5703ad49063cb16")
    MPLUS1P_BOLD = get_fontfile_tuple("mplus_1p/bold.ttf", "aa140061f44d0dda19ab2573a0ad93d3")


class FontKorean(FontBase):
    """Drawlib Fonts.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    # sansserif
    SANSSERIF_LIGHT = get_fontfile_tuple("noto_sansserif_cjk/light.otf", "88ce9ab7e76fed605c822b52605ac2fd")
    SANSSERIF_REGULAR = get_fontfile_tuple("noto_sansserif_cjk/regular.otf", "6d57a40c6695bd46457315e2a9dc757a")
    SANSSERIF_BOLD = get_fontfile_tuple("noto_sansserif_cjk/bold.otf", "64d01f4e75814352cc9dea68074f4067")

    # serif
    SERIF_LIGHT = get_fontfile_tuple("noto_serif_cjk/light.otf", "0def63d37c63f0945d1046dae5ab4d83")
    SERIF_REGULAR = get_fontfile_tuple("noto_serif_cjk/regular.otf", "069123ca4dcbdee5cef81ef2f1d2ba8d")
    SERIF_BOLD = get_fontfile_tuple("noto_serif_cjk/bold.otf", "ea7175c0325777d126622340f9c94a66")


class FontChinese(FontBase):
    """Drawlib Fonts.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    # sansserif
    SANSSERIF_LIGHT = get_fontfile_tuple("noto_sansserif_cjk/light.otf", "88ce9ab7e76fed605c822b52605ac2fd")
    SANSSERIF_REGULAR = get_fontfile_tuple("noto_sansserif_cjk/regular.otf", "6d57a40c6695bd46457315e2a9dc757a")
    SANSSERIF_BOLD = get_fontfile_tuple("noto_sansserif_cjk/bold.otf", "64d01f4e75814352cc9dea68074f4067")

    # serif
    SERIF_LIGHT = get_fontfile_tuple("noto_serif_cjk/light.otf", "0def63d37c63f0945d1046dae5ab4d83")
    SERIF_REGULAR = get_fontfile_tuple("noto_serif_cjk/regular.otf", "069123ca4dcbdee5cef81ef2f1d2ba8d")
    SERIF_BOLD = get_fontfile_tuple("noto_serif_cjk/bold.otf", "ea7175c0325777d126622340f9c94a66")


class FontThai(FontBase):
    """Drawlib Fonts.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    # sansserif
    SANSSERIF_LIGHT = get_fontfile_tuple("noto_thai_sans/light.ttf", "fa192df61c8ef9a6a204c6323fdae9dc")
    SANSSERIF_REGULAR = get_fontfile_tuple("noto_thai_sans/regular.ttf", "a84996ee5e940db8c7c2e1375728ca68")
    SANSSERIF_BOLD = get_fontfile_tuple("noto_thai_sans/bold.ttf", "1296256d14a6c704f87967dc06583a64")

    # serif
    SERIF_LIGHT = get_fontfile_tuple("noto_thai_serif/light.ttf", "70c158b4144d83cba0f7266952ddad2f")
    SERIF_REGULAR = get_fontfile_tuple("noto_thai_serif/regular.ttf", "fe28175fbf4e79f1562d30f60933cab7")
    SERIF_BOLD = get_fontfile_tuple("noto_thai_serif/bold.ttf", "dc10158f174b8141c810880b98ba5a5a")


class FontArabic(FontBase):
    """Drawlib Fonts.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    # sans
    SANSSERIF_LIGHT = get_fontfile_tuple("noto_arabic_sans/light.ttf", "ffcfcc231a05032bca6e0819aa60eacb")
    SANSSERIF_REGULAR = get_fontfile_tuple("noto_arabic_sans/regular.ttf", "75527903c6a793772b02807c5343f4c8")
    SANSSERIF_BOLD = get_fontfile_tuple("noto_arabic_sans/bold.ttf", "cda675687ed1576b7bda072838c0ed5f")

    # naskh
    NASKH_REGULAR = get_fontfile_tuple("noto_arabic_naskh/regular.ttf", "08f2d6bfe92d3e78721a0e1746397344")
    NASKH_BOLD = get_fontfile_tuple("noto_arabic_naskh/bold.ttf", "3e8ac1d70691caf5ddfd36fee8acce3d")

    # kufi
    KUFI_LIGHT = get_fontfile_tuple("noto_arabic_kufi/light.ttf", "23517c64b528b3c744bfb3be94e58836")
    KUFI_REGULAR = get_fontfile_tuple("noto_arabic_kufi/regular.ttf", "600b529eb4849a54dde020e3ea389de2")
    KUFI_BOLD = get_fontfile_tuple("noto_arabic_kufi/bold.ttf", "34886bd59d48cf9113e1e9386bee615e")


class FontMonoSpace(FontBase):
    """Drawlib Fonts.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    # robotomono
    ROBOTO_MONO_LIGHT = get_fontfile_tuple("roboto_mono/light.ttf", "c9166464b1db95fc3cdf9b50fc7f98e2")
    ROBOTO_MONO_REGULAR = get_fontfile_tuple("roboto_mono/regular.ttf", "5b04fdfec4c8c36e8ca574e40b7148bb")
    ROBOTO_MONO_BOLD = get_fontfile_tuple("roboto_mono/bold.ttf", "90190d91283189e340b2a44fe560f2cd")

    # courier
    COURIER_REGULAR = get_fontfile_tuple("courier/regular.ttf", "fba4686ed1d1b4ef05ab14db78805dbe")
    COURIER_BOLD = get_fontfile_tuple("courier/bold.ttf", "4acfa45d29d240044e0075a8e58f0862")

    # source code pro
    SOURCECODEPRO_LIGHT = get_fontfile_tuple("source_han_code_jp/light.otf", "ef1eb2fa9ff7c02e8a3336a70826ad47")
    SOURCECODEPRO_REGULAR = get_fontfile_tuple("source_han_code_jp/regular.otf", "abcdbd5449ad6a30d540221a12f4a0b5")
    SOURCECODEPRO_BOLD = get_fontfile_tuple("source_han_code_jp/bold.otf", "dff5826247909bb8e04b8bf3be893386")


class FontSourceCode(FontBase):
    """Drawlib Fonts which good for source code.

    Drawlib avoid using system font since it depends on host OS.
    Using only internal font files and user provided font file.

    """

    ROBOTO_MONO = get_fontfile_tuple("roboto_mono/regular.ttf", "5b04fdfec4c8c36e8ca574e40b7148bb")
    COURIER = get_fontfile_tuple("courier/regular.ttf", "fba4686ed1d1b4ef05ab14db78805dbe")
    SOURCECODEPRO = get_fontfile_tuple("source_han_code_jp/regular.otf", "abcdbd5449ad6a30d540221a12f4a0b5")


@dataclasses.dataclass
class FontFile:
    file: str

    @property  # type: ignore[no-redef]
    def file(self) -> Optional[str]:
        """getter of font_file"""

        return self._file

    @file.setter
    def file(self, value: str) -> None:
        """setter of font_file"""

        if isinstance(value, property):
            raise ValueError("font file not specified at class FontFile.")

        path = get_script_relative_path(value)
        if not os.path.exists(path):
            raise FileNotFoundError(f'font file "{path}" does not exist.')
        self._file = path
