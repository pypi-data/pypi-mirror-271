# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""This module defines tool functions

Note:
    This module's concept is very similar to util module.
    However, please don't merge them.
    
    This module is created for avoiding circular import between ``canvas`` and ``util``.
    Function ``run()`` depends on ``canvas`` and ``canvas_singleton``.
    And ``canvas`` and core modules depends on ``util``.
    If you move function ``run()`` to ``util``, it makes import trouble.

"""

# pylint: disable=logging-fstring-interpolation
# pylint: disable=global-statement

import os
from typing import Set, List, Final
import importlib.util
import traceback
import sys

from drawlib.v0_1.private.logging import logger
from drawlib.v0_1.private.util import (
    error_handler,
    get_script_relative_path,
)
from drawlib.v0_1.private.core_canvas.canvas import clear


class Loader:
    _INDENT_SIZE: Final[int] = 4

    def __init__(self) -> None:
        self._executed_files: Set[str] = set()
        self._load_stack: int = 0

    @error_handler
    def dload(self, file_or_directory: str, auto_clear: bool = True) -> None:
        """Run specified python file or python files in specified directory

        Call python file via OS path.
        When you specify python file, only run it.
        When you specify directory, run all python files recursively inside it.
        Each python files are called only 1 time.
        2nd time call is skipped.

        When file1.py calls ``run("file2.py")`` and file2.py calls
        ``run("file3.py")``, loading file3.py first.
        This recursive load situation can be checked on console.
        Please don't make circular loading situation.

        Note:
            We recommend creating ``.drawlib`` directory and put all python files which are loaded.
            Each drawing python file need to declare only ``run(<path_to_.drawlib>)``.

        Strongly recommend ``auto_clear=True`` when specifying directory.
        If user code doesn't call ``clear()``,
        canvas state is shared between python files.
        It means 2nd draw can contain 1st draw results.
        Default value of ``auto_clear`` is True.

        Args:
            file_or_directory: run target. relative to user script path.
            auto_clear(optional): call ``clear()`` method between running each python files.

        Returns:
            None

        """

        path = get_script_relative_path(file_or_directory)
        if not os.path.exists(path):
            raise ValueError(f'"{path}" does not exist')

        if os.path.isfile(path):
            if not path.endswith(".py"):
                raise ValueError(f'Unable to run "{path}"')
            self._load_file(path, auto_clear)
        else:
            self._load_directory(path, auto_clear)

    def _load_file(self, path: str, auto_clear: bool):
        self._load_stack += 1
        indent = " " * (self._load_stack - 1) * self._INDENT_SIZE
        logger.info(f"{indent}---")
        logger.info(f"{indent}Execute file")
        self._exec_module(path, auto_clear)
        logger.info(f"{indent}End")
        logger.info(f"{indent}---")
        self._load_stack -= 1

    def _load_directory(self, path: str, auto_clear: bool):
        self._load_stack += 1
        indent = " " * (self._load_stack - 1) * self._INDENT_SIZE
        logger.info(f"{indent}---")
        logger.info(f"{indent}Execute files under: {path}")
        file_paths = self._get_python_files(path)
        for file_path in file_paths:
            self._exec_module(file_path, auto_clear)
        logger.info(f"{indent}End")
        logger.info(f"{indent}---")
        self._load_stack -= 1

    def _get_python_files(self, directory: str) -> List[str]:
        python_files: List[str] = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    python_files.append(file_path)

        return sorted(python_files, key=lambda path: path.count(os.sep))

    def _exec_module(self, file_path: str, auto_clear: bool) -> None:
        """write docstring later"""

        # run only 1 time.
        # don't move .add() to bottom. It makes loop
        if file_path in self._executed_files:
            return
        self._executed_files.add(file_path)

        mspec = importlib.util.spec_from_file_location(
            name="dynamically_loaded_module",
            location=file_path,
        )
        if mspec is None:
            # need to investigate what situation
            return
        module = importlib.util.module_from_spec(mspec)

        try:
            if auto_clear:
                # clear previous module's drawing status
                clear()

            # call module for drawing
            indent = " " * (self._load_stack - 1) * self._INDENT_SIZE
            logger.info(f"{indent} - {file_path}")
            mspec.loader.exec_module(module)  # type: ignore[union-attr]
        except Exception as e:  # pylint: disable=broad-exception-caught
            file, line, _, _ = traceback.extract_tb(e.__traceback__)[-1]
            logger.critical(f'{type(e).__name__} at file:"{file}", line:"{line}"')
            logger.critical(str(e))
            logger.debug("")
            logger.debug(traceback.format_exc())
            sys.exit(1)


__loader = Loader()
dload = __loader.dload
