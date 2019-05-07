import pygame as pg
import random
import time
import math
#from GravityJump.py import Platform


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

# Set the width and height of the screen (width,height)
screen_width = 600
screen_height = 900
window = pg.display.set_mode((screen_width,screen_height))
screen = pg.Surface((600,900))

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pg.time.Clock()

image1 = pg.image.load('setting.jpeg')
image2 = pg.image.load('setting.jpeg')

x = 100
y = 100
screen.blit(image2,(10,30))
screen.blit(image1,(100,100))
window.blit(screen, (0,0))



while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True

    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    #window.fill(WHITE)



    if pg.key.get_pressed()[pg.K_UP]:
        screen.scroll(0, -4)
    if pg.key.get_pressed()[pg.K_DOWN]:
        screen.scroll(0, 4)





    # Limit frames per second
    tick = clock.tick(60)


    #Update the screen
    pg.display.flip()




# Close the window and quit.
pg.quit()
