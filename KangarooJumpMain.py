import pygame as pg
import random
import time
import math
import os

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
WHITE = (255,255,255)
MAGENTA = (169, 69, 178)

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
font2 = pg.font.SysFont('stkaiti',120)
font3 = pg.font.SysFont('stkaiti',60)

def printtext(font,text,x,y,color):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))

class Platform:
    """Create a new platform

    """
    #Initialize platform attributes
    def __init__(self):
        self.width = 120
        self.height = 15
        self.image = pg.image.load('sprites/Platform.PNG')
        self.plat = pg.transform.scale(self.image,(self.width,self.height))


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
        self.position = self.top - int(self.height/2)
        screen.blit(self.plat,(self.x  - (self.width/2), self.y - (self.height/2)))

class Portal:
    """Creates portal sprites. These switch the two kangaroos locations.

    """
    def __init__(self):
        self.size = 80
        self.image = pg.image.load('sprites/portal2.png')
        self.portal = pg.transform.scale(self.image,(self.size,self.size))

    def draw_portal(self, x, y):
        """ Blit surface that represents character. """
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x  - (self.size/2), self.y - (self.size/2), self.size, self.size)
        #Draw and blit character to screen
        screen.blit(self.portal,(self.x - self.size/2, self.y - self.size/2))


class Character():
    """Build character

    Create and add character to screen. Set constant jump. Move with arrow keys.
    Detect collisions wih platforms and react appropriatley.

    End Goal:
    Currently the characters are represented as square surfaces.
    """

    def __init__(self,name, color, left, right, sprite_num, x = 150, y = 825, score=0):
        self.name = name
        self.color = color
        self.left = left
        self.right = right
        self.x = x
        self.y = y
        self.size = 60
        self.v = -60
        self.g = 9.81
        self.delta_y = 0
        self.imageR = pg.image.load('sprites/Kanga%dR.png' % sprite_num)
        self.imageL = pg.image.load('sprites/Kanga%dL.png' % sprite_num)
        self.spriteR = pg.transform.scale(self.imageR,(self.size,self.size))
        self.spriteL = pg.transform.scale(self.imageL,(self.size,self.size))
        self.going_right = True
        self.score = score


    def draw_character(self):
        """ Blit surface that represents character. """
        #Draw and blit character to screen
        if self.going_right:
            sprite = self.spriteR
        else:
            sprite = self.spriteL
        screen.blit(sprite,(self.x - self.size/2, self.y - self.size/2))

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
            self.going_right = False
        if pg.key.get_pressed()[self.right]:
            self.x += 5
            self.going_right = True

    def game_over(self,other):
        losercolor = self.color
        winnercolor = other.color
        screen.fill(WHITE)
        printtext(font2,"GAMEOVER",75,300,losercolor)
        printtext(font3, other.name +" "+"Wins!!",200,500,winnercolor)
        #button("Restart", 210,700,30,160,RED,ORANGE)
        printtext(font,'%s got %d points' % (other.name, other.score),200,550,other.color)
        printtext(font,'%s got %d points' % (self.name, self.score),200,600,self.color)

        pg.display.update()

    def button(msg,x,y,w,h,ic,ac):
        mouse = pg.mouse.get_pos()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pg.draw.rect(gameDisplay, ac,(x,y,w,h))
        else:
            pg.draw.rect(gameDisplay, ic,(x,y,w,h))

        smallText = pg.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        gameDisplay.blit(textSurf, textRect)


    def boundry_detection(self,other):
        """ Detect screen boundries and adjust accordingly.

        If the character falls off the bottom they reappear at the top. If they go
        off a side they loop to the other side.
        """
        if self.y >= screen_height:
            self.y = 825
            #self.end_screen(other)
            other.score += 1
            self.game_over(other)
            pg.time.wait(1000)
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

        #Collider rect created under character's feet
        if self.going_right:
            self.bottom_collider = pg.Rect(int(self.x), self.y + (self.size/2), self.size * 5/12, self.delta_y)
        else:
            self.bottom_collider = pg.Rect(int(self.x-(self.size * 4/10)), self.y + (self.size/2), self.size * 5/12, self.delta_y)
        #Checks for collision and, if so, records which platform was collided with
        self.current_plat = self.bottom_collider.collidelist(rect_list)
        #Checks which platform was collided with and if the character is falling
        if self.current_plat != -1 and self.delta_y > 0:
            #Places character on top of platform it collided with
            self.y = (rect_list[self.current_plat].top) - (self.size/2)
            #Starts a new jump
            self.v = -60
            self.score+=1
            obj_list.remove(obj_list[self.current_plat])


    def portal_detection(self,other):
        if map.portal_active == False:
            return
        else:
            self.rect = pg.Rect(self.x  - (self.size/2), self.y - (self.size/2), self.size, self.size)
            if self.rect.colliderect(portal.rect):
                tempx = other.x
                tempy = other.y
                other.x = self.x
                other.y = self.y
                self.x = tempx
                self. y = tempy
                map.portal_active = False


    def run_character(self,other):
        """Run character functions

        other = other character name
        """
        self.draw_character()
        self.move()
        self.boundry_detection(other)
        self.scroll_detection(other)
        self.collision_detection(map.plat_obj)
        self.portal_detection(other)


class Map:
    """Generate new platforms as character moves up

    """
    def __init__(self):
        #Verticle distance between platforms at start
        self.spacing = 50
        #Point at which the screen scrolls
        self.scroll_point = 200
        self.scroll = 0
        self.plat_obj = []
        self.portal_obj = []
        self.height = screen_height
        self.portal_active = False

    def initialize(self):
        """Set starting screen with platforms.

        Two set platforms for character starting positions. Predetermined Y coordinates
        for rest of platforms but random X coordinates.
        """
        self.generate_plat(150, 850)
        self.generate_plat(450, 850)
        for num in range(100,900,self.spacing):
            self.plats_at_height(900-num,3)

    def plats_at_height(self, x, freq_double_plats):
        """Create new platform object at specified Y coordinate

        Append platform object to platform object list. Draw the new platform on the screen.

        Parameter
        ----------
        x: int
            X coordinate of center of new platform
        freq_double_plats: int
            1 in int chance of double plat at given x height
        """
        rando_placement = random.randint(15, screen_width -15)
        self.generate_plat(rando_placement, x)
        if random.randint(1,freq_double_plats) == 1:
            second_rando = random.randint(15 ,screen_width-15)
            while abs(rando_placement - second_rando) <= 120:
                second_rando = random.randint(15,screen_width-15)
            self.generate_plat(second_rando, x)



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
        if self.portal_active:
            portal.draw_portal(portal.x,portal.y)

    def move_map(self):
        """ Scroll map in relation to character height"""
        if self.scroll != 0:
            self.height += self.scroll
            for plat in self.plat_obj:
                plat.y += self.scroll
            if self.portal_active:
                portal.y += self.scroll

    def proximity_check(self):
        """Check if there is self.spacing distance between the top platform and the top of the screen"""
        if self.plat_obj[-1].position < self.spacing-20:
            return False
        else:
            return True

    def off_the_edge(self):
        """Check if a platform is off the bottom of the screen and remove it from the list if so"""
        if self.plat_obj[0].top > screen_height:
             self.plat_obj.remove(self.plat_obj[0])
        if self.portal_active and portal.y > screen_height + portal.size:
            self.portal_active = False

    def new_plat(self):
        if self.proximity_check():
            self.plats_at_height(-10, 3)


    def generate_portal(self):
        while self.height == screen_height:
            return
        if not self.portal_active and random.randint(0,300) == 7:
            self.portal_active = True
            portal.x = random.randint(20, screen_width-20)
            portal.y = random.randint(-70,-20)
            portal.rect = pg.Rect(portal.x  - (portal.size/2), portal.y - (portal.size/2), portal.size, portal.size)


    def score_board(self):
        red_text = '%s has %d points!' % (red.name, red.score)
        red_score = font.render(red_text, False, red.color, GREY)
        screen.blit(red_score,(360,20))
        blue_text = '%s has %d points!' % (blue.name, blue.score)
        blue_score = font.render(blue_text, False, blue.color, GREY)
        screen.blit(blue_score,(30,20))

    def paused(self):

        largeText = pg.font.SysFont("comicsansms",115)
        # TextSurf, TextRect = text_objects("Paused", largeText)
        # TextRect.center = ((display_width/2),(display_height/2))
        # gameDisplay.blit(TextSurf, TextRect)


        while pause:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            screen.fill(WHITE)
            printtext(largeText,"Paused",75,400,RED)

        #button("Continue",150,450,100,50,green,bright_green,unpause)
        #button("Quit",550,450,100,50,red,bright_red,quitgame)

            pg.display.update()
            clock.tick(15)

    def reset(self):
        self.__init__()
        self.initialize()
        red.__init__('Red',RED, pg.K_LEFT, pg.K_RIGHT,2, 450, score = 0)
        blue.__init__('Blue', BLUE, pg.K_a, pg.K_d,1, score = 0)

    def run_map(self):
        """Run it all"""
        self.draw_map()
        self.off_the_edge()
        self.new_plat()
        self.generate_portal()
        self.score_board()




map = Map()
map.initialize()
portal = Portal()
red = Character('Player1',RED, pg.K_LEFT, pg.K_RIGHT, 2 ,450)
blue = Character('Player2', BLUE, pg.K_a, pg.K_d, 1)



pause = False



# -------- Main Program Loop -----------
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                print('pause')
                pause = True
                map.paused()
        #Escape key alternative way to end game
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True
        if pause == True:

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause = False
                    print('resume')
    # Clears old screen
    screen.fill(WHITE)


    # Limit frames per second
    tick = clock.tick(60)


    map.run_map()
    blue.run_character(red)
    red.run_character(blue)


    #Update the screen
    pg.display.flip()

# Close the window and quit.
pg.quit()
