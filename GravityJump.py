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
plat_rect_list = []
plat_obj_list = []


class Platform:
    """Builds platform

    """
    def __init__(self):
        self.width = 150
        self.height = 10
        self.plat = pg.Surface((self.width, self.height))
        self.plat.fill(LUSHGREEN)
        self.initialized = False

    def draw_platform(self, x, y):
        self.x = x
        self.y = y
        screen.blit(self.plat,(self.x  - (self.width/2), self.y - (self.height/2)))
        if self.initialized == False:
            plat_rect_list.append(pg.Rect(self.x  - (self.width/2), self.y - (self.height/2), self.width, self.height))
            self.initialized = True
        for rect in plat_rect_list:
            rect = pg.Rect(self.x  - (self.width/2), self.y - (self.height/2), self.width, self.height)

class Map:
    """Generates Map

    """
    def __init__(self):
        self.spacing = 30
        self.counter = 0

    def initialize(self):
        for num in range(100,900,100):
            self.generate_plat(num)


    def proximity_check(self):
        if plat_obj_list[-1].top < self.spacing:
            return False
        else:
            return True

    def off_the_edge(self):
        if plat_obj_list[0].top > screen_height:
            plat_obj_list.remove(plat_obj_list[0])


    def generate_plat(self, y):
            plat = Platform()
            plat_obj_list.append(plat)
            plat.draw_platform(random.randint(0,screen_width),y)

    def move_map(self):
        if pg.key.get_pressed()[pg.K_DOWN]:
            for plat in plat_obj_list:
                plat.y += 5

    def run_map(self):
        self.move_map()
        self.generate_plat()
        self.off_the_edge()


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
            self.y = (plat_rect_list[self.index].top) - (self.size/2)
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

        if self.bottom_collider.collidelist(plat_rect_list) != -1:
            self.index = self.bottom_collider.collidelist(plat_rect_list)
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


map = Map()
first_plat = Platform()
map.initialize()
red = Character()
print(plat_rect_list)
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
    for plat in plat_obj_list:
        plat.draw_platform(plat.x,plat.y)
    # Limit frames per second
    tick = clock.tick(60)

    map.run_map()
    #map.initialize()
    first_plat.draw_platform(350, 650)
    red.create_character()

    #Update the screen
    pg.display.flip()





# Close the window and quit.
pg.quit()
