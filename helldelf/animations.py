""" ╔═══════════════════════════╗
    ║   HELLDELF - V2.2.1       ║
    ╚═══════════════════════════╝
    animations.py             """

from random import random, randint, choice, uniform
from effects import EFFECTS, PATTERNS, FX
from typing import Dict, Any
from itertools import cycle
from colors import COLORS

import time
import sys
import os

class fx:
    def __init__(self, text: str):
        self.text, self.effect, self.dur, self.fps = text, None, 0, 0.05

    def play(self, name: str, dur: float = 3.0) -> None:
        if name in FX:
            self.effect, self.dur = FX[name], dur
            self._run()

    def _run(self) -> None:
        st = time.time()
        while time.time() - st < self.dur:
            t, out = time.time() - st, ""
            for i, char in enumerate(self.text):
                if not char.isspace():
                    off = self.effect(i, t)
                    if isinstance(off, tuple):
                        x, y = off
                        out += f"\033[{int(y)};{int(x)}H{char}"
                    else:
                        out += f"\033[{int(off)}C{char}"
                else:
                    out += char
            sys.stdout.write("\r" + out)
            sys.stdout.flush()
            time.sleep(self.fps)
        sys.stdout.write("\r" + self.text + "\n")
        sys.stdout.flush()

class anim:
    def __init__(self, text: str):
        self.text = text

    def load(self, style: str = "spin", dur: float = 3.0, color: str = "cyan") -> None:
        chars = PATTERNS.get(style, PATTERNS["spin"])
        col = COLORS.get(color, COLORS["cyan"])
        end = time.time() + dur

        while time.time() < end:
            for char in cycle(chars):
                if time.time() > end:
                    break
                sys.stdout.write(
                    f"\r\033[38;2;{col[0]};{col[1]};{col[2]}m{char}\033[0m {self.text}"
                )
                sys.stdout.flush()
                time.sleep(0.1)
        sys.stdout.write("\r" + " " * (len(self.text) + 2) + "\r")
        sys.stdout.flush()

def matrix(self, dur: float = 5.0, density: float = 0.2) -> None:
    terminal = Terminal()
    width, height = terminal.width, terminal.height - 1
    drops, chars = [], list(EFFECTS["matrix"])
    greens = [
        f"\033[38;2;{int(40+i*215/height)};{int(160+i*95/height)};40m"
        for i in range(height)
    ]
    end = time.time() + dur

    while time.time() < end:
        terminal.clear()
        if random() < density:
            drops.append(
                {
                    "x": randint(0, width - 1),
                    "y": 0,
                    "speed": uniform(0.5, 1.5),
                    "len": randint(3, 10),
                    "char": choice(chars),
                    "update": 0,
                }
            )
        screen = [[" " for _ in range(width)] for _ in range(height)]
        new_drops = []

        for drop in drops:
            drop["update"] += drop["speed"]
            if drop["update"] >= 1:
                drop["y"] += 1
                drop["update"] = 0
                drop["char"] = choice(chars)
            if drop["y"] < height:
                for i in range(drop["len"]):
                    y = int(drop["y"]) - i
                    if 0 <= y < height:
                        intensity = 1 - (i / drop["len"])
                        color = greens[min(height - 1, int(y * intensity))]
                        screen[y][drop["x"]] = f"{color}{choice(chars)}"
                new_drops.append(drop)
        drops = new_drops
        for line in screen:
            print("".join(char if char != " " else " " for char in line))
        time.sleep(0.05)
    print(RESET_STYLE)