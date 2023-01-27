import pygame

pygame.init()

clock = pygame.time.Clock()

SIZE = W, H = 800, 600
screen = pygame.display.set_mode(SIZE)

# шрифты:
FONT_DEFAULT = pygame.font.Font(None, 30)
FONT_LEVELS = pygame.font.SysFont("comicsansms", 40)  # выбор режимов
FONT_DEFEAT = pygame.font.SysFont('times new roman', 50)  # проигрыш

# цвета:
COLOR_TEXT = pygame.Color('#FFFFFF')
COLOR_BACKGROUND = pygame.Color('#000000')
COLOR_SELECTED_TEXT = pygame.Color('green')
COLOR_UNSELECTED_TEXT = pygame.Color('gray')
COLOR_BORDER = pygame.Color('#7193bf')  # граница
COLOR_FIRST_CELL = pygame.Color('#abd850')  # цвет первой клеточки
COLOR_SECOND_CELL = pygame.Color('#a3d247')  # второй клеточки (более тёмный)
COLOR_DEFEAT = pygame.Color('red')

# игровое поле:
N = 40  # количество клеточек
CELL_SIZE = W // N  # размер клеточки
