from Board import Board
from UI import UI


def main():
    size = 5
    board = Board(size)
    board.shuffle(200)
    ui = UI(board, size * 100)
    ui.startPrint()


if __name__ == "__main__":
    main()
