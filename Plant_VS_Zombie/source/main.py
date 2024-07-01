import pygame as py
import sys
from pygame.locals import *

py.init()
py.mixer.init()

import image
from const import *
from game import *
import objectBase
import zombieBase
import peaBullet
import sunshine
import plantBase

Win=py.display.set_mode(GAME_SIZE)
game1 = Game(Win)
while True:
    for event in py.event.get():
        if event.type == QUIT:
            py.quit()
            sys.exit()
        elif event.type == py.MOUSEBUTTONDOWN:
            game1.mouseClickHandler(event.button)
    game1.draw()
    game1.update()


    py.display.update()