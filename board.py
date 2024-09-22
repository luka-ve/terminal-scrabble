from dataclasses import dataclass
from pathlib import Path
from random import sample
from typing import Self
from blessed import Terminal


def double_mirror(
    seq: tuple[tuple : [int, int]], size: int
) -> tuple[tuple : [int, int]]:
    size -= 1
    new_seq = [x for x in seq]
    new_seq.extend([(size - subseq[0], subseq[1]) for subseq in seq])
    new_seq.extend([(subseq[0], size - subseq[1]) for subseq in new_seq])

    return tuple(set(new_seq))


_SPECIAL_TILES: dict[str, tuple[tuple : [int, int]]] = {
    "TRIPLE_WORD": double_mirror(
        ((0, 0), (0, 7), (7, 0)),
        15,
    ),
    "DOUBLE_WORD": double_mirror(
        ((1, 1), (2, 2), (3, 3), (4, 4)),
        15,
    ),
    "DOUBLE_LETTER": double_mirror(
        ((0, 3), (2, 6), (3, 0), (3, 7), (6, 2), (6, 6), (7, 3)), 15
    ),
    "TRIPLE_LETTER": double_mirror(((1, 5), (5, 1), (5, 5)), 15),
}

SPECIAL_TILES = {}
for multiplier, positions in _SPECIAL_TILES.items():
    for position in positions:
        SPECIAL_TILES[position] = multiplier


class ColorMaker:
    def __init__(self, term: Terminal):
        self.term = term

        self.colors = {
            "DOUBLE_WORD": self.term.on_deeppink,
            "TRIPLE_WORD": self.term.on_red,
            "DOUBLE_LETTER": self.term.on_cyan2,
            "TRIPLE_LETTER": self.term.on_blue,
            "EMPTY": self.term.white_on_gray46,
            "EXISTING_LETTER": self.term.black_on_lightgray,
            "NEW_LETTER_VALID": self.term.black_on_lightgreen,
            "NEW_LETTER_INVALID": self.term.black_on_lightred,
        }


class Board:
    def __init__(
        self, terminal: Terminal, height: int, width: int, double_width: bool = True
    ):
        self.height = height
        self.width = width
        self.term = terminal
        self.double_width = double_width

        self._state: list[list[str]] = [
            [" " for j in range(width)] for i in range(height)
        ]
        self.color_maker = ColorMaker(self.term)

        self._dictionary: set[str] = read_word_list("./legal_words.txt")

    @property
    def rendered_board(self) -> list[str]:
        """Returns a prerendered list of strings of the board"""
        lines = []
        for rownum, line in enumerate(self._state):
            new_line = ""
            for colnum, letter in enumerate(line):
                formatter: callable = None
                if letter == " ":
                    multipier_tile = SPECIAL_TILES.get((rownum, colnum))
                    if multipier_tile:
                        formatter = self.color_maker.colors[multipier_tile]
                    else:
                        formatter = self.color_maker.colors["EMPTY"]
                else:
                    formatter = self.color_maker.colors["EXISTING_LETTER"]

                new_line += formatter(letter)

                if self.double_width:
                    new_line += formatter(" ")

            lines.append("".join(new_line))

        return lines

    def set_letter(self, letter, y, x):
        assert len(letter) == 1
        self._state[y][x] = letter

    def evaluate_word(
        self, word: str, y: int, x: int, horizontal: bool
    ) -> tuple[bool, int]:
        pass

    @staticmethod
    def score_letter(letter: str, y: int, x: int):
        pass

    def set_temp_word_overlay(self, word: str, y: int, x: int, horizontal: bool):
        self._current_word_overlay = WordOverlay(word, y, x, horizontal)

    def check_word_legality(self, word: str) -> bool:
        return word in self._dictionary


def read_word_list(file_path: Path) -> set[str]:
    with open(file_path, "r") as f:
        return set(f.readlines())


@dataclass
class WordOverlay:
    word: str
    y: int
    x: int
    horizontal: bool


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.letters: list[str] = []


class LetterBag:
    def __init__(self) -> None:
        self._letters: list[str] = []
        self._letter_points: dict[str, int] = {}

    def draw_letters(self, n) -> list[str]:
        n_adjusted = min(n, len(self._letters))
        letters = sample(self._letters, n_adjusted)
        for letter in letters:
            self._letters.remove(letter)

        return letters

    def exchange_letters(self, letters: list[str]) -> list[str]:
        """Put a list of letters into the bag and then draw the same number of letters from the bag"""
        self._letters.extend(letters)
        return self.draw_letters(len(letters))

    @staticmethod
    def from_csv(file: Path) -> Self:
        with open(file, "r") as f:
            lines = f.readlines()

        bag = LetterBag()
        for line in lines[1:]:
            letter, count, points = line.split(",")
            for i in count:
                bag._letters.append(letter)

            bag._letter_points[letter] = points

        return bag

    def letter_value(self, letter: str) -> int:
        return self._letter_points[letter]
