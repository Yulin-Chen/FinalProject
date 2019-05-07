import pygame as pg
import random
import time
import math
from platform import Platform
from map import Map
from character import Character
from initialize import *

#Color presets
BLACK = (0, 0, 0)
GREY = (170, 174, 181)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GINGER = (224, 72, 6)
ORANGE = (247, 160, 0)
DRIEDBLOOD = (147, 0, 0)
LUSHGREEN = (0, 158, 26)
VELVET = (71, 4, 114)
BLU = (57, 33, 239)
WHITE = (0, 0, 0)

#Initialize game
pg.init()

#Label window
pg.display.set_caption("Doodle jump")



#Create and initialize class objects
#init = Initialize()
map = Map()
map.initialize()
red = Character(RED, pg.K_LEFT, pg.K_RIGHT)
blue = Character(BLUE, pg.K_a, pg.K_d, 450)

# -------- Main Program Loop -----------
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        #Escape key alternative way to end game
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True

    # Clears old screen
    screen.fill(WHITE)


    # Limit frames per second
    #tick = clock.tick(60)

    map.run_map()
    blue.run_character()
    red.run_character()


    #Update the screen
    pg.display.flip()

# Close the window and quit.
pg.quit()
