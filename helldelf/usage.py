from colors import COLORS, SCHEMES, rgb
from datetime import datetime, UTC

import asyncio
import signal
import math
import sys
import os

class demo:
    def __init__(self):
        self.running = True
        self.frame = 0
        self.width = 80
        self.height = 25
        self.buffer = []
        self.setup_terminal()

    def setup_terminal(self):
        if os.name == "nt":
            os.system("color")
            os.system(
                f"mode con: cols={self.width} lines={self.height}"
            )
        print(
            "\033[?25l"
        )  # hide cursor
        signal.signal(
            signal.SIGINT,
            lambda x, y: self.cleanup(),
        )

    def cleanup(self):
        print(
            "\033[?25h\033[0m"
        )  # show cursor and reset colors
        self.running = False
        sys.exit(0)

    def clear_screen(self):
        print(
            "\033[H", end="", flush=True
        )

    def render_frame(self):
        print(
            "".join(self.buffer),
            end="",
            flush=True,
        )
        self.buffer = []

    def add_to_buffer(
        self, x: int, y: int, text: str
    ):
        self.buffer.append(
            f"\033[{y};{x}H{text}"
        )

    async def draw_border(self):
        top_border = (
            "╔"
            + "═" * (self.width - 2)
            + "╗"
        )
        bottom_border = (
            "╚"
            + "═" * (self.width - 2)
            + "╝"
        )
        empty_line = (
            "║"
            + " " * (self.width - 2)
            + "║"
        )
        color = rgb(
            *COLORS["cyan"]
        ).blend(
            rgb(*COLORS["purple"]),
            (
                math.sin(
                    self.frame * 0.1
                )
                + 1
            )
            / 2,
        )

        self.add_to_buffer(
            1,
            1,
            f"{color.to_ansi()}{top_border}\033[0m",
        )
        for i in range(2, self.height):
            self.add_to_buffer(
                1,
                i,
                f"{color.to_ansi()}{empty_line}\033[0m",
            )
        self.add_to_buffer(
            1,
            self.height,
            f"{color.to_ansi()}{bottom_border}\033[0m",
        )

    async def draw_header(self):
        title = (
            " HellDelf Color System "
        )
        x = (
            self.width - len(title)
        ) // 2
        color = rgb(
            *COLORS["cyan"]
        ).blend(
            rgb(*COLORS["purple"]),
            (
                math.sin(
                    self.frame * 0.1
                )
                + 1
            )
            / 2,
        )
        self.add_to_buffer(
            x,
            3,
            f"{color.to_ansi()}{title}\033[0m",
        )

        current_time = datetime.now(
            UTC
        ).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )
        x = (
            self.width
            - len(current_time)
        ) // 2
        self.add_to_buffer(
            x,
            5,
            f"{rgb(*COLORS['azure']).to_ansi()}{current_time}\033[0m",
        )

        user = "User: alterkleo"
        x = (
            self.width - len(user)
        ) // 2
        self.add_to_buffer(
            x,
            6,
            f"{rgb(*COLORS['purple']).to_ansi()}{user}\033[0m",
        )

    async def draw_schemes(self):
        y = 8
        for (
            scheme_name,
            colors,
        ) in SCHEMES.items():
            scheme_title = f"► {scheme_name.upper()}"
            self.add_to_buffer(
                4,
                y,
                f"{rgb(*COLORS['cyan']).to_ansi()}{scheme_title}\033[0m",
            )

            x = 25
            for color_name in colors:
                color = rgb(
                    *COLORS[color_name]
                )
                self.add_to_buffer(
                    x,
                    y,
                    f"{color.to_ansi()}■■■\033[0m",
                )
                x += 4
            y += 2

    async def draw_random_colors(self):
        y = self.height - 7
        header = "Random Color Samples:"
        self.add_to_buffer(
            4,
            y,
            f"{rgb(*COLORS['azure']).to_ansi()}{header}\033[0m",
        )

        for i in range(3):
            color = rgb.rand()
            self.add_to_buffer(
                4,
                y + i + 1,
                f"{color.to_ansi()}■■■ Sample {i+1}\033[0m",
            )

    async def run(self):
        try:
            while self.running:
                self.clear_screen()

                await self.draw_border()
                await self.draw_header()
                await self.draw_schemes()
                await self.draw_random_colors()

                exit_msg = "Press Ctrl+C to exit"
                x = (
                    self.width
                    - len(exit_msg)
                ) // 2
                color = rgb(
                    *COLORS["azure"]
                ).blend(
                    rgb(
                        *COLORS[
                            "purple"
                        ]
                    ),
                    (
                        math.sin(
                            self.frame
                            * 0.1
                        )
                        + 1
                    )
                    / 2,
                )
                self.add_to_buffer(
                    x,
                    self.height - 2,
                    f"{color.to_ansi()}{exit_msg}\033[0m",
                )

                self.render_frame()
                self.frame += 1
                await asyncio.sleep(0.1)

        except Exception as e:
            print(
                f"\033[31mError: {str(e)}\033[0m"
            )
        finally:
            self.cleanup()


if __name__ == "__main__":
    try:
        demo = demo()
        asyncio.run(demo.run())
    except KeyboardInterrupt:
        print(
            "\033[?25h\033[0m"
        )  # ensure terminal is reset
