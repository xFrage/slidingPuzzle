import pygame
import sys


class UI:
    def __init__(self, board, windowSize):
        pygame.init()
        self.board = board
        self.size = len(board.grid)
        self.windowSize = windowSize
        self.tileSize = windowSize // self.size
        self.screen = pygame.display.set_mode((self.windowSize, self.windowSize))
        self.font = pygame.font.SysFont(None, 48)
        self.startPrint()

    def draw(self, board):
        self.screen.fill((30, 30, 30))
        b = board.grid
        tileSize = self.tileSize
        for i in range(self.size):
            for j in range(self.size):
                v = b[i][j]
                if v == 0:
                    continue
                r = pygame.Rect(j * tileSize, i * tileSize, tileSize, tileSize)
                pygame.draw.rect(self.screen, (70, 130, 180), r, border_radius=8)
                txt = self.font.render(str(v), True, (255, 255, 255))
                self.screen.blit(txt, txt.get_rect(center=r.center))
        pygame.display.flip()

    def startPrint(self):
        board = self.board
        grid = board.grid
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = e.pos
                    i, j = y // self.tileSize, x // self.tileSize
                    zi, zj = board.find_zero()
                    if abs(i - zi) + abs(j - zj) == 1:
                        grid[zi][zj], grid[i][j] = grid[i][j], grid[zi][zj]
            self.draw(self.board)
