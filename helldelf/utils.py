from typing import Dict, List, Tuple, Union, Optional, Callable

import time
import sys
import os

def get_terminal_size() -> Tuple[int, int]:
    return os.get_terminal_size()

def write_stdout(text: str) -> None:
    sys.stdout.write(text)
    sys.stdout.flush()
