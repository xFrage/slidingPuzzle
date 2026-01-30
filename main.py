import pygame, random, sys

N = 4
SIZE = 400
TILE = SIZE // N
FONT_SIZE = 48

pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))
font = pygame.font.SysFont(None, FONT_SIZE)


def solved_board():
    return [[(i * N + j + 1) % (N * N) for j in range(N)] for i in range(N)]


def find_zero(b):
    for i in range(N):
        for j in range(N):
            if b[i][j] == 0:
                return i, j


def moves(b):
    i, j = find_zero(b)
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < N and 0 <= nj < N:
            yield ni, nj


def shuffle(b, steps=200):
    for _ in range(steps):
        ni, nj = random.choice(list(moves(b)))
        i, j = find_zero(b)
        b[i][j], b[ni][nj] = b[ni][nj], b[i][j]


def draw(b):
    screen.fill((30, 30, 30))
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


board = solved_board()
shuffle(board)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit();
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = e.pos
            i, j = y // TILE, x // TILE
            zi, zj = find_zero(board)
            if abs(i - zi) + abs(j - zj) == 1:
                board[zi][zj], board[i][j] = board[i][j], board[zi][zj]
    draw(board)
