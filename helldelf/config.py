""" ╔═══════════════════════════╗
    ║   HELLDELF - V2.2.1       ║
    ╚═══════════════════════════╝
    config.py                 """

from datetime import datetime
from typing import Dict, Any

# metadata
CREATED_AT  = "2025"
VERSION     = "2.1.1" 
AUTHOR      = "alterkleo"

# animations
DEFAULT_DURATION  = 3.0
DEFAULT_DENSITY   = 0.2
DEFAULT_DELAY     = 0.1
DEFAULT_STEPS     = 10
DEFAULT_FPS       = 0.05

# color
DEFAULT_BACKGROUND  = "black"
DEFAULT_INTENSITY   = 0.8
DEFAULT_SCHEME      = "sunset"
DEFAULT_COLOR       = "cyan"

# terminal
MIN_TERMINAL_WIDTH    = 80
MIN_TERMINAL_HEIGHT   = 24

CLEAR_SCREEN      = "\033[2J\033[H"
CURSOR_HIDE       = "\033[?25l"
CURSOR_SHOW       = "\033[?25h"
RESET_STYLE       = "\033[0m"
CURSOR_HOME       = "\033[H"

# performance
BUFFER_SIZE     = 1024
UPDATE_RATE     = 0.05
MAX_DROPS       = 100
MIN_SPEED       = 0.5
MAX_SPEED       = 1.5

# effect
MATRIX_DENSITY      = 0.2
GLITCH_PROBABILITY  = 0.1
SHAKE_PROBABILITY   = 0.3
RAINBOW_COLORS      = [
"red",
"yellow",
"green",
"cyan",
"blue",
"magenta"
]

# system
DEBUG     = False
SAFE_MODE = False
LOG_LEVEL = "INFO"

# default
DEFAULT_CONFIG: Dict[str, Any] = {
    "animation": {
        "fps"                   : DEFAULT_FPS,
        "duration"              : DEFAULT_DURATION,
        "density"               : DEFAULT_DENSITY,
        "delay"                 : DEFAULT_DELAY,
        "steps"                 : DEFAULT_STEPS
    },
    "color": {
        "default"               : DEFAULT_COLOR,
        "scheme"                : DEFAULT_SCHEME,
        "background"            : DEFAULT_BACKGROUND,
        "intensity"             : DEFAULT_INTENSITY
    },
    "terminal": {
        "min_width"             : MIN_TERMINAL_WIDTH,
        "min_height"            : MIN_TERMINAL_HEIGHT
    },
    "performance": {
        "buffer_size"           : BUFFER_SIZE,
        "max_drops"             : MAX_DROPS,
        "min_speed"             : MIN_SPEED,
        "max_speed"             : MAX_SPEED,
        "update_rate"           : UPDATE_RATE
    },
    "effects": {
        "matrix_density"        : MATRIX_DENSITY,
        "glitch_probability"    : GLITCH_PROBABILITY,
        "shake_probability"     : SHAKE_PROBABILITY
    },
    "system": {
        "debug"                 : DEBUG,
        "safe_mode"             : SAFE_MODE,
        "log_level"             : LOG_LEVEL
    }
}