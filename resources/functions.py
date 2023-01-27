from os import path
from time import sleep
from random import randrange
from sys import exit as close
from datetime import datetime
from resources.constants import *


def terminate():
    pygame.quit()
    close()


def load_image(name):
    fullname = path.join('data', name)  # путь к файлу
    print(fullname)
    # если файл не существует, то выходим:
    if not path.isfile(fullname):
        print('Отсутствуют необходимые файлы изображений! Программа завершена')
        terminate()
    image = pygame.image.load(fullname)
    return image


IMAGE_SNAKE, IMAGE_FRUIT = load_image('snake_texture.png'), \
                           load_image('fruit.png')
all_sprites = pygame.sprite.Group()  # группа всех спрайтов


class Snake(pygame.sprite.Sprite):
    def __init__(self, block_size, border, x):
        super().__init__(all_sprites)
        self.border = border  # есть ли граница
        self.direction = 'RIGHT'  # направление
        # координаты тела (начиная с конца, но без головы):
        self.body = [[x - block_size, 100], [x, 100]]
        self.image = IMAGE_SNAKE
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, 100  # координата 1 кубика по X
        self.previous = 0

    def update(self, direction, x, y, score, name):
        if self.border == 'limited field' and (not 19 < self.rect.x < 761 or
                                               not 19 < self.rect.y < 561):
            game_over(score, self.border)
            return
        if direction == 'LEFT':
            self.rect.x -= 20
        elif direction == 'RIGHT':
            self.rect.x += 20
        elif direction == 'DOWN':
            self.rect.y += 20
        elif direction == 'UP':
            self.rect.y -= 20
        if self.border == 'unlimited field':
            if self.rect.x < 0:
                self.rect.x = W
            elif self.rect.x >= W:
                self.rect.x = 0
            if self.rect.y < 0:
                self.rect.y = H
            elif self.rect.y >= H:
                self.rect.y = 0
        self.body.append([self.rect.x, self.rect.y])
        # если очки увеличатся, то хвостик удлинится:
        if self.previous >= score:
            self.body = self.body[1:]
        # проверка на столкновение с самим собой
        if self.body.count([self.rect.x, self.rect.y]) > 1:
            game_over(score, self.border)
            return
        self.previous = score


# сохранение всех результатов в файл:
def log(mode, name=None, fps=None, score=None, border=None):
    file = open('Players rating.txt', mode='a', encoding='utf8')
    if mode == 'log in':
        file.write(
            f'Player "{name}" started the game. Speed: {fps}. '
            f'Date: '
            f'{datetime.now().strftime("%d %b %Y %H:%M:%S")}\n')
    elif mode == 'game over':
        if border == 'limited field':
            file.write(f'The game is over on a limited field '
                       f'with score: {score}. Date: '
                       f'{datetime.now().strftime("%d %b %Y %H:%M:%S")}\n')
        elif border == 'unlimited field':
            file.write(
                f'The game is over on an unlimited field '
                f'with score: {score}. Date: '
                f'{datetime.now().strftime("%d %b %Y %H:%M:%S")}\n')
    file.close()


# стартовый экран
def start_screen():
    choice, name = 'limited field', ''  # выбор игрового режима; имя
    while True:
        screen.fill(COLOR_BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                # игрок выбирает режим:
                if event.key == pygame.K_UP:
                    choice = 'limited field'
                elif event.key == pygame.K_DOWN:
                    choice = 'unlimited field'
                # игрок вводит имя любимое моё:
                if len(name) <= 30:
                    name += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-2]
                # выход со стартового окна при нажатии Enter
                name = name.strip()
                if event.key == pygame.K_RETURN and name != '':
                    return choice, name  # переходим на следующий экран

        # отрисовка текста:
        string_rendered = FONT_DEFAULT.render(
            'Please enter your name, then select the mode', True, COLOR_TEXT)
        screen.blit(string_rendered, [190, 50])

        string_rendered = FONT_DEFAULT.render(f'Your name: {name}', True,
                                              COLOR_TEXT)
        screen.blit(string_rendered, [190, 150])

        if choice == 'limited field':
            string_rendered = FONT_LEVELS.render(
                'The field is limited by walls (classic)', True,
                pygame.Color(COLOR_SELECTED_TEXT))
            screen.blit(string_rendered, [65, 250])

            string_rendered = FONT_LEVELS.render('The field is unlimited',
                                                 True, COLOR_UNSELECTED_TEXT)
            screen.blit(string_rendered, [200, 350])
        elif choice == 'unlimited field':
            string_rendered = FONT_LEVELS.render(
                'The field is limited by walls (classic)', True,
                COLOR_UNSELECTED_TEXT)
            screen.blit(string_rendered, [65, 250])

            string_rendered = FONT_LEVELS.render('The field is unlimited',
                                                 True, COLOR_SELECTED_TEXT)
            screen.blit(string_rendered, [200, 350])

        pygame.display.flip()
        clock.tick(15)  # невысокий фпс, чтобы не тратить лишние ресурсы пк


# игрок вводит ФПС/скорость
def choice_of_speed(name):
    fps = ''
    while True:
        screen.fill(COLOR_BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if len(str(fps)) < 3 and event.unicode.isdigit():
                    fps += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    fps = fps[:-1]
                # выход с окна при нажатии Enter
                if event.key == pygame.K_RETURN and fps != '' and \
                        0 < int(fps) <= 50:
                    log('log in', name=name, fps=fps)
                    return fps  # начинаем игру
        # отрисовка текста:
        string_rendered = FONT_DEFAULT.render(
            "Enter the character's speed from 1 to 50 (default: 10)", True,
            COLOR_TEXT)
        screen.blit(string_rendered, [135, 70])
        string_rendered = FONT_DEFAULT.render(f'Speed: {fps}', True,
                                              COLOR_TEXT)
        screen.blit(string_rendered, [335, 170])

        pygame.display.flip()
        clock.tick(15)


# игра
def game():
    choice, name = start_screen()
    score, fps = 0, int(choice_of_speed(name))
    direction = 'RIGHT'  # направление по умолчанию
    # случайные координаты фрукта:
    fruit_pos = [randrange(1, ((W - CELL_SIZE) // CELL_SIZE)) * CELL_SIZE,
                 randrange(1, ((H - CELL_SIZE) // CELL_SIZE)) * CELL_SIZE]
    snake = Snake(20, choice, 100)
    while True:
        clock.tick(fps)
        snake_body = snake.body
        screen.fill(COLOR_FIRST_CELL)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                # игрок выбирает режим:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
        # отрисовка игрового поля:
        for i in range(0, N):
            for j in range(0, N):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, COLOR_SECOND_CELL, ((i *
                                                                  CELL_SIZE, j
                                                                  * CELL_SIZE),
                                                                 (CELL_SIZE,
                                                                  CELL_SIZE)))
        # если игрок выбрал ограниченное поле, то рисуем границу:
        if choice == 'limited field':
            pygame.draw.rect(screen, COLOR_BORDER,
                             ((CELL_SIZE // 2, CELL_SIZE // 2),
                              (W - CELL_SIZE, H - CELL_SIZE)), CELL_SIZE // 2)
        # змеиное туловище
        for pos in snake_body:
            screen.blit(IMAGE_SNAKE, (pos[0], pos[1]))
            if fruit_pos == pos:
                # меняем координату и прибавляем очки
                fruit_pos = [randrange(1, ((W - CELL_SIZE) // CELL_SIZE)) *
                             CELL_SIZE, randrange(1, ((H - CELL_SIZE) //
                                                      CELL_SIZE)) * CELL_SIZE]
                score += 1

        screen.blit(IMAGE_FRUIT, (fruit_pos[0], fruit_pos[1]))
        all_sprites.update(direction, 1, 1, score, name)
        # отрисовка очков:
        string_rendered = FONT_DEFAULT.render(f"score: {score}", True,
                                              COLOR_TEXT)
        screen.blit(string_rendered, [710, 570])

        all_sprites.draw(screen)
        pygame.display.flip()


# поражение
def game_over(score, border):
    game_over_surface = FONT_DEFEAT.render(
        "You've lost! Your score: " + str(score), True, COLOR_DEFEAT)
    rect = game_over_surface.get_rect()
    rect.midtop = (W // 2, H // 4)
    screen.blit(game_over_surface, rect)
    pygame.display.flip()
    log('game over', score=score, border=border)
    sleep(3)
    terminate()
