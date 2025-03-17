""" ╔═══════════════════════════╗
    ║   HELLDELF - V2.2.1       ║
    ╚═══════════════════════════╝
    Music Player - 2025      """

import asyncio
import random
import signal
import math
import sys
import os
from datetime import datetime, UTC
from typing import List, Dict, Any

# Constantes para la terminal
MIN_TERMINAL_WIDTH = 80
MIN_TERMINAL_HEIGHT = 24
CLEAR_SCREEN = "\033[2J"
CURSOR_HIDE = "\033[?25l"
CURSOR_SHOW = "\033[?25h"
RESET_STYLE = "\033[0m"
CURSOR_HOME = "\033[H"

# Colores básicos
COLORS = {
    "red": (255, 50, 50),
    "green": (50, 255, 50),
    "blue": (50, 50, 255),
    "cyan": (50, 255, 255),
    "purple": (255, 50, 255),
    "yellow": (255, 255, 50),
    "orange": (255, 165, 0),
    "white": (255, 255, 255),
    "gray": (128, 128, 128)
}

class RGB:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b
    
    def to_ansi(self) -> str:
        return f"\033[38;2;{self.r};{self.g};{self.b}m"
    
    def blend(self, other: 'RGB', factor: float) -> 'RGB':
        factor = max(0, min(1, factor))
        return RGB(
            int(self.r + (other.r - self.r) * factor),
            int(self.g + (other.g - self.g) * factor),
            int(self.b + (other.b - self.b) * factor)
        )

class Terminal:
    def __init__(self):
        self.width, self.height = self._get_size()
        self.buffer = []
        self._prev_buffer = {}

    def _get_size(self):
        width, height = os.get_terminal_size()
        return max(width, MIN_TERMINAL_WIDTH), max(height, MIN_TERMINAL_HEIGHT)

    def setup(self):
        if os.name == "nt":
            os.system("color")
        sys.stdout.write(CURSOR_HIDE)
        sys.stdout.flush()
        self.clear()

    def cleanup(self):
        sys.stdout.write(CURSOR_SHOW + RESET_STYLE)
        sys.stdout.flush()

    def clear(self):
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.flush()

    def add_to_buffer(self, x: int, y: int, text: str, key: str = None):
        if key is None:
            key = f"{x},{y}"
        content = f"\033[{y};{x}H{text}"
        if key not in self._prev_buffer or self._prev_buffer[key] != content:
            self.buffer.append(content)
            self._prev_buffer[key] = content

    def render_buffer(self):
        if self.buffer:
            print("".join(self.buffer), end="", flush=True)
            self.buffer = []

class Track:
    def __init__(self, title: str, artist: str, duration: int):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.progress = 0

    def format_time(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    @property
    def duration_str(self) -> str:
        return self.format_time(self.duration)

    @property
    def progress_str(self) -> str:
        return self.format_time(self.progress)

class MusicPlayer:
    def __init__(self):
        self.term = Terminal()
        self.running = True
        self.frame = 0
        self.playing = True
        self.current_track_idx = 0
        self.volume = 80
        
        self.playlist = [
            Track("Cyberpunk Dreams", "HellDelf", 245),
            Track("Neon Nights", "ByteRunner", 198),
            Track("Digital Rain", "Terminal Prophet", 312),
            Track("Ghost in the Code", "Syntax Error", 274),
            Track("Binary Sunset", "Alt3rkl30", 183),
        ]
        
        self.frequencies = [0.0] * 32
        self.setup()

    def setup(self):
        self.term.setup()
        signal.signal(signal.SIGINT, lambda x, y: self.cleanup())

    def cleanup(self):
        self.term.cleanup()
        self.running = False
        sys.exit(0)

    async def draw_header(self):
        # Title
        title = "♫ HELLDELF MUSIC PLAYER ♫"
        x = (self.term.width - len(title)) // 2
        color = RGB(*COLORS["cyan"])
        self.term.add_to_buffer(x, 1, f"{color.to_ansi()}{title}{RESET_STYLE}")
        
        # Current time
        time_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        x = (self.term.width - len(time_str)) // 2
        color = RGB(*COLORS["gray"])
        self.term.add_to_buffer(x, 2, f"{color.to_ansi()}{time_str}{RESET_STYLE}")

    async def draw_track_info(self):
        track = self.playlist[self.current_track_idx]
        
        # Track title
        title = f"♫ {track.title} - {track.artist}"
        x = (self.term.width - len(title)) // 2
        color = RGB(*COLORS["purple"])
        self.term.add_to_buffer(x, 4, f"{color.to_ansi()}{title}{RESET_STYLE}")
        
        # Progress bar
        progress_width = 50
        progress_pos = int((track.progress / track.duration) * progress_width)
        x = (self.term.width - progress_width) // 2
        
        # Time
        time_text = f"{track.progress_str} / {track.duration_str}"
        time_x = (self.term.width - len(time_text)) // 2
        self.term.add_to_buffer(time_x, 5, time_text)
        
        # Bar
        for i in range(progress_width):
            if i < progress_pos:
                color = RGB(*COLORS["cyan"])
                char = "━"
            else:
                color = RGB(*COLORS["gray"])
                char = "─"
            self.term.add_to_buffer(x + i, 6, f"{color.to_ansi()}{char}{RESET_STYLE}")

    async def draw_playlist(self):
        x = 5
        y = 8
        
        # Playlist title
        color = RGB(*COLORS["cyan"])
        self.term.add_to_buffer(x, y, f"{color.to_ansi()}PLAYLIST:{RESET_STYLE}")
        
        # Tracks
        for i, track in enumerate(self.playlist):
            color = RGB(*COLORS["white"]) if i == self.current_track_idx else RGB(*COLORS["gray"])
            indicator = "▶ " if i == self.current_track_idx and self.playing else "  "
            self.term.add_to_buffer(
                x, y + i + 1,
                f"{color.to_ansi()}{indicator}{track.title} - {track.duration_str}{RESET_STYLE}"
            )

    async def draw_visualization(self):
        # Update frequencies
        for i in range(len(self.frequencies)):
            target = abs(math.sin(self.frame * 0.1 + i * 0.2)) * 0.7 + random.random() * 0.3
            self.frequencies[i] += (target - self.frequencies[i]) * 0.3
        
        # Draw bars
        width = min(32, self.term.width - 10)
        x = (self.term.width - width) // 2
        y = 15
        
        for i in range(width):
            height = int(self.frequencies[i] * 8)
            for h in range(height):
                color = RGB(*COLORS["purple"]).blend(RGB(*COLORS["cyan"]), h/8)
                char = "■"
                self.term.add_to_buffer(x + i, y - h, f"{color.to_ansi()}{char}{RESET_STYLE}")

    async def update(self):
        if self.playing:
            track = self.playlist[self.current_track_idx]
            track.progress += 0.1
            if track.progress >= track.duration:
                track.progress = 0
                self.current_track_idx = (self.current_track_idx + 1) % len(self.playlist)

    async def run(self):
        try:
            self.term.clear()
            
            while self.running:
                await self.update()
                
                await self.draw_header()
                await self.draw_track_info()
                await self.draw_playlist()
                await self.draw_visualization()
                
                self.term.render_buffer()
                self.frame += 1
                await asyncio.sleep(0.1)
                
        except Exception as e:
            print(f"\033[31mError: {str(e)}\033[0m")
        finally:
            self.cleanup()

if __name__ == "__main__":
    try:
        player = MusicPlayer()
        asyncio.run(player.run())
    except KeyboardInterrupt:
        print(CURSOR_SHOW + RESET_STYLE)