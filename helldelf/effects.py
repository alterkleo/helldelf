""" ╔═══════════════════════════╗
    ║   HELLDELF - V2.2.1       ║
    ╚═══════════════════════════╝
    effects.py                """

from random import randint, random

import math

EFFECTS = {
    "matrix"        : "日ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ",
    "kanji"         : "゠クケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヰヱヲン",
    "blocks"        : "█▀▄▌▐░▒▓",
    "shades"        : "░▒▓█",
    "box"           : "┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬═║",
    "round"         : "╭╮╰╯╱╲",
    "arrows"        : "←↑→↓↖↗↘↙",
    "special"       : "♠♣♥♦★☆⚡☼",
    "dots"          : "⠁⠂⠄⡀⢀⠠⠐⠈",
    "braille"       : "⣾⣽⣻⢿⡿⣟⣯⣷",
}

PATTERNS = {
    "spin"          : "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
    "pulse"         : "█▓▒░ ░▒▓█",
    "snake"         : "⣾⣽⣻⢿⡿⣟⣯⣷",
    "line"          : "|/-\\",
    "grow"          : "▁▂▃▄▅▆▇█",
    "bounce"        : "⠁⠂⠄⡀⢀⠠⠐⠈",
    "flow"          : "←↖↑↗→↘↓↙",
}

FX = {
    "wave"          : lambda x, t: math.sin(x / 2 + t * 3) * 2,
    "bounce"        : lambda x, t: abs(math.sin(t * 2 + x / 3)) * 3,
    "shake"         : lambda x, t: randint(-2, 2) if random() < 0.3 else 0,
    "spiral"        : lambda x, t: (math.sin(x / 4 + t * 2), math.cos(x / 4 + t * 2)),
    "glitch"        : lambda x, t: randint(-3, 3) if random() < 0.1 else 0,        # alpha
    "pulse"         : lambda x, t: math.sin(t * 4) * 2,
    "zigzag"        : lambda x, t: (x % 3) * math.sin(t * 2) * 2,
    "rotate"        : lambda x, t: (math.cos(t) * x / 4, math.sin(t) * x / 4),
    "expand"        : lambda x, t: abs(math.sin(t * 2)) * x / 3,
    "shrink"        : lambda x, t: (1 - abs(math.sin(t * 2))) * x / 3,              # beta
}