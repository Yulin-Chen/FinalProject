import pygame as pg
import random
import time
import math

"""Here's the idea:
Build a long rectangular 3d map to travel down during the game. The rectangle is screen sized on one end and n pixels long.
Each (screen x 1 pixel) frame of the map is a unit. Each frame of the game is built by placing the closest unit on the screen.
Then the next image is shrunk and centered at the vanishing point. It is then overlayed on the first but it can only be
seen through the negative space of the first. This is repeated until the nth unit vanishes into the vanishing point.
"""


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
pg.display.set_caption("3D")

# Set the width and height of the screen (width,height)
screen = pg.display.set_mode((700,700))

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pg.time.Clock()




#class Frame:

#class Map:


class Slice:
    """Creates each slice of the map

    """
    def __init__(self):
        self.position = 0
        self.w = 700
        self.h = 700

        #Number of tiles along each axis
        self.map_h = 7
        self.map_w = 7

        #Sets size of each space on the map whether wall or path
        self.tile_size = 100

        #Name matrix values
        WALL = 0
        PATH = 1

        #Set map colors
        self.colors = {WALL : RED,
                  PATH : VELVET}

        #Define map layout
        self.map = [
            [WALL, WALL, WALL, WALL, WALL, WALL, WALL],
            [WALL, WALL, WALL, WALL, WALL, WALL, WALL],
            [WALL, WALL, WALL, WALL, WALL, WALL, WALL],
            [WALL, WALL, WALL, WALL, WALL, WALL, WALL],
            [WALL, WALL, WALL, WALL, PATH, PATH, PATH],
            [WALL, WALL, WALL, WALL, PATH, PATH, PATH],
            [WALL, WALL, WALL, WALL, PATH, PATH, WALL]
            ]

        self.slice = self.draw_slice()


    def draw_slice(self):
        #Creates a surface to draw slice on
        self.slice = pg.Surface((self.w,self.h))
        self.slice.fill(RED)
        self.slice.set_colorkey(RED)

        for row in range(self.map_h):
            for column in range(self.map_w):
                pg.draw.rect(self.slice, self.colors[self.map[row][column]], (column*self.tile_size, row*self.tile_size, self.tile_size, self.tile_size))

        return self.slice



    def shrink(self, surface, size):
    """Shrinks a surface

    surface: Surface to be shrunk
    size: size after shrink
    """
    surface = pg.transform.scale(surface, (size, size))

        #screen.blit(self.slice, (0,0))
        rect = self.slice.get_rect(center=(350,350))

        self.w -= 2
        self.h -= 2
        deeper_slice = pg.transform.scale(self.slice,(self.w,self.h))
        screen.blit(deeper_slice, rect)

        pass

"""    def rotate(self, surface, rect, angle):
        # Rotate the surface and create a new image
        new_image = pg.transform.rotate(surface, angle)
        # Get a new rectangle with the same center as the old rectangle. Both stay in the same place.
        rect = new_image.get_rect(center=rect.center)
        #Return new image and new rectangle
        return new_image, rect

        #Rotates the turret
    def turret_motion(self):
        #Get rectangle centered on the tanks position
        rect = self.surf.get_rect(center = (self.x,self.y))
        #Return rotated turret new position and corresponding rectangle
        image, rect = self.rotate(self.surf, rect, self.turret_theta)
        #Copy surface with turret to screen
        DISPLAYSURF.blit(image, rect)"""



    def run(self):
        if self.w > 20:
            self.shrink()



slice1 = Slice()

# -------- Main Program Loop -----------
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()

    slice1.run()


    #Update the screen
    pg.display.flip()

    # Used to manage how fast the screen updates
    clock = pg.time.Clock()
    # Limit frames per second
    clock.tick(60)


# Close the window and quit.
pg.quit()
