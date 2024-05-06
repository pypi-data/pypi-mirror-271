from typing import List

from colorama import Back, Fore, Style
from halo import Halo

TEXT_ANSWER = "[answer]:"
TEXT_COMMAND = "[command]:"
TEXT_CONFIRMATION = "run [y/n]:"

CONFIRM_OPTIONS = ["y", "yes"]


class Console:
    # TODO improve colors
    def __init__(self):
        self.spinner = Halo(text="thinking...\n", spinner=get_zed_spinner())
        self.column_width = max(
            [len(t) for t in [TEXT_ANSWER, TEXT_COMMAND, TEXT_CONFIRMATION]]
        )

    def print_answer(self, answer: str):
        answer_title = styled(
            text=f"{TEXT_ANSWER:>{self.column_width}}",
            style=Style.BRIGHT,
            color=Fore.LIGHTGREEN_EX,
        )
        print(f"{answer_title} {answer}")

    def print_command(self, command: str):
        command_title = styled(
            text=f"{TEXT_COMMAND:>{self.column_width}}",
            style=Style.BRIGHT,
            color=Fore.LIGHTCYAN_EX,
        )
        print(f"{command_title} {command}")

    def await_confirmation(self) -> bool:
        confirmation_title = styled(
            text=f"{TEXT_CONFIRMATION:>{self.column_width}}",
            style=Style.BRIGHT,
            color=Fore.MAGENTA,
        )
        return input(f"{confirmation_title} ").lower() in CONFIRM_OPTIONS

    def print_run_command(self, command: str):
        print(
            styled(text=f"\n$ {command}\n", style=Style.DIM, color=Fore.LIGHTWHITE_EX)
        )

    def print_retry(self):
        print(
            styled(
                text="Sorry, but I couldn't find an answer. Please try again.",
                color=Fore.LIGHTRED_EX,
            )
        )

    def print_farewell(self):
        print(
            styled(text="Command not ran.", style=Style.DIM, color=Fore.LIGHTWHITE_EX)
        )

    def show_spinner(self):
        self.spinner.start()

    def hide_spinner(self):
        self.spinner.stop()


def styled(text: str, color: Fore = "", back: Back = "", style: Style = "") -> str:
    return f"{style}{back}{color}{text}{Style.RESET_ALL}"


def get_zed_spinner() -> dict:
    frames: List[str] = []
    for color in [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW]:
        cycle = [
            styled("d       ", color=color),
            styled("ed      ", color=color),
            styled("zed     ", color=color),
            styled(" zed    ", color=color),
            styled("  zed   ", color=color),
            styled("   zed  ", color=color),
            styled("    zed ", color=color),
            styled("     zed", color=color),
            styled("      ze", color=color),
            styled("       z", color=color),
            styled("        ", color=color),
        ]
        frames.extend(cycle)
    return {
        "interval": 60,
        "frames": frames,
    }
