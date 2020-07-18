""" Flip book"""
import argparse
import curses
import os
from time import sleep

from identify import identify

from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

DEFAULT_FRAME_RATE = 4

test_directory = "testing"


def get_file_list(directory: str) -> list:
    # file names must be digits only
    file_list = []
    if os.path.isdir(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            tags = identify.tags_from_path(item_path)
            if "text" in tags and item.isdigit():
                file_list.append(item_path)
        else:
            file_list.sort()
            return file_list
    else:
        return []


def load_file(filename: str) -> Tuple[str, str]:
    with open(filename, "r") as f:
        data = f.read()
    head, tail = os.path.split(filename)
    if "#fb_info#" in data:
        data_first, last_line = data.split("#fb_info#")
        return data_first, f"{tail}" + last_line
    return data, f"{tail}"


def curses_main(screen,
                file_list: List[str],
                frame_rate: int,
                show_last_line: bool,
                goto_slide: int) -> None:
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    play = True
    pointer = goto_slide
    while True:
        size_y, size_x = screen.getmaxyx()
        file_data, last_line = load_file(file_list[pointer])
        screen.clear()
        screen.addstr(0, 0, file_data)
        if show_last_line:
            screen.addstr(size_y - 2, 0, f"#{pointer}  {last_line}")
        screen.refresh()
        if play:
            pointer += 1
        if pointer >= len(file_list):
            break
        ch = screen.getch()
        if ch in [81, 113]:  # q, Q
            break
        elif ch == 115:  # s
            show_last_line = not show_last_line
        elif ch == 112:  # p
            play = not play  # flips play value between True and False
        elif ch == 98 and not play:  # b
            if pointer == 0:
                pass
            else:
                pointer -= 1
        elif ch == 110 and not play:  # n
            if pointer <= len(file_list):
                pointer += 1
        elif ch == 2 and not play:  # ctrl-b
            pointer = 0
        sleep(1 / frame_rate)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",
                        help="root directory containing the text files")
    parser.add_argument("-f", "--frame_rate",
                        choices=[1, 2, 4, 8],
                        default=DEFAULT_FRAME_RATE,
                        type=int,
                        help="frame (slide) per second.  Default 4")
    parser.add_argument("-s", "--show_slide_info", action="store_true",
                        help="Show slide number and slide last line")
    parser.add_argument("-g", "--goto_slide", default=0, type=int,
                        help="goto to slide number")
    args = parser.parse_args(argv)

    file_list = get_file_list(args.directory)
    if len(file_list) == 0:
        print("No flip book text files found")
        return 1
    else:
        curses.wrapper(curses_main,
                       file_list,
                       args.frame_rate,
                       args.show_slide_info,
                       args.goto_slide)
    return 0


if __name__ == "__main__":
    exit(main())
