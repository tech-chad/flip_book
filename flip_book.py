""" Flip book"""
import argparse
import curses
import os
from time import sleep

from identify import identify

from typing import List
from typing import Optional
from typing import Sequence

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


def load_file(filename: str) -> str:
    with open(filename, "r") as f:
        data = f.read()
    return data


def curses_main(screen, file_list: List[str]) -> None:
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    play = True
    pointer = 0
    while True:
        file_data = load_file(file_list[pointer])
        screen.clear()
        screen.addstr(0, 0, file_data)
        screen.refresh()
        if play:
            pointer += 1
        if pointer >= len(file_list):
            break
        ch = screen.getch()
        if ch in [81, 113]:  # q, Q
            break
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
        sleep(0.25)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",
                        help="root directory containing the text files")
    args = parser.parse_args(argv)

    file_list = get_file_list(args.directory)
    if len(file_list) == 0:
        print("No flip book text files found")
        return 1
    else:
        curses.wrapper(curses_main, file_list)
    return 0


if __name__ == "__main__":
    exit(main())
