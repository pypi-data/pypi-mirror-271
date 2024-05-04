# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Handle drawlib command

Entry point ``__main__`` calls this module's function ``call()``.
After that class ``DrawlibArgParser`` parse options.
Then operate appropriate actions.

"""

import os
import sys
import argparse
from typing import Optional, List
import drawlib
import drawlib.v0_1
from drawlib.v0_1.private.logging import logger
from drawlib.v0_1.private.settings import dsettings
from drawlib.v0_1.private.tools import dload


def call() -> None:
    """drawlib command handling function.

    This method is called from each API's ``__main__`` module.
    If the API is latest, called from root package's ``__main__`` module too.

    Abstract procedure of this function.

    1. Crate DrawlibArgParser instance.
    2. Parse command line options
    3. If options requests version info, show it and quit.
    4. Apply options such as logging level
    5. get target files and directories which drawlib run.
    6. call ``tools.run()`` for each files, directories

    Returns:
        None

    """

    argparser = DrawlibArgParser()
    argparser.parse()
    argparser.show_version_then_exit0_if_requested()
    argparser.apply_options()
    paths = argparser.get_positional_args()

    if len(paths) == 0:
        logger.critical("no input files and directories")
        logger.critical('check options with "drawlib --help"')
        sys.exit(1)

    for path in paths:
        if not os.path.isfile(path) and not os.path.isdir(path):
            msg = f'ignore arg "{path}" since it is not a file/dir path'
            logger.warning(msg)
            continue

        abspath = os.path.abspath(path)
        realpath = os.path.realpath(abspath)
        logger.info(realpath)
        dload(realpath)


class DrawlibArgParser:
    """drawlib ArgParser Class"""

    def __init__(self) -> None:
        """Initializa DrawlibArgParser

        In this method, create ``ArgumentParser`` instance and
        define command line options.

        Returns:
            None

        """

        parser = argparse.ArgumentParser(
            description="Ilustration as code by python",
        )
        parser.add_argument(
            "file_or_directory",
            nargs="...",
            help="Target python file or directory which contains python codes",
        )
        parser.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="Show version",
        )
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Enable quiet logging. show only error messages",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose logging.",
        )
        parser.add_argument(
            "--developer",
            action="store_true",
            help=("Enable verbose logging. " "Disable error handling for library users."),
        )
        self._parser = parser
        self._positional_args: Optional[List[str]] = None
        self._name_args: Optional[argparse.Namespace] = None

    def parse(self) -> None:
        """Parse command line options.

        Parse command line options.
        This method must be called before calling get methods.

        Returns:
            None

        """

        self._name_args, _ = self._parser.parse_known_args()
        args = self._parser.parse_args()
        self._positional_args = args.file_or_directory

    def get_positional_args(self) -> List[str]:
        """Get positional args. which are files and directories.

        drawlib command requires files and directories as positional args.
        They are the target of ``tool.run()`` function.
        It means specified file or files inside directories
        are called from python.
        If those python files are drawlib's one, generate images.

        This method must be called after ``parse()`` method is called.

        Returns:
            List[str]: Positional args (files and directories)

        """

        if self._positional_args is None:
            logger.critical("DrawlibArgParser must be parsed before getting optional args")
            sys.exit(1)

        return self._positional_args

    def show_version_then_exit0_if_requested(self) -> None:
        """show version if option ``-v/`` or ``--version`` exists. And then quit.

        Check whether option has ``-v`` or ``--version``.
        If yes, show version. And then, quit with ``sys.exit(0)``.

        Returns:
            None

        """

        if self._name_args is None:
            logger.critical("DrawlibArgParser must be parsed before apply options")
            sys.exit(1)

        if self._name_args.version:
            logger.critical(f"software={drawlib.VERSION}")
            logger.critical(f"api={drawlib.v0_1.VERSION}")
            sys.exit(0)

    def apply_options(self) -> None:
        """Check named args and apply appropriate configs.

        Check these named argses. And do appropriate actions.

        * --quiet: make logging mode quiet
        * --debug: make logging mode verbose
        * --devdebug: make logging mode developer

        Returns:
            None

        """

        if self._name_args is None:
            logger.critical("DrawlibArgParser must be parsed before apply options")
            sys.exit(1)

        if self._name_args.quiet and (self._name_args.verbose or self._name_args.developer):
            raise ValueError("option --quiet can't use with option --debug and --devdebug")

        if self._name_args.quiet:
            dsettings.set_logging_mode("quiet")

        if self._name_args.verbose:
            dsettings.set_logging_mode("verbose")

        if self._name_args.developer:
            dsettings.set_logging_mode("developer")
