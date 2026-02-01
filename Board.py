import random


class Board:

    def __init__(self, size):
        self.size = size
        self.grid = self._solved_board()
        self.solved = self.is_solved()

    def reset(self, shuffle_steps=10):
        self.grid = self._solved_board()
        self.shuffle(shuffle_steps)
        return self.get_state()

    def get_state(self):
        return [v for row in self.grid for v in row]

    def get_legal_mask(self):
        zi, zj = self.find_zero()
        mask = [0, 0, 0, 0]

        if zi > 0:
            mask[0] = 1  # up
        if zi < self.size - 1:
            mask[1] = 1  # down
        if zj > 0:
            mask[2] = 1  # left
        if zj < self.size - 1:
            mask[3] = 1  # right

        return mask

    def getMoves(self):
        i, j = self.find_zero()
        moves = []

        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.size and 0 <= nj < self.size:
                moves.append((ni, nj))

        return moves

    def step(self, action):
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        zi, zj = self.find_zero()
        di, dj = dirs[action]
        ni, nj = zi + di, zj + dj

        if not (0 <= ni < self.size and 0 <= nj < self.size):
            return self.get_state(), -0.1, False

        prev_dist = self.manhattan_distance()
        self.grid[zi][zj], self.grid[ni][nj] = self.grid[ni][nj], self.grid[zi][zj]
        new_dist = self.manhattan_distance()

        reward = (prev_dist - new_dist) / (self.size * self.size)
        done = self.is_solved()
        if done: reward = 10.0
        reward = max(min(reward, 10.0), -1.0)
        return self.get_state(), reward, done

    def manhattan_distance(self):
        size = self.size
        dist = 0
        for i in range(size):
            for j in range(size):
                val = self.grid[i][j]
                if val == 0: continue
                target_i = (val - 1) / size
                target_j = (val - 1) % size
                dist += abs(i - target_i) + abs(j - target_j)
        return dist

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
        for row in self.grid:
            for v in row:
                print(v, end='')
