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
pg.display.set_caption("Kangaroo Jump")

# Set the width and height of the screen (width,height)
screen_width = 600
screen_height = 900
screen = pg.display.set_mode((screen_width,screen_height))

# Loop until the user closes program
done = False

# Used to manage how fast the screen updates
clock = pg.time.Clock()

font = pg.font.SysFont('chandas', 20, True)

class Platform:
    """Create a new platform

    """
    #Initialize platform attributes
    def __init__(self):
        self.width = 120
        self.height = 10
        #This will later be changed to a more visually appealing platform
        self.plat = pg.Surface((self.width, self.height))
        self.plat.fill(LUSHGREEN)


    def draw_platform(self, x, y):
        """ Blit a platform onto the screen and set the rectangle around it.

        Parameters
        ----------
        x: int
            X coordinate of center of new platform
        y: int
            Y coordinate of center of new platform
        """
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x  - (self.width/2), self.y - (self.height/2), self.width, self.height)
        # Blits surface to screen
        self.top = self.rect.top
        screen.blit(self.plat,(self.x  - (self.width/2), self.y - (self.height/2)))

class Character():
    """Build character

    Create and add character to screen. Set constant jump. Move with arrow keys.
    Detect collisions wih platforms and react appropriatley.

    End Goal:
    Currently the characters are represented as square surfaces. This will be changed to animated sprites.
    """

    def __init__(self,name, color, left, right, fire, x = 150, y = 825, score=0):
        self.name = name
        self.color = color
        self.left = left
        self.right = right
        self.fire = fire
        self.x = x
        self.y = y
        self.size = 40
        self.v = -60
        self.g = 9.81
        self.delta_y = 0
        self.surf = pg.Surface((self.size,self.size))
        self.surf.fill(self.color)
        self.score = score
        self.babykangas = []
        self.pouch = 2
        self.lives = 3


    def draw_character(self):
        """ Blit surface that represents character. """
        #Draw and blit character to screen
        screen.blit(self.surf,(self.x - 20, self.y - 20))

    def jump(self):
        """Calculate change in y during jump and update y """
        #This sets the time step for each calculation
        time = tick/90
        self.delta_y = self.v * time + 0.5 * self.g * math.pow(time, 2)
        self.v = self.v + time * self.g
        self.y += self.delta_y

    def move(self):
        """ Move character according to user input."""
        #Constant jumping
        self.jump()
        #Left,Right controls
        if pg.key.get_pressed()[self.left]:
            self.x += -5
        if pg.key.get_pressed()[self.right]:
            self.x += 5
        """if pg.key.get_pressed()[self.fire] and len(self.babykangas) == 0:
            babykanga = BabyKanga(self.x,self.y)
            self.babykangas.append(babykanga)
            self.pouch -= 1"""


    def boundry_detection(self,other):
        """ Detect screen boundries and adjust accordingly.

        If the character falls off the bottom they reappear at the top. If they go
        off a side they loop to the other side.
        """
        if self.y >= screen_height:
            self.y = 825
            #self.end_screen(other)
            other.score += 1
            map.reset()

        if self.x > screen_width:
            self.x = 0
        if self.x < 0:
            self.x = screen_width

    def scroll_detection(self, other):
        if self.delta_y > 0:
            map.scroll = 0
        else:
            if self.y <= map.scroll_point:
                map.scroll = map.scroll_point - self.y
                self.y = map.scroll_point
                map.move_map()
                other.opponent_scroll_detection()

    def opponent_scroll_detection(self):
        if map.scroll != 0 and self.y > map.scroll_point:
            self.y += map.scroll
            self.draw_character()


    def collision_detection(self, obj_list):
        """Checks for collison with platforms and adjusts accordingly. """
        #Creates a list of platform location using their rectangles
        rect_list = []
        for obj in obj_list:
            rect_list.append(obj.rect)
        #Collider rect created under character
        self.bottom_collider = pg.Rect(self.x-(self.size/2), self.y + (self.size/2), self.size, self.delta_y)
        #Checks for collision and, if so, records which platform was collided with
        self.current_plat = self.bottom_collider.collidelist(rect_list)
        #Checks which platform was collided with and if the character is falling
        if self.current_plat != -1 and self.delta_y > 0:
            #Places character on top of platform it collided with
            self.y = (rect_list[self.current_plat].top) - (self.size/2)
            #Starts a new jump
            self.v = -60
            #initiates falling function
            obj_list.remove(obj_list[self.current_plat])

    def pouch_detection(self, other):
        location_rect = self.surf.get_rect(center=(self.x,self.y))
        if location_rect.collidelist(other.babykangas):
            self.pouch +=  1
            self.lives -= 1
            if self.lives == 0:
                other.score += 1
                map.reset()

    def idk(self):
        if self.babykangas[0].y <= 0:
            self.babykangas.remove(self.babykangas[0])


    def run_character(self,other):
        """Run character functions

        other = other character name
        """
        self.draw_character()
        self.move()
        self.boundry_detection(other)
        self.scroll_detection(other)
        #self.pouch_detection(other)
        self.collision_detection(map.plat_obj)

class BabyKanga:

        #Initialize babykanga instance.(Tank instance firing, opponent's Tank instance)
    def __init__(self, kangx,kangy, name='joey'):
        self.x = kangx
        self.y = kangy
        self.mother = name
        self.vert_speed = 9
        self.v = -60
        self.g = 9.81
        self.delta_y = 0
        self.where = True

        #Draws babykanga
    def draw_babykanga(self):
        pg.draw.rect(screen, DRIEDBLOOD, (self.x, self.y, 4, 8), 0)
        self.trajectory2()
        self.rect = pg.Rect(self.x, self.y, 4, 4)

    def trajectory2(self):
        self.y -= 8

    def trajectory1(self):
        if self.where == True and self.y >= 250:
            self.y -= self.vert_speed
        else:
            #change sprite
            time = tick/40
            self.delta_y = self.v * time + 0.5 * self.g * math.pow(time, 2)
            self.v = self.v + time * self.g
            self.y += self.delta_y
            self.where = False
            if self.delta_y >= 0:
                self.x = self.mother.x


class Map:
    """Generate new platforms as character moves up

    """
    def __init__(self):
        #Verticle distance between platforms at start
        self.spacing = 30
        #Point at which the screen scrolls
        self.scroll_point = 200
        self.scroll = 0
        self.plat_obj = []

    def initialize(self):
        """Set starting screen with platforms.

        Two set platforms for character starting positions. Predetermined Y coordinates
        for rest of platforms but random X coordinates.
        """
        self.generate_plat(150, 850)
        self.generate_plat(450, 850)
        for num in range(100,900,50):
            rando_placement = random.randint(15, screen_width -15)
            self.generate_plat(rando_placement, 900 - num)
            if random.randint(1,4) == 4:
                second_rando = random.randint(15 ,screen_width-15)
                while abs(rando_placement - second_rando) <= 60:
                    second_rando = random.randint(15,screen_width-15)
                self.generate_plat(second_rando, 900 - num)


    def generate_plat(self, x, y):
        """Create new platform object at specified Y coordinate

        Append platform object to platform object list. Draw the new platform on the screen.

        Parameter
        ----------
        y: int
            Y coordinate of center of new platform
        x: int
            X coordinate of center of new platform
        """
        plat = Platform()
        self.plat_obj.append(plat)
        plat.draw_platform(x,y)

    def draw_map(self):
        #Iterates through platform list and draws them all
        for plat in self.plat_obj:
            plat.draw_platform(plat.x,plat.y)

    def move_map(self):
        """ Scroll map in relation to character height"""
        if map.scroll != 0:
            for plat in self.plat_obj:
                plat.y += self.scroll


    def proximity_check(self):
        """Check if there is self.spacing distance between the top platform and the top of the screen"""
        if self.plat_obj[-1].top < self.spacing:
            return False
        else:
            return True

    def off_the_edge(self):
        """Check if a platform is off the bottom of the screen and remove it from the list if so"""
        if self.plat_obj[0].top > screen_height:
            self.plat_obj.remove(self.plat_obj[0])

    def new_plat(self):
        if self.proximity_check():
            rando_placement = random.randint(15, screen_width-15)
            self.generate_plat(rando_placement,-5)
            if random.randint(1,3) == 1:
                second_rando = random.randint(15,screen_width-15)
                while abs(rando_placement - second_rando) <= 60:
                    second_rando = random.randint(15,screen_width-15)
                self.generate_plat(second_rando,-5)


    def score_board(self):
        red_text = '%s has %d points!' % (red.name, red.score)
        red_score = font.render(red_text, False, red.color, GREY)
        screen.blit(red_score,(360,20))
        blue_text = '%s has %d points!' % (blue.name, blue.score)
        blue_score = font.render(blue_text, False, blue.color, GREY)
        screen.blit(blue_score,(30,20))

        """red_lives = '%s lives: %d' % (red.name, red.lives)
        red_life_text = font.render(red_lives, False, red.color, GREY)
        screen.blit(red_life_text,(360,50))
        blue_lives = '%s lives: %d' % (blue.name, blue.lives)
        blue_life_text = font.render(blue_lives, False, blue.color, GREY)
        screen.blit(blue_life_text,(30,50))"""


    def reset(self):
        self.__init__()
        self.initialize()
        red.__init__('Red',RED, pg.K_LEFT, pg.K_RIGHT, pg.K_UP,450, score = red.score)
        blue.__init__('Blue', BLUE, pg.K_a, pg.K_d, pg.K_w, score = blue.score)

    def run_map(self):
        """Run it all"""
        self.draw_map()
        self.off_the_edge()
        self.new_plat()
        self.score_board()


map = Map()
map.initialize()
red = Character('Red',RED, pg.K_LEFT, pg.K_RIGHT, pg.K_UP, 450)
blue = Character('Blue', BLUE, pg.K_a, pg.K_d, pg.K_w)



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
    tick = clock.tick(60)


    for babykanga in red.babykangas:
        babykanga.draw_babykanga()

    for babykanga in blue.babykangas:
        babykanga.draw_babykanga()



    map.run_map()
    blue.run_character(red)
    red.run_character(blue)


    #Update the screen
    pg.display.flip()

# Close the window and quit.
pg.quit()
