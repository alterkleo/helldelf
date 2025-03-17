""" ╔═══════════════════════════╗
    ║   HELLDELF - V2.2.1       ║
    ╚═══════════════════════════╝
    terminal.py               """

from typing import Tuple, Optional
from config import (
    MIN_TERMINAL_WIDTH,
    MIN_TERMINAL_HEIGHT,
    CLEAR_SCREEN,
    CURSOR_HIDE,
    CURSOR_SHOW,
    RESET_STYLE,
    CURSOR_HOME
)

import os
import sys

class terminal:
    """Terminal handler for ANSI-compatible terminals.
    
    Provides methods for terminal manipulation, cursor control,
    and screen management while ensuring proper cleanup.
    
    Properties:
        width (int): Current terminal width
        height (int): Current terminal height
    """
    
    def __init__(self):
        """Initialize terminal handler with minimum size requirements."""
        self._width, self._height = self._get_size()
        self._original_size = (self._width, self._height)
        self._buffer = []
        self._prev_buffer = {}
        self._initialized = False

    def _get_size(self) -> Tuple[int, int]:
        """Get current terminal size enforcing minimums.
        
        Returns:
            Tuple[int, int]: Terminal width and height
        """
        width, height = os.get_terminal_size()
        return max(width, MIN_TERMINAL_WIDTH), max(height, MIN_TERMINAL_HEIGHT)

    def setup(self) -> None:
        """Initialize terminal for display.
        
        - Enables color support on Windows
        - Sets terminal size
        - Hides cursor
        - Clears screen
        """
        if not self._initialized:
            if os.name == "nt":
                os.system("color")
                os.system(f"mode con: cols={self._width} lines={self._height}")
            sys.stdout.write(CURSOR_HIDE)
            sys.stdout.flush()
            self.clear()
            self._initialized = True

    def cleanup(self) -> None:
        """Restore terminal to original state.
        
        - Shows cursor
        - Resets colors and styles
        - Clears screen
        """
        if self._initialized:
            sys.stdout.write(CURSOR_SHOW + RESET_STYLE)
            sys.stdout.write(CLEAR_SCREEN)
            sys.stdout.flush()
            self._initialized = False

    def clear(self) -> None:
        """Clear screen and move cursor to home position."""
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.flush()

    def move_cursor(self, x: int, y: int) -> None:
        """Move cursor to specific position.
        
        Args:
            x (int): Column position (1-based)
            y (int): Row position (1-based)
        """
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    def home(self) -> None:
        """Move cursor to home position (1,1)."""
        sys.stdout.write(CURSOR_HOME)
        sys.stdout.flush()

    def add_to_buffer(self, x: int, y: int, text: str, key: str = None) -> None:
        """Add content to buffer with differential updates.
        
        Args:
            x (int): Column position
            y (int): Row position
            text (str): Text to display
            key (str, optional): Unique key for content. Defaults to "x,y".
        """
        if key is None:
            key = f"{x},{y}"
        
        content = f"\033[{y};{x}H{text}"
        
        if key not in self._prev_buffer or self._prev_buffer[key] != content:
            self._buffer.append(content)
            self._prev_buffer[key] = content

    def render_buffer(self) -> None:
        """Render buffered content to screen."""
        if self._buffer:
            sys.stdout.write("".join(self._buffer))
            sys.stdout.flush()
            self._buffer = []

    def clear_buffer(self) -> None:
        """Clear the buffer without rendering."""
        self._buffer = []
        self._prev_buffer = {}

    def write(self, text: str) -> None:
        """Write text directly to terminal.
        
        Args:
            text (str): Text to write
        """
        sys.stdout.write(text)
        sys.stdout.flush()

    def write_at(self, x: int, y: int, text: str) -> None:
        """Write text at specific position.
        
        Args:
            x (int): Column position
            y (int): Row position
            text (str): Text to write
        """
        self.move_cursor(x, y)
        self.write(text)

    @property
    def width(self) -> int:
        """Current terminal width."""
        return self._width

    @property
    def height(self) -> int:
        """Current terminal height."""
        return self._height

    def check_size(self) -> bool:
        """Check if terminal size has changed.
        
        Returns:
            bool: True if size changed, False otherwise
        """
        current = self._get_size()
        if current != (self._width, self._height):
            self._width, self._height = current
            return True
        return False

    def __enter__(self):
        """Context manager entry.
        
        Allows using terminal with 'with' statement:
        with terminal() as term:
            term.write("Hello")
        """
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()

    def create_box(self, x: int, y: int, width: int, height: int,
                  style: str = "single") -> None:
        """Create a box with specified dimensions.
        
        Args:
            x (int): Starting X position
            y (int): Starting Y position
            width (int): Box width
            height (int): Box height
            style (str, optional): Box style ("single" or "double").
                                 Defaults to "single".
        """
        styles = {
            "single": ("┌", "┐", "└", "┘", "│", "─"),
            "double": ("╔", "╗", "╚", "╝", "║", "═")
        }
        
        chars = styles.get(style, styles["single"])
        
        # Top border
        self.write_at(x, y, chars[0] + chars[5] * (width-2) + chars[1])
        
        # Sides
        for i in range(height-2):
            self.write_at(x, y + i + 1, chars[4])
            self.write_at(x + width - 1, y + i + 1, chars[4])
        
        # Bottom border
        self.write_at(x, y + height - 1,
                     chars[2] + chars[5] * (width-2) + chars[3])
