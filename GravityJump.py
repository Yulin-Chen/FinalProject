import pygame as pg
import random
import time
import math


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
screen = pg.display.set_mode((screen_width,screen_height))

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pg.time.Clock()

#Keeps track of the platforms
plat_list = []


class Platform:
    """Builds platform

    """
    def __init__(self):
        self.width = 200
        self.height = 10
        self.plat = pg.Surface((self.width, self.height))
        self.plat.fill(LUSHGREEN)
        self.initialized = False

    def draw_platform(self, x, y):
        self.x = x
        self.y = y
        screen.blit(self.plat,(self.x  - (self.width/2), self.y - (self.height/2)))
        if self.initialized == False:
            plat_list.append(pg.Rect(self.x  - (self.width/2), self.y - (self.height/2), self.width, self.height))
            self.initialized = True

    #def generate(self):



class Character:
    """Builds character

    """
    def __init__(self):
        self.x = 350
        self.y = 580
        self.size = 40
        self.g = 9.81
        self.v = -60
        self.delta_y = 0
        self.falling = False



    def draw_sqr(self):
        self.bottom_collider = pg.Rect(self.x-(self.size/2), self.y + (self.size/2), self.size, 5)
        if self.collision_detection() and self.delta_y > 0:
            self.y = (plat_list[self.index].top) - (self.size/2)
            self.v = -60
        self.surf = pg.Surface((self.size,self.size))
        self.surf.fill(RED)
        screen.blit(self.surf,(self.x - 20, self.y - 20))


    def jump(self):
        time = tick/90
        self.delta_y = self.v * time + 0.5 * self.g * math.pow(time, 2)
        self.v = self.v + time * self.g
        self.y += self.delta_y


    def collision_detection(self):
        if self.y > screen_height:
            self.y = 0
        if self.x > screen_width:
            self.x = 0
        if self.x < 0:
            self.x = screen_width
        #Checks if characters collider is in collision with a platform
        if self.bottom_collider.collidelist(plat_list) != -1:
            self.index = self.bottom_collider.collidelist(plat_list)
            return True
        else:
            return False

    def move(self):
        self.jump()
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.x += -4
        if pg.key.get_pressed()[pg.K_RIGHT]:
            self.x += 4

    def update_state(self):
        self.bottom_collider = pg.Rect(self.x-20, self.y + 18, 40, 5)

    def create_character(self):
        self.draw_sqr()
        self.move()
        #self.update_state()



first_plat = Platform()
plat2= Platform()
plat3 = Platform()
plat4= Platform()
plat5 = Platform()
red = Character()
# -------- Main Program Loop -----------
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True

    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    # Limit frames per second
    tick = clock.tick(60)


    first_plat.draw_platform(350, 650)
    plat2.draw_platform(450, 500)
    plat3.draw_platform(50,100)
    plat4.draw_platform(50,400)
    plat5.draw_platform(200, 300)
    red.create_character()

    #Update the screen
    pg.display.flip()





# Close the window and quit.
pg.quit()
