import random


class Board:

    def __init__(self, size):
        self.size = size
        self.grid = self._solved_board()
        self.solved = self.is_solved()

    def _solved_board(self):
        board = []
        value = 1

        for i in range(self.size):
            row = []
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:  # 0 tile at the bottom right
                    row.append(0)
                else:
                    row.append(value)
                    value += 1
            board.append(row)

        return board

    def is_solved(self):
        count = 1
        for i in range(self.size):
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    return self.grid[i][j] == 0
                if self.grid[i][j] != count:
                    return False
                count += 1

    def getMoves(self):
        i, j = self.find_zero()
        moves = []

        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                moves.append((ni, nj))

        return moves

    def find_zero(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return i, j

    def shuffle(self, steps):
        b = self.grid
        for _ in range(steps):
            ni, nj = random.choice(list(self.getMoves()))
            i, j = self.find_zero()
            b[i][j], b[ni][nj] = b[ni][nj], b[i][j]

    def print(self):
        print("")
        for i in range(self.size):
            for j in range(self.size):
                print(self.grid[i][j].__str__(), " ", end='')
            print("")

    def printLegalMoves(self):
        moves = []
        for i in self.getMoves():
            moves.append(self.toCoordinate(i[0], i[1]))
        print(moves)


    def toCoordinate(self, i, j):
        file = chr(ord('a') + j)
        rank = self.size - i
        return f"{file}{rank}"
