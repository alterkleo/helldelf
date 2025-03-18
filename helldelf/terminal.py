""" ╔═══════════════════════════╗
    ║   HELLDELF - V2.2.1       ║
    ╚═══════════════════════════╝
    terminal.py               """

from typing import Tuple, Optional
from config import (
    MIN_TERMINAL_HEIGHT,
    MIN_TERMINAL_WIDTH,
    CLEAR_SCREEN,
    CURSOR_HIDE,
    CURSOR_SHOW,
    RESET_STYLE,
    CURSOR_HOME
)

import os
import sys

class terminal:
    def __init__(self):
        """Initialize terminal handler with minimum size requirements."""
        self._width, self._height = self._get_size()
        self._original_size = (self._width, self._height)
        self._buffer = []
        self._prev_buffer = {}
        self._initialized = False

    def _get_size(self) -> Tuple[int, int]:
        width, height = os.get_terminal_size()
        return max(width, MIN_TERMINAL_WIDTH), max(height, MIN_TERMINAL_HEIGHT)

    def setup(self) -> None:
        if not self._initialized:
            if os.name == "nt":
                os.system("color")
                os.system(f"mode con: cols={self._width} lines={self._height}")
            sys.stdout.write(CURSOR_HIDE)
            sys.stdout.flush()
            self.clear()
            self._initialized = True

    def cleanup(self) -> None:
        if self._initialized:
            sys.stdout.write(CURSOR_SHOW + RESET_STYLE)
            sys.stdout.write(CLEAR_SCREEN)
            sys.stdout.flush()
            self._initialized = False

    def clear(self) -> None:
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.flush()

    def move_cursor(self, x: int, y: int) -> None:
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    def home(self) -> None:
        sys.stdout.write(CURSOR_HOME)
        sys.stdout.flush()

    def add_to_buffer(self, x: int, y: int, text: str, key: str = None) -> None:
        if key is None:
            key = f"{x},{y}"
        
        content = f"\033[{y};{x}H{text}"
        
        if key not in self._prev_buffer or self._prev_buffer[key] != content:
            self._buffer.append(content)
            self._prev_buffer[key] = content

    def render_buffer(self) -> None:
        if self._buffer:
            sys.stdout.write("".join(self._buffer))
            sys.stdout.flush()
            self._buffer = []

    def clear_buffer(self) -> None:
        self._buffer = []
        self._prev_buffer = {}

    def write(self, text: str) -> None:
        sys.stdout.write(text)
        sys.stdout.flush()

    def write_at(self, x: int, y: int, text: str) -> None:
        self.move_cursor(x, y)
        self.write(text)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def check_size(self) -> bool:
        current = self._get_size()
        if current != (self._width, self._height):
            self._width, self._height = current
            return True
        return False

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()

    def create_box(self, x: int, y: int, width: int, height: int,
                  style: str = "single") -> None:
        styles = {
            "single": ("┌", "┐", "└", "┘", "│", "─"),
            "double": ("╔", "╗", "╚", "╝", "║", "═")
        }
        
        chars = styles.get(style, styles["single"])
        
        # top border
        self.write_at(x, y, chars[0] + chars[5] * (width-2) + chars[1])
        
        # sides
        for i in range(height-2):
            self.write_at(x, y + i + 1, chars[4])
            self.write_at(x + width - 1, y + i + 1, chars[4])
        
        # bottom border
        self.write_at(x, y + height - 1,
                     chars[2] + chars[5] * (width-2) + chars[3])
