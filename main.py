import pygame, random, sys

from Board import Board

SIZE = 3
WINDOW_SIZE = 400
TILE = WINDOW_SIZE // SIZE
FONT_SIZE = 48

pygame.init()

board = Board(SIZE)
board.shuffle(200)
board.print()
board.printLegalMoves()



"""
screen = pygame.display.set_mode((SIZE, SIZE))
font = pygame.font.SysFont(None, FONT_SIZE)


def draw(board):
    screen.fill((30, 30, 30))
    b = board.grid
    for i in range(N):
        for j in range(N):
            v = b[i][j]
            if v == 0:
                continue
            r = pygame.Rect(j * TILE, i * TILE, TILE, TILE)
            pygame.draw.rect(screen, (70, 130, 180), r, border_radius=8)
            txt = font.render(str(v), True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=r.center))
    pygame.display.flip()
    
while True:
    for e in pygame.event.get():
        if board.is_solved():
            print("yippie!")
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = e.pos
            i, j = y // TILE, x // TILE
            zi, zj = board.find_zero()
            if abs(i - zi) + abs(j - zj) == 1:
                board[zi][zj], board[i][j] = board[i][j], board[zi][zj]
    draw(board)    

"""



