import pygame
import sys
import os
from random import randint

# hex: #f5f9ea

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
    sys.exit()


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
                    return choice  # переходим на следующий экран

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
def choice_of_speed():
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
    def __init__(self, block_size, border, speed, x):
        super().__init__(all_sprites)
        self.block_size = block_size
        self.border = border  # есть ли граница
        self.speed = speed  # скорость (кадр/сек)
        self.length = 3  # длина (кол-во блоков)
        self.direction = 'RIGHT'  # направление
        self.block_size = 20  # размер 1 блока (в px)
        self.score = 0  # очки
        self.body = [(20, 20), (20, 40), (20, 60)]  # список с координатами
        self.image = load_image('snake_texture.png')
        self.rect = self.image.get_rect()
        self.rect.x = x  # координата 1 кубика по х
        self.rect.y = 100

    def update(self, direction, x, y):
        print(self.rect.x, self.rect.y)
        if self.border == 'limited field' and not 19 < self.rect.x < 761 or not 19 < self.rect.y < 561:
            return False
        elif direction == 'LEFT':
            self.rect.x -= 20
        elif direction == 'RIGHT':
            self.rect.x += 20
        elif direction == 'DOWN':
            self.rect.y += 20
        elif direction == 'UP':
            self.rect.y -= 20
        return True


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)  # путь к файлу
    # если файл не существует, то выходим:
    if not os.path.isfile(fullname):
        terminate()
    image = pygame.image.load(fullname)
    return image


def game():
    choice = start_screen()
    fps = int(choice_of_speed())
    w, n = 800, 40
    cell_size = w // n
    snake_color = pygame.Color('#a3d247')  # более тёмный цвет
    border_color = pygame.Color('#7193bf')  # граница
    font = pygame.font.Font(None, 20)
    direction = 'RIGHT'  # направление
    all_sprites.add(Snake(20, choice, fps, 100), Snake(20, choice, fps, 80), Snake(20, choice, fps, 60))
    while True:
        clock.tick(fps)
        screen.fill('#abd850')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                # игрок выбирает режим:
                if event.key == pygame.K_UP:
                    direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'
        # отрисовка игрового поля:
        for i in range(0, n):
            for j in range(0, n):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, snake_color, ((i * cell_size, j * cell_size), (cell_size, cell_size)))
        # если игрок выбрал ограниченное поле, то рисуем границу:
        if choice == 'limited field':
            pygame.draw.rect(screen, border_color, (
                (cell_size // 2, cell_size // 2), (W - cell_size, H - cell_size)), cell_size // 2)

        if all_sprites.update(direction, 1, 1):
            string_rendered = pygame.font.Font(None, 50).render(f"You've lost! Press ESC to exit. Your score: 00", True, pygame.Color('red'))
            screen.blit(string_rendered, [30, 250])
        else:
            string_rendered = font.render("score: 00", True,
                                          pygame.Color('white'))
            screen.blit(string_rendered, [5, 5])
        all_sprites.draw(screen)

        # отрисовываем очки:


        pygame.display.flip()


print('начало игры')
game()
