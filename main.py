import random
import sys
import time
import pygame as pg
from pygame.locals import *

# Инициализация параметров
fps = 25
window_w, window_h = 600, 500
block = 20
cup_h, cup_w = 20, 10

side_freq, down_freq = 0.15, 0.1  # Передвижение в сторону и вниз
top_margin = 50  # Отступ сверху
side_margin = 200  # Отступ по бокам

# Загрузка цветов
colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))  # Синий, Зеленый, Красный, Желтый
lightcolors = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))  # Светло-синий, Светло-зеленый, Светло-красный, Светло-желтый

white, gray, black = (255, 255, 255), (185, 185, 185), (0, 0, 0)
brd_color, bg_color, txt_color, title_color, info_color = white, black, white, colors[3], colors[0]

fig_w, fig_h = 5, 5
empty = 'o'

# Определение фигур
figures = {
    'S': [['ooooo',
           'ooooo',
           'ooxxo',
           'oxxoo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxxo',
           'oooxo',
           'ooooo']],
    'Z': [['ooooo',
           'ooooo',
           'oxxoo',
           'ooxxo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'oxxoo',
           'oxooo',
           'ooooo']],
    'J': [['ooooo',
           'oxooo',
           'oxxxo',
           'ooooo',
           'ooooo'],
          ['ooooo',
           'ooxxo',
           'ooxoo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'oxxxo',
           'oooxo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxoo',
           'oxxoo',
           'ooooo']],
    'L': [['ooooo',
           'oooxo',
           'oxxxo',
           'ooooo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxoo',
           'ooxxo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'oxxxo',
           'oxooo',
           'ooooo'],
          ['ooooo',
           'oxxoo',
           'ooxoo',
           'ooxoo',
           'ooooo']],
    'I': [['ooxoo',
           'ooxoo',
           'ooxoo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'xxxxo',
           'ooooo',
           'ooooo']],
    'O': [['ooooo',
           'ooooo',
           'oxxoo',
           'oxxoo',
           'ooooo']],
    'T': [['ooooo',
           'ooxoo',
           'oxxxo',
           'ooooo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxxo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'oxxxo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'oxxoo',
           'ooxoo',
           'ooooo']]
}

# Инициализация уровня сложности
difficulty_level = 1  # Уровень сложности

# Загрузка звука
pg.mixer.init()
point_sound = pg.mixer.Sound('data/point.ogg')

# Загрузка логотипа
logo = pg.image.load('data/logo.png')

def txtObjects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def drawTitle():
    # Отрисовка логотипа
    logo_rect = logo.get_rect(center=(window_w // 2, top_margin // 2))
    display_surf.blit(logo, logo_rect)

def main_menu():
    global display_surf
    while True:
        display_surf.fill(bg_color)
        logo_rect = logo.get_rect(center=(window_w // 2, window_h - 400))
        display_surf.blit(logo, logo_rect)

        # Кнопки меню
        startSurf, startRect = txtObjects('Начать игру', basic_font, txt_color)
        startRect.center = (window_w // 2, window_h // 2 - 20)
        display_surf.blit(startSurf, startRect)

        settingsSurf, settingsRect = txtObjects('Настройки', basic_font, txt_color)
        settingsRect.center = (window_w // 2, window_h // 2 + 20)
        display_surf.blit(settingsSurf, settingsRect)

        feedbackSurf, feedbackRect = txtObjects('Обратная связь', basic_font, txt_color)
        feedbackRect.center = (window_w // 2, window_h // 2 + 100)
        display_surf.blit(feedbackSurf, feedbackRect)

        exitSurf, exitRect = txtObjects('Выход', basic_font, txt_color)
        exitRect.center = (window_w // 2, window_h // 2 + 60)
        display_surf.blit(exitSurf, exitRect)

        pg.display.update()

        for event in pg.event.get():
            if event.type == QUIT:
                stopGame()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    stopGame()
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()  # Получаем позицию мыши при нажатии
                if startRect.collidepoint(mouse_pos):
                    return  # Начать игру
                elif settingsRect.collidepoint(mouse_pos):
                    settings_menu()
                elif feedbackRect.collidepoint(mouse_pos):
                    feedback_menu()  # Переход в меню обратной связи
                elif exitRect.collidepoint(mouse_pos):
                    stopGame()



def settings_menu():
    global display_surf, window_w, window_h, difficulty_level  # Объявляем переменные как глобальные
    while True:
        display_surf.fill(bg_color)
        titleSurf, titleRect = txtObjects('Настройки', big_font, title_color)
        titleRect.center = (window_w // 2, top_margin)
        display_surf.blit(titleSurf, titleRect)

        # Кнопка увеличения сложности
        increase_difficulty_surf, increase_difficulty_rect = txtObjects('Увеличить сложность', basic_font, txt_color)
        increase_difficulty_rect.center = (window_w // 2, window_h // 2 - 20)
        display_surf.blit(increase_difficulty_surf, increase_difficulty_rect)

        # Кнопка уменьшения сложности
        decrease_difficulty_surf, decrease_difficulty_rect = txtObjects('Уменьшить сложность', basic_font, txt_color)
        decrease_difficulty_rect.center = (window_w // 2, window_h // 2 + 40)
        display_surf.blit(decrease_difficulty_surf, decrease_difficulty_rect)

        # Кнопка изменения размера экрана
        change_size_surf, change_size_rect = txtObjects('Изменить размер экрана', basic_font, txt_color)
        change_size_rect.center = (window_w // 2, window_h // 2 + 80)
        display_surf.blit(change_size_surf, change_size_rect)

        # Отображение текущего уровня сложности
        difficulty_text = f'Текущая сложность: {difficulty_level}'
        difficulty_surf, difficulty_rect = txtObjects(difficulty_text, basic_font, txt_color)
        difficulty_rect.center = (window_w // 2, window_h // 2 + 120)
        display_surf.blit(difficulty_surf, difficulty_rect)

        # Кнопка "Назад"
        backSurf, backRect = txtObjects('Назад', basic_font, txt_color)
        backRect.center = (window_w // 2, window_h - 100)
        display_surf.blit(backSurf, backRect)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    main_menu()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if increase_difficulty_rect.collidepoint(mouse_pos):
                    if difficulty_level < 3:  # Ограничиваем уровень сложности до 3
                        difficulty_level += 1  # Увеличиваем уровень сложности
                elif decrease_difficulty_rect.collidepoint(mouse_pos):
                    if difficulty_level > 1:  # Ограничиваем уровень сложности до 1
                        difficulty_level -= 1  # Уменьшаем уровень сложности
                elif change_size_rect.collidepoint(mouse_pos):
                    change_window_size()  # Вызов функции для изменения размера окна
                elif backRect.collidepoint(mouse_pos):  # Возвращаемся в главное меню
                    return


def change_window_size():
    global display_surf, window_w, window_h, cup_w, cup_h, block
    # Изменение размера окна
    if (window_w, window_h) == (600, 500):
        window_w, window_h = 800, 600
    else:
        window_w, window_h = 600, 500

    # Пересчет размеров игрового поля
    cup_w = (window_w - 2 * side_margin) // block
    cup_h = (window_h - top_margin - 50) // block  # Учитываем отступ сверху и место для информации
    display_surf = pg.display.set_mode((window_w, window_h))  # Обновляем размер окна


def stopGame():
    pg.quit()
    sys.exit()


def pauseScreen():
    pause = pg.Surface((window_w, window_h), pg.SRCALPHA)
    pause.fill((0, 0, 255, 127))
    display_surf.blit(pause, (0, 0))


def runTetris():
    cup = emptycup()
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    going_down = False
    going_left = False
    going_right = False
    points = 0
    level, fall_speed = calcSpeed(points)
    fallingFig = getNewFig()
    nextFig = getNewFig()

    while True:
        if fallingFig is None:
            # если нет падающих фигур, генерируем новую
            fallingFig = nextFig
            nextFig = getNewFig()
            last_fall = time.time()

            if not checkPos(cup, fallingFig):
                return  # если на игровом поле нет свободного места - игра закончена
        quitGame()
        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pauseScreen()
                    showText('Пауза')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False

            elif event.type == KEYDOWN:
                # перемещение фигуры вправо и влево
                if event.key == K_LEFT and checkPos(cup, fallingFig, adjX=-1):
                    fallingFig['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and checkPos(cup, fallingFig, adjX=1):
                    fallingFig['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()

                # поворачиваем фигуру, если есть место
                elif event.key == K_UP:
                    fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(figures[fallingFig['shape']])
                    if not checkPos(cup, fallingFig):
                        fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(figures[fallingFig['shape']])

                # ускоряем падение фигуры
                elif event.key == K_DOWN:
                    going_down = True
                    if checkPos(cup, fallingFig, adjY=1):
                        fallingFig['y'] += 1
                    last_move_down = time.time()

                # мгновенный сброс вниз
                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, cup_h):
                        if not checkPos(cup, fallingFig, adjY=i):
                            break
                    fallingFig['y'] += i - 1

        # управление падением фигуры при удержании клавиш
        if (going_left or going_right) and time.time() - last_side_move > side_freq:
            if going_left and checkPos(cup, fallingFig, adjX=-1):
                fallingFig['x'] -= 1
            elif going_right and checkPos(cup, fallingFig, adjX=1):
                fallingFig['x'] += 1
            last_side_move = time.time()

        if going_down and time.time() - last_move_down > down_freq and checkPos(cup, fallingFig, adjY=1):
            fallingFig['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed:  # свободное падение фигуры
            if not checkPos(cup, fallingFig, adjY=1):  # проверка "приземления" фигуры
                addToCup(cup, fallingFig)  # фигура приземлилась, добавляем ее в содержимое стакана
                points += clearCompleted(cup)
                level, fall_speed = calcSpeed(points)
                fallingFig = None
            else:  # фигура пока не приземлилась, продолжаем движение вниз
                fallingFig['y'] += 1
                last_fall = time.time()

        # рисуем окно игры со всеми надписями
        display_surf.fill(bg_color)
        drawTitle()
        gamecup(cup)
        drawInfo(points, level)
        drawnextFig(nextFig)
        if fallingFig is not None:
            drawFig(fallingFig)
        pg.display.update()
        fps_clock.tick(fps)


def quitGame():
    for event in pg.event.get(QUIT):  # проверка всех событий, приводящих к выходу из игры
        stopGame()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            main_menu()
        pg.event.post(event)


def calcSpeed(points):
    # вычисляет уровень и скорость падения
    level = int(points / 10) + 1 + difficulty_level - 1  # Учитываем уровень сложности
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed


def getNewFig():
    # возвращает новую фигуру со случайным цветом и углом поворота
    shape = random.choice(list(figures.keys()))
    newFigure = {'shape': shape,
                 'rotation': random.randint(0, len(figures[shape]) - 1),
                 'x': int(cup_w / 2) - int(fig_w / 2),
                 'y': -2,
                 'color': random.randint(0, len(colors) - 1)}
    return newFigure


def addToCup(cup, fig):
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                cup[x + fig['x']][y + fig['y']] = fig['color']


def emptycup():
    # создает пустой стакан
    cup = []
    for i in range(cup_w):
        cup.append([empty] * cup_h)
    return cup


def incup(x, y):
    return x >= 0 and x < cup_w and y < cup_h


def checkPos(cup, fig, adjX=0, adjY=0):
    # проверяет, находится ли фигура в границах стакана, не сталкиваясь с другими фигурами
    for x in range(fig_w):
        for y in range(fig_h):
            abovecup = y + fig['y'] + adjY < 0
            if abovecup or figures[fig['shape']][fig['rotation']][y][x] == empty:
                continue
            if not incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                return False
            if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty:
                return False
    return True


def isCompleted(cup, y):
    # проверяем наличие полностью заполненных рядов
    for x in range(cup_w):
        if cup[x][y] == empty:
            return False
    return True


def clearCompleted(cup):
    # Удаление заполенных рядов и сдвиг верхних рядов вниз
    removed_lines = 0
    y = cup_h - 1
    while y >= 0:
        if isCompleted(cup, y):
            point_sound.play()  # Воспроизведение звука при удалении ряда
            for pushDownY in range(y, 0, -1):
                for x in range(cup_w):
                    cup[x][pushDownY] = cup[x][pushDownY - 1]
            for x in range(cup_w):
                cup[x][0] = empty
            removed_lines += 1
        else:
            y -= 1
    return removed_lines


def convertCoords(block_x, block_y):
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))


def drawBlock(block_x, block_y, color, pixelx=None, pixely=None):
    # отрисовка квадратных блоков, из которых состоят фигуры
    if color == empty:
        return
    if pixelx is None and pixely is None:
        pixelx, pixely = convertCoords(block_x, block_y)
    pg.draw.rect(display_surf, colors[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
    pg.draw.rect(display_surf, lightcolors[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
    pg.draw.circle(display_surf, colors[color], (pixelx + block / 2, pixely + block / 2), 5)


def gamecup(cup):
    # граница игрового поля-стакана
    pg.draw.rect(display_surf, brd_color, (side_margin - 4, top_margin - 4, (cup_w * block) + 8, (cup_h * block) + 8),
                 5)

    # фон игрового поля
    pg.draw.rect(display_surf, bg_color, (side_margin, top_margin, block * cup_w, block * cup_h))
    for x in range(cup_w):
        for y in range(cup_h):
            drawBlock(x, y, cup[x][y])


def drawTitle():
    # Отрисовка логотипа
    logo_rect = logo.get_rect(center=(window_w // 2, top_margin // 2))
    display_surf.blit(logo, logo_rect)


def drawInfo(points, level):
    pointsSurf = basic_font.render(f'Баллы: {points}', True, txt_color)
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (window_w - 180, window_h - 120)
    display_surf.blit(pointsSurf, pointsRect)

    levelSurf = basic_font.render(f'Уровень: {level}', True, txt_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (window_w - 180, window_h - 100)
    display_surf.blit(levelSurf, levelRect)

    pausebSurf = basic_font.render('Пауза: пробел', True, info_color)
    pausebRect = pausebSurf.get_rect()
    pausebRect.topleft = (window_w - 180, window_h - 80)
    display_surf.blit(pausebSurf, pausebRect)

    escbSurf = basic_font.render('Выход: Esc', True, info_color)
    escbRect = escbSurf.get_rect()
    escbRect.topleft = (window_w - 180, window_h - 60)
    display_surf.blit(escbSurf, escbRect)


def drawFig(fig, pixelx=None, pixely=None):
    figToDraw = figures[fig['shape']][fig['rotation']]
    if pixelx is None and pixely is None:
        pixelx, pixely = convertCoords(fig['x'], fig['y'])

    # отрисовка элементов фигур
    for x in range(fig_w):
        for y in range(fig_h):
            if figToDraw[y][x] != empty:
                drawBlock(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))


def drawnextFig(fig):  # превью следующей фигуры
    nextSurf = basic_font.render('Следующая:', True, txt_color)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (window_w - 150, top_margin + 20)
    display_surf.blit(nextSurf, nextRect)
    drawFig(fig, pixelx=window_w - 150, pixely=top_margin + 50)


def showText(text):
    titleSurf, titleRect = txtObjects(text, big_font, title_color)
    titleRect.center = (int(window_w / 2), int(window_h / 2))
    display_surf.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = txtObjects('Нажмите любую клавишу для продолжения', basic_font, title_color)
    pressKeyRect.center = (int(window_w / 2), int(window_h / 2) + 50)
    display_surf.blit(pressKeySurf, pressKeyRect)

    while checkKeys() is None:
        pg.display.update()
        fps_clock.tick()


def checkKeys():
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            return True
    return None


def main():
    global fps_clock, display_surf, basic_font, big_font
    pg.init()
    fps_clock = pg.time.Clock()
    display_surf = pg.display.set_mode((window_w, window_h))
    basic_font = pg.font.SysFont('arial', 20)
    big_font = pg.font.SysFont('verdana', 45)
    pg.display.set_caption('Тетрис')
    main_menu()  # Переход в главное меню
    while True:  # начинаем игру
        runTetris()
        pauseScreen()
        showText('GAME OVER')


def feedback_menu():
    while True:
        display_surf.fill(bg_color)
        titleSurf, titleRect = txtObjects('Обратная связь', big_font, title_color)
        titleRect.center = (window_w // 2, top_margin)
        display_surf.blit(titleSurf, titleRect)

        # Отображение логотипов и ссылок
        vk_logo = pg.image.load('data/vk.png')  # Замените на путь к вашему изображению
        tg_logo = pg.image.load('data/tg.png')  # Замените на путь к вашему изображению
        github_logo = pg.image.load('data/github.png')  # Замените на путь к вашему изображению

        # Позиции для логотипов
        vk_rect = vk_logo.get_rect(center=(window_w // 2, top_margin + 100))
        tg_rect = tg_logo.get_rect(center=(window_w // 2, top_margin + 160))
        github_rect = github_logo.get_rect(center=(window_w // 2, top_margin + 220))

        display_surf.blit(vk_logo, vk_rect)
        display_surf.blit(tg_logo, tg_rect)
        display_surf.blit(github_logo, github_rect)

        # Добавьте текстовые ссылки под логотипами
        vk_text = txtObjects('vk.com/matveytokarev', basic_font, txt_color)
        tg_text = txtObjects('t.me/yaemogirl228', basic_font, txt_color)
        github_text = txtObjects('github.com/KayOrNoffil', basic_font, txt_color)

        display_surf.blit(vk_text[0], (vk_rect.centerx - vk_text[0].get_width() // 2, vk_rect.bottom + 5))
        display_surf.blit(tg_text[0], (tg_rect.centerx - tg_text[0].get_width() // 2, tg_rect.bottom + 5))
        display_surf.blit(github_text[0], (github_rect.centerx - github_text[0].get_width() // 2, github_rect.bottom + 5))

        # Кнопка "Назад"
        backSurf, backRect = txtObjects('Назад', basic_font, txt_color)
        backRect.center = (window_w // 2, window_h - 100)
        display_surf.blit(backSurf, backRect)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                stopGame()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return  # Возвращаемся в главное меню
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if backRect.collidepoint(mouse_pos):
                    return  # Возвращаемся в главное меню



if __name__ == '__main__':
    main()


