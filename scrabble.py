from blessed import Terminal
from board import Board, LetterBag, Player


def main():
    term = Terminal()

    print(term.clear())

    board = Board(term, 15, 15)

    player = Player("Luki")
    letter_bag = LetterBag.from_csv("./letters.csv")
    player.letters = letter_bag.draw_letters(7)

    with term.location(0, term.height - 1):
        print(f"Your letters: {' '.join(player.letters)}")

    board_padding = (2, 2)

    with term.location(0, board_padding[1]):
        state = board.rendered_board
        for line in state:
            print(" " * board_padding[0], end="")
            print(line)


def create_board(height: int, width: int) -> list[str]:
    return [" " * width for i in range(height)]


if __name__ == "__main__":
    exit(main())
