import tcod
from tcod.console import Console
from typing import Tuple


def create_console(width: int, height: int) -> Console:
    return Console(width, height, "C")


def paste_console_on(pasted: Console,
                     target: Console,
                     pasted_top_left_position: Tuple[int, int],
                     opacity: float = 1.0) -> None:
    tcod.console_blit(pasted, 0, 0, 0, 0, target, pasted_top_left_position[0], pasted_top_left_position[1], opacity, opacity)
