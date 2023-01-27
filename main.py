from sys import exit
from resources.functions import *


try:
    pygame.init()
except Exception as err:
    print('PyGame Error. Code:', err)
    exit()

pygame.mouse.set_visible(False)
pygame.display.set_caption('SnakeI')


game()
