import pygame
from os import path
from time import sleep
from random import randrange
from sys import exit as close
from datetime import datetime

pygame.init()

clock = pygame.time.Clock()
pygame.display.set_caption('Wormi')
SIZE = W, H = 800, 600
screen = pygame.display.set_mode(SIZE)
WHITE = pygame.Color('#FFFFFF')
BLACK = pygame.Color('#000000')
pygame.mouse.set_visible(False)
all_sprites = pygame.sprite.Group()  # группа всех спрайтов


def terminate():
    pygame.quit()
    close()


def start_screen():
    choice = 'limited field'  # выбор игрового режима
    name = ''
    font = pygame.font.Font(None, 30)
    choice_font = pygame.font.SysFont("comicsansms", 40)
    while True:
        screen.fill(BLACK)
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
        string_rendered = font.render(
            'Please enter your name, then select the mode', True,
            pygame.Color('white'))
        screen.blit(string_rendered, [190, 50])

        string_rendered = font.render(f'Your name: {name}', True,
                                      pygame.Color('white'))
        screen.blit(string_rendered, [190, 150])

        if choice == 'limited field':
            string_rendered = choice_font.render(
                'The field is limited by walls (classic)', True,
                pygame.Color('green'))
            screen.blit(string_rendered, [65, 250])

            string_rendered = choice_font.render('The field is unlimited',
                                                 True,
                                                 pygame.Color('gray'))
            screen.blit(string_rendered, [200, 350])
        elif choice == 'unlimited field':
            string_rendered = choice_font.render(
                'The field is limited by walls (classic)', True,
                pygame.Color('gray'))
            screen.blit(string_rendered, [65, 250])

            string_rendered = choice_font.render('The field is unlimited',
                                                 True,
                                                 pygame.Color('green'))
            screen.blit(string_rendered, [200, 350])

        pygame.display.flip()
        clock.tick(15)  # невысокий фпс, чтобы не тратить лишние ресурсы пк


# игрок вводит ФПС/скорость
def choice_of_speed(name):
    fps = ''
    font = pygame.font.Font(None, 30)
    while True:
        screen.fill(BLACK)
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
                    file = open('Player rating.txt', mode='a', encoding='utf8')
                    file.write(
                        f'Player "{name}" started the game. Date: '
                        f'{datetime.now().strftime("%d %b %Y %H:%M:%S")}\n')
                    file.close()
                    return fps  # начинаем игру
        # отрисовка текста:
        string_rendered = font.render(
            "Enter the character's speed from 1 to 50 (default: 10)", True,
            pygame.Color('white'))
        screen.blit(string_rendered, [135, 70])

        string_rendered = font.render(f'Speed: {fps}', True,
                                      pygame.Color('white'))
        screen.blit(string_rendered, [335, 170])

        pygame.display.flip()
        clock.tick(15)


class Snake(pygame.sprite.Sprite):
    def __init__(self, block_size, border, x):
        super().__init__(all_sprites)
        self.block_size = block_size
        self.border = border  # есть ли граница
        self.direction = 'RIGHT'  # направление
        self.block_size = 20  # размер 1 блока (в px)
        # координаты тела (начиная с конца, но без головы):
        self.body = [[x - block_size, 100], [x, 100]]
        self.image = load_image('snake_texture.png')
        self.rect = self.image.get_rect()
        self.rect.x = x  # координата 1 кубика по х
        self.rect.y = 100
        self.prev = 0

    def update(self, direction, x, y, score, name):
        if self.border == 'limited field' and (not 19 < self.rect.x < 761 or
                                               not 19 < self.rect.y < 561):
            game_over(score, name, self.border)
            return
        elif direction == 'LEFT':
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
            elif self.rect.x > W:
                self.rect.x = 0
            if self.rect.y < 0:
                self.rect.y = H
            elif self.rect.y > H:
                self.rect.y = 0
        self.body.append([self.rect.x, self.rect.y])
        # если очки увеличатся, то хвостик удлинится:
        if self.prev >= score:
            self.body = self.body[1:]
        # проверка на столкновение с самим собой
        if self.body.count([self.rect.x, self.rect.y]) > 1:
            game_over(score, name, self.border)
            return
        self.prev = score


def load_image(name):
    fullname = path.join('data', name)  # путь к файлу
    # если файл не существует, то выходим:
    if not path.isfile(fullname):
        terminate()
    image = pygame.image.load(fullname)
    return image


def game():
    choice, name = start_screen()
    fps = int(choice_of_speed(name))
    w, n = 800, 40
    cell_size = w // n
    snake_color = pygame.Color('#a3d247')  # более тёмный цвет
    border_color = pygame.Color('#7193bf')  # граница
    image_snake = load_image('snake_texture.png')
    image_fruit = load_image('fruit.png')
    font = pygame.font.SysFont("comicsansms", 20)
    direction = 'RIGHT'  # направление
    # случайные координаты фрукта:
    fruit_pos = [randrange(1, ((W - cell_size) // cell_size)) * cell_size,
                 randrange(1, ((H - cell_size) // cell_size)) * cell_size]
    score = 0  # очки
    snake = Snake(20, choice, 100)
    while True:
        clock.tick(fps)
        snake_body = snake.body
        screen.fill('#abd850')
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
        for i in range(0, n):
            for j in range(0, n):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, snake_color, ((i * cell_size,
                                                            j * cell_size),
                                                           (cell_size,
                                                            cell_size)))
        # если игрок выбрал ограниченное поле, то рисуем границу:
        if choice == 'limited field':
            pygame.draw.rect(screen, border_color,
                             ((cell_size // 2, cell_size // 2),
                              (W - cell_size, H - cell_size)), cell_size // 2)
        # змеиное туловище
        for pos in snake_body:
            screen.blit(image_snake, (pos[0], pos[1]))
            if fruit_pos == pos:
                # меняем координату и прибавляем очки
                fruit_pos = [randrange(1, ((W - cell_size) // cell_size)) *
                             cell_size, randrange(1, ((H - cell_size) //
                                                      cell_size)) * cell_size]
                score += 1

        screen.blit(image_fruit, (fruit_pos[0], fruit_pos[1]))
        all_sprites.update(direction, 1, 1, score, name)
        # отрисовка очков:
        string_rendered = font.render(f"score: {score}", True,
                                      pygame.Color('white'))
        screen.blit(string_rendered, [710, 570])

        all_sprites.draw(screen)
        pygame.display.flip()


def game_over(score, name, border):
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render("You've lost! Your score: " + str(score),
                                    True, 'red')
    rect = game_over_surface.get_rect()
    rect.midtop = (W // 2, H // 4)
    screen.blit(game_over_surface, rect)
    pygame.display.flip()
    # сохранение результатов в файл:
    file = open('Player rating.txt', mode='a', encoding='utf8')
    if border == 'limited field':
        file.write(f'Player "{name}" finished the game on a limited field '
                   f'with a score: {score}. Date: '
                   f'{datetime.now().strftime("%d %b %Y %H:%M:%S")}\n')
    elif border == 'unlimited field':
        file.write(f'Player "{name}" finished the game on an unlimited field '
                   f'with a score: {score}. Date: '
                   f'{datetime.now().strftime("%d %b %Y %H:%M:%S")}\n')
    file.close()
    sleep(3)
    terminate()


print('начало игры')
game()
