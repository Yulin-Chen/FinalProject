import pygame as pg
import random
import time
import math

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

# Set the width and height of the screen (width,height)
screen_width = 600
screen_height = 900
screen = pg.display.set_mode((screen_width,screen_height))

# Loop until the user closes program
done = False

# Used to manage how fast the screen updates
clock = pg.time.Clock()

#Keeps track of the platform objects
plat_obj_list = []
#Keeps track of the platforms location rectangles
plat_rect_list = []


class Platform:
    """Create a new platform

    """
    #Initialize platform attributes
    def __init__(self):
        self.width = 150
        self.height = 10
        #This will later be changed to a more visually appealing platform
        self.plat = pg.Surface((self.width, self.height))
        self.plat.fill(LUSHGREEN)
        self.initialized = False

    def draw_platform(self, x, y):
        """ Draw a platform and add its location rectangle to the list of platform rectangles.

        Parameters
        ----------
        x: int
            X coordinate of center of new platform
        y: int
            Y coordinate of center of new platform
        """

        self.x = x
        self.y = y
        # Blits surface to screen
        screen.blit(self.plat,(self.x  - (self.width/2), self.y - (self.height/2)))
        if self.initialized == False:
            plat_rect_list.append(pg.Rect(self.x  - (self.width/2), self.y - (self.height/2), self.width, self.height))
            self.initialized = True


    def update_plat_location(self):
        """ Updates plat_rect_list with the current position of all the platforms """
        for rect in plat_rect_list:
            rect = pg.Rect(self.x  - (self.width/2), self.y - (self.height/2), self.width, self.height)

class Map:
    """Generate new platforms and move the map


    End goal:
    New platforms are generated semi-randomly in relation to eachother. They are added and removed
    from the platform objects list as they appear and exit the screen. Platforms and sprites move
    downward in sychronism as sprites advance through the game to give the illusion of a upward
    scrolling motion.
    """

    def __init__(self):
        #Verticle distance between platforms
        self.spacing = 30

    def initialize(self):
        """Set starting screen with platforms.

        Predetermined Y coordinates for each but random X coordinates.
        """
        for num in range(100,900,100):
            self.generate_plat(num)


    def proximity_check(self):
        """Check if there is slef.spacing distance between the top platform and the top of the screen"""
        if plat_obj_list[-1].top < self.spacing:
            return False
        else:
            return True

    def off_the_edge(self):
        """Check if a platform is off the bottom of the screen and remove it from the list if so"""
        if plat_obj_list[0].top > screen_height:
            plat_obj_list.remove(plat_obj_list[0])


    def generate_plat(self, y):
        """Create new platform object at specified Y coordinate

        Append platform object to platform object list. Draw the new platform on the screen.

        Parameter
        ----------
        y: int
            Y coordinate of center of new platform
        """

        plat = Platform()
        plat_obj_list.append(plat)
        plat.draw_platform(random.randint(0,screen_width),y)

    def move_map(self):
        """ This function is just to assist in debugging and testing.
        Ultimately the map will move as a function of the highest sprite's position
        and velocity so that the sprite's never move up and off the map"""

        if pg.key.get_pressed()[pg.K_DOWN]:
            for plat in plat_obj_list:
                plat.y += 5

    def run_map(self):
        """Run it all"""
        self.move_map()
        self.generate_plat()
        self.off_the_edge()


class Character:
    """Build character

    Create and add character to screen. Set constant jump. Move with arrow keys.
    Detect collisions wih platforms and react appropriatley.

    End Goal:
    Currently the characters are represented as square surfaces. This will be changed to animated sprites.
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
        """ Draw surface to represent character. Create collision detection collider underneath
        character. Also update state is collision is detected.

        End Goal:
        This is a very messy func, it will be improved and sorted into logical functions.
        """
        #Coliider rect created under character
        self.bottom_collider = pg.Rect(self.x-(self.size/2), self.y + (self.size/2), self.size, 5)
        #If sprite collides AND is moving downwards a collision reaction is triggered
        if self.collision_detection() and self.delta_y > 0:
            #Pulls character to platform before next jump to avoid jumping on 'air' because collider extends below character
            self.y = (plat_rect_list[self.index].top) - (self.size/2)
            self.v = -60
        #Draw and blit character to screen
        self.surf = pg.Surface((self.size,self.size))
        self.surf.fill(RED)
        screen.blit(self.surf,(self.x - 20, self.y - 20))


    def jump(self):
        """Calculate change in y during jump and update y
        """
        #This sets the time step for each calculation
        time = tick/90
        self.delta_y = self.v * time + 0.5 * self.g * math.pow(time, 2)
        self.v = self.v + time * self.g
        self.y += self.delta_y


    def collision_detection(self):
        """Check character position and react according to special cases.

        If the character falls off the bottom they reappear at the top. If they go
        off a side they loop to the other side. This also detects collisions with
        platforms.

        End Goal:
        In the final program, falling off the botrtom is game over.
        """
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
        """ Move charaacter according to user input."""
        #Constant jumping
        self.jump()
        #Left,Right controls
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.x += -4
        if pg.key.get_pressed()[pg.K_RIGHT]:
            self.x += 4


    def update_state(self):
        """ Update location of collider"""
        self.bottom_collider = pg.Rect(self.x-20, self.y + 18, 40, 5)


    def create_character(self):
        """Run character actions"""
        self.draw_sqr()
        self.move()
        

#Create and initialize class objects
map = Map()
first_plat = Platform()
map.initialize()
red = Character()

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

    #Iterates through platform list and draws them all
    for plat in plat_obj_list:
        plat.draw_platform(plat.x,plat.y)

    # Limit frames per second
    tick = clock.tick(60)


    first_plat.draw_platform(350, 650)
    red.create_character()

    #Update the screen
    pg.display.flip()

# Close the window and quit.
pg.quit()
