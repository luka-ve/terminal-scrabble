import string
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

    print(f"{term.home}{term.black_on_skyblue}")

    current_word = ""

    with term.cbreak():
        keyval = ""
        while True:
            keyval = term.inkey()
            if keyval.name in ("KEY_BACKSPACE", "KEY_DELETE"):
                current_word = current_word[:-1]
            elif keyval.lower() in string.ascii_lowercase:
                current_word += keyval.upper()

            # Draw current word
            with term.location(0, term.height - 3):
                print(
                    f"{term.black_on_skyblue(current_word)}{term.black_on_skyblue((" ") * (15 - len(current_word)))}"
                )


if __name__ == "__main__":
    exit(main())
