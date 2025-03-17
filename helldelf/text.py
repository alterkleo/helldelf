from colors import COLORS, SCHEMES, rgb

class txt:
    def __init__(self, text: str):
        self.bg, self.fx, self.cols, self.text = None, [], [], text

    def style(self, *styles: str) -> "txt":
        self.fx.extend(s for s in styles if s in COLORS)
        return self

    def rbw(self) -> "txt":
        cols = [
        "red",
        "yellow",
        "green",
        "cyan",
        "blue",
        "magenta"
        ]
        out = ""
        for i, char in enumerate(self.text):
            if not char.isspace():
                c = COLORS[cols[i % len(cols)]]
                out += f"\033[38;2;{c[0]};{c[1]};{c[2]}m{char}"
            else:
                out += char
        self.text = out + "\033[0m"
        return self

    def __str__(self) -> str:
        return (
            "".join(
                f"\033[38;2;{COLORS[fx][0]};{COLORS[fx][1]};{COLORS[fx][2]}m"
                for fx in self.fx
            )
            + self.text
            + "\033[0m"
        )

class grad:
    def __init__(self, text: str):
        self.text = text

    def flow(self, scheme: str = "sunset", steps: int = None) -> str:
        colors = SCHEMES.get(scheme, SCHEMES["sunset"])
        steps = steps or len(self.text)
        rgbs = [rgb(*COLORS[c]) for c in colors]
        segs, cps, res, idx = len(rgbs) - 1, steps // (len(rgbs) - 1), "", 0

        for i in range(segs):
            c1, c2 = rgbs[i], rgbs[i + 1]
            for step in range(cps):
                if idx >= len(self.text):
                    break
                p = step / cps
                r = int(c1.r + (c2.r - c1.r) * p)
                g = int(c1.g + (c2.g - c1.g) * p)
                b = int(c1.b + (c2.b - c1.b) * p)
                if not self.text[idx].isspace():
                    res += f"\033[38;2;{r};{g};{b}m{self.text[idx]}"
                else:
                    res += self.text[idx]
                idx += 1
        return res + "\033[0m"