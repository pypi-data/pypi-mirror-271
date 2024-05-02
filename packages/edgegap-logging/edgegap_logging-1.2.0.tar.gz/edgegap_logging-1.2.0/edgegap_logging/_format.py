from typing import Any

from colorama import Fore as Color


class Format:
    @staticmethod
    def squared(value: Any, color: Color):
        return f'[{color}{value}{Color.RESET}]'

    @staticmethod
    def curled(value: Any, color: Color):
        return '{' + f'{color}{value}{Color.RESET}' + '}'

    @staticmethod
    def parentheses(value: Any, color: Color):
        return f'({color}{value}{Color.RESET})'
