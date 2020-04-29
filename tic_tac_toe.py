import pygame as pg,sys
from pygame.locals import *
import time

XO = 'x'
winner = None
draw = False
width = 400
height = 400
background_color = (239, 228, 176)
line_color = (10, 60, 73)
check_line_color = (0, 250, 0)

# доска 9х9
TTT = [[None]*3, [None]*3, [None]*3]

# окно игры
pg.init()
fps = 30
clock = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe")

# загрузка изображений
start_img = pg.image.load('Tic Tac Toe.png')
x_img = pg.image.load('X.png')
o_img = pg.image.load('O.png')

# меняем размер изображения
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
start_img = pg.transform.scale(start_img, (width, height+100))

def game_opening():
    # заставка, пауза, заливка фона
    screen.blit(start_img, (0, 0))
    pg.display.update()
    time.sleep(1.5)
    screen.fill(background_color)
    # прорисовка вертикальных линий поля
    pg.draw.line(screen, line_color, (width/3, 0), (width/3, height), 7)
    pg.draw.line(screen, line_color, (width/3*2, 0), (width/3*2, height), 7)
    # прорисовка горизонтальных линий поля
    pg.draw.line(screen, line_color, (0, height/3), (width, height/3), 7)
    pg.draw.line(screen, line_color, (0, height/3*2), (width, height/3*2), 7)
    draw_status()


def draw_status():
    global draw

    # задать текст сообщения
    if winner is None:
        message = XO.upper() + "'s turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = 'Game Draw!'
    # задать шрифт
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))
    # копируем сообщение на доску
    screen.fill((10, 60, 73), (0, 400, 400, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()

def check_win():
    global TTT, winner, draw

    # проверка победителя по строке
    for row in range(0, 3):
        if (TTT[row][0] == TTT[row][1] == TTT[row][2]) and (TTT[row][0] is not None):
            # эта строка победила
            winner = TTT[row][0]
            pg.draw.line(screen, check_line_color, ((row + 1) * width / 3 - width / 6, 0),
                         ((row + 1) * width / 3 - width / 6, height), 4)
            break

    # проверка победителя по столбцу
    for col in range(0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            # этот столбец победил
            winner = TTT[0][col]
            # рисуем линию
            pg.draw.line(screen, check_line_color, (0, (col + 1) * height / 3 - height / 6),
                         (width, (col + 1) * height / 3 - height / 6), 4)
            break

    # проверка победителя по диагонали
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        # выйграла диагноаль слева направо
        winner = TTT[0][0]
        pg.draw.line(screen, check_line_color, (50, 50), (350, 350), 4)

    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        # выйграла диагноаль справа налево
        winner = TTT[0][2]
        pg.draw.line(screen, check_line_color, (350, 50), (50, 350), 4)

    if all([all(row) for row in TTT]) and winner is None:
        draw = True
    draw_status()


def drawXO(row, col):
    global TTT, XO

    if row == 1:
        posx = 30
    if row == 2:
        posx = width / 3 + 30
    if row == 3:
        posx = width / 3 * 2 + 30

    if col == 1:
        posy = 30
    if col == 2:
        posy = height / 3 + 30
    if col == 3:
        posy = height / 3 * 2 + 30

    TTT[row - 1][col - 1] = XO
    if XO == 'x':
        screen.blit(x_img, (posx, posy))
        XO = 'o'
    else:
        screen.blit(o_img, (posx, posy))
        XO = 'x'
    pg.display.update()


def userClick():
    # получаем координаты компьютерной мыши
    y, x = pg.mouse.get_pos()

    # выясняем номер колонки
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    # выясняем номер строки
    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and TTT[row - 1][col - 1] is None:
        global XO

        # рисуем х или о
        drawXO(row, col)
        check_win()

def reset_game():
    global TTT, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    game_opening()
    winner = None
    TTT = [[None]*3, [None]*3, [None]*3]


game_opening()

# зацикливаем гру
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type is MOUSEBUTTONDOWN:
            userClick()
            if winner or draw:
                reset_game()
    pg.display.update()
    clock.tick(fps)
