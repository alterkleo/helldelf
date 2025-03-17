""" ╔═══════════════════════════╗
    ║   HELLDELF - V2.2.1       ║
    ╚═══════════════════════════╝
    colors.py                 """

from typing import Tuple, Dict, List
from random import randint

import os

# enable colors in Windows terminal
if os.name == 'nt':
    os.system('color')

COLORS: Dict[str, Tuple[int, int, int]] = {
    # basic
    "black"     : (0, 0, 0),
    "white"     : (255, 255, 255),
    "red"       : (255, 0, 0),
    "green"     : (0, 255, 0),
    "blue"      : (0, 0, 255),

    # warm
    "orange"    : (255, 165, 0),
    "salmon"    : (250, 128, 114),
    "coral"     : (255, 127, 80),
    "crimson"   : (220, 20, 60),
    "maroon"    : (128, 0, 0),
    "pink"      : (255, 192, 203),
    "hotpink"   : (255, 105, 180),
    "magenta"   : (255, 0, 255),

    # cool
    "cyan"      : (0, 255, 255),
    "sky"       : (135, 206, 235),
    "indigo"    : (75, 0, 130),
    "violet"    : (238, 130, 238),
    "purple"    : (128, 0, 128),
    "lavender"  : (230, 230, 250),
    "azure"     : (0, 127, 255),
    "teal"      : (0, 128, 128),

    # earth
    "brown"     : (165, 42, 42),
    "tan"       : (210, 180, 140),
    "gold"      : (255, 215, 0),
    "emerald"   : (46, 204, 113),
    "forest"    : (34, 139, 34),
    "olive"     : (128, 128, 0),
    "lime"      : (0, 255, 0),
    "yellow"    : (255, 255, 0),
}

SCHEMES: Dict[str, List[str]] = {
    "sunset": [
        "maroon",
        "crimson",
        "coral",
        "orange",
        "gold"
    ],

    "ocean": [
        "indigo",
        "blue",
        "sky",
        "cyan",
        "white"
    ],

    "forest": [
        "forest",
        "emerald",
        "green",
        "lime",
        "yellow"
    ],

    "candy": [
        "purple",
        "violet",
        "pink",
        "magenta",
        "salmon"
    ],

    "matrix": [
        "black",
        "forest",
        "green",
        "lime",
        "white"
    ],

    "fire": [
        "maroon",
        "crimson",
        "orange",
        "gold",
        "yellow"
    ],

    "ice": [
        "indigo",
        "azure",
        "sky",
        "cyan",
        "white"
    ],

    "nature": [
        "forest",
        "emerald",
        "olive",
        "lime",
        "yellow"
    ],
}

class rgb:
    """RGB color class with blending and ANSI terminal support"""
    
    def __init__(self, r: int, g: int, b: int):
        """Initialize RGB color with values clamped between 0-255"""
        self.r, self.g, self.b = (
            max(0, min(255, r)),
            max(0, min(255, g)), 
            max(0, min(255, b)),
        )

    @classmethod
    def rand(cls) -> "rgb":
        """Generate random RGB color"""
        return cls(randint(0, 255), randint(0, 255), randint(0, 255))

    def blend(self, other: "rgb", f: float) -> "rgb":
        """Blend with another color using factor f (0-1)"""
        f = max(0, min(1, f))
        return rgb(
            int(self.r + (other.r - self.r) * f),
            int(self.g + (other.g - self.g) * f),
            int(self.b + (other.b - self.b) * f),
        )

    def to_ansi(self, background: bool = False) -> str:
        """Convert to ANSI color code for terminal output"""
        code = 48 if background else 38
        return f"\033[{code};2;{self.r};{self.g};{self.b}m"

    def __str__(self) -> str:
        """String representation of RGB values"""
        return f"rgb({self.r}, {self.g}, {self.b})"

    def __repr__(self) -> str:
        """Object representation"""
        return self.__str__()

