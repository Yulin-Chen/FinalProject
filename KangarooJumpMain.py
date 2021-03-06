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
LUSHGREEN = (0, 158, 26)
VELVET = (71, 4, 114)
BLU = (57, 33, 239)
WHITE = (255,255,255)
MAGENTA = (160, 15, 196)
SUNBLEACHEDGRAPE = (206, 132, 224)
ORANGE = (224, 115, 0)
GREEN = (76, 173, 94)

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
FPS = 60

#initialize fonts
font = pg.font.SysFont('stkaiti', 40, True)
font1 = pg.font.SysFont('stkaiti', 60, True)
font2 = pg.font.SysFont('stkaiti',120)
font3 = pg.font.SysFont('stkaiti',60)
largerText = pg.font.SysFont("comicsansms",115)
largeText = pg.font.SysFont("comicsansms",80)


def printtext(font,text,x,y,color):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))



class Platform:
    """Define a platform"""

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
        #Rect around sprite, used for collision detection
        self.rect = pg.Rect(self.x  - (self.width/2), self.y - (self.height/2), self.width, self.height)
        #Helps track platforms
        self.top = self.rect.top
        self.position = self.top - int(self.height/2)
        #Blit platform onto scree
        screen.blit(self.plat,(self.x  - (self.width/2), self.y - (self.height/2)))

class Portal:
    """Define a portal.

    Portals switch the characters positions when collided with"""

    def __init__(self):
        self.size = 100
        self.x = 300
        self.y = 400
        self.rect = pg.Rect(self.x  - (self.size/4), self.y - (self.size/4), self.size*1/2, self.size*1/2)
        #List of rotation positions
        self.sprite_list = []
        #list index for sprite position (rotation)
        self.position = 11
        #fills list with rotated sprite surfaces
        for i in range(1,13):
            self.sprite_list.append(pg.transform.scale(pg.image.load('sprites/portalRotations/position%d.png' % i),(self.size,self.size)))
        self.animation_rate = 7
        self.frame_counter = 0
        self.teleport_started = False
        self.exit_portalX = 0
        self.exit_portalY = 0
        self.sound = pg.mixer.Sound('sprites/Sounds/portal.wav')
        self.sound.set_volume(1)


    def draw_portal(self, x, y):
        """ Move and blit portal to screen"""
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x  - (self.size/4), self.y - (self.size/4), self.size*1/2, self.size*1/2)
        self.spin_portal()
        screen.blit(self.sprite,(self.x - self.size/2, self.y - self.size/2))

    def draw_exit_portal(self):
        """ Create exit portal and blit"""
        self.exit_rect = pg.Rect(self.exit_portalX  - (self.size/4), self.exit_portalY - (self.size/4), self.size*1/2, self.size*1/2)
        self.spin_portal()
        screen.blit(self.sprite,(self.exit_portalX - self.size/2, self.exit_portalY - self.size/2))

    def spin_portal(self):
        """Iterate through sprite_list to animate spinning portal"""
        self.frame_counter += 1
        self.sprite = self.sprite_list[self.position]
        #Set speed of spinning
        if self.frame_counter % self.animation_rate == 0:
            self.position -=1
        if self.position == -1:
            self.position = 11

    def portal_event(self, primary, secondary):
        """ Reacts to a portal being hit by a player

        Parameter
        ----------
        primary: name of kangaroo instance hitting portal
        secondary: name of kangaroo opponent instance
        """
        #Set initial conditions
        if not self.teleport_started:
            self.exit_portalX = secondary.x
            self.exit_portalY = secondary.y
            self.teleport_started = True
            primary.entering = True
            self.sound.play()
        portal.draw_exit_portal()
        #Entrance sequence
        if primary.size > 10 and primary.entering == True:
            primary.enter_portal(self.x,self.y)
            secondary.enter_portal(self.exit_portalX,self.exit_portalY)
        #Exit sequence
        elif primary.size < 60:
            primary.entering = False
            primary.exit_portal(self.exit_portalX,self.exit_portalY)
            secondary.exit_portal(self.x,self.y)
        #Reset all flags
        else:
            primary.hit_portal = False
            secondary.sucked_in = False
            map.portal_active = False
            self.teleport_started = False


class Character():
    """Build character

    Create and add character to screen. Set constant jump. Move with arrow keys.
    Detect collisions and react appropriatley.
    """

    def __init__(self,name, color, left, right, sprite_num, x = 150, y = 820, score=0):
        """ Initialize

        Parameter
        ----------
        name: str
            name of kangaroo
        color: color (RGB)
            kangaroo's text color
        left: pygame.key
            controls left motion
        right: pygame.key
            controls right motion
        sprite_num: int
            which character it is
        x: int
            x position
        y: int
            y position
        score: int
            character score
        """
        self.number = sprite_num
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
        self.imageR = pg.image.load('sprites/Kanga%dR.png' % self.number)
        self.imageL = pg.image.load('sprites/Kanga%dL.png' % self.number)
        self.spriteR = pg.transform.scale(self.imageR,(self.size,self.size))
        self.spriteL = pg.transform.scale(self.imageL,(self.size,self.size))
        self.going_right = True
        self.score = score
        self.hit_portal = False
        self.sucked_in = False
        self.entering = False
        self.frame_counter = 0
        self.portal_sprite_list = []
        self.animation_rate = 3
        self.spin_position = 0
        for i in range(1,13):
            self.portal_sprite_list.append(pg.transform.scale(pg.image.load('sprites/Kanga%dRots/position%d.png' % (self.number,i)),(int(self.size*1.3),int(self.size*1.3))))

    def draw_character(self):
        """ Blit character. """
        #Determine which direction sprite faces
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
        """Game over screen"""
        #set text colors
        losercolor = self.color
        winnercolor = other.color
        screen.fill(WHITE)
        printtext(font2,"GAMEOVER",75,300,losercolor)
        printtext(font3, other.name +" "+"Wins!!",160,500,winnercolor)
        printtext(font,'%s got %d points' % (other.name, other.score),180,550,other.color)
        printtext(font,'%s got %d points' % (self.name, self.score),180,600,self.color)

        pg.display.update()
        clock.tick(60)


    def boundry_detection(self,other):
        """ Detect screen boundries and adjust accordingly.

        If the character falls off the bottom they reappear at the top. If they go
        off a side they loop to the other side.
        """
        if self.y >= screen_height:
            other.score += 1
            self.game_over(other)
            clock.tick(1)
            #pg.time.wait(1000)
            play.reset()


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

    def freeze(self):
        self.x = self.x
        self.y = self.y

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
                self.hit_portal = True

    def spin_kanga(self):
        self.frame_counter += 1
        self.sprite = self.portal_sprite_list[self.spin_position]
        if self.frame_counter % self.animation_rate == 0:
            self.spin_position +=1
        if self.spin_position == 12:
            self.spin_position = 0
        return self.sprite

    def enter_portal(self, portalX, portalY):
        self.x = portalX
        self.y = portalY
        self.size -= 1
        sprite = pg.transform.scale(self.spin_kanga(), (self.size, self.size))
        screen.blit(sprite,(self.x - self.size/2, self.y - self.size/2))

    def exit_portal(self, exit_portalX, exit_portalY):
        self.x = exit_portalX
        self.y = exit_portalY
        self.size += 1
        sprite = pg.transform.scale(self.spin_kanga(), (self.size, self.size))
        screen.blit(sprite,(self.x - self.size/2, self.y - self.size/2))


    def run_character(self,other):
        """Run character functions

        other = other character name
        """
        if not self.hit_portal and not self.sucked_in:
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
        self.height = screen_height
        self.portal_active = False
        self.background_image = pg.image.load('sprites/Brocollli.png')
        self.stretched_bg = pg.transform.scale(self.background_image,(screen_width,int(screen_height * 2/3)))
        self.bgx1 = 600
        self.bgx2 = 0
        self.bgx3 = -600


    def initialize(self):
        """Set starting screen with platforms.

        Two set platforms for character starting positions. Predetermined Y coordinates
        for rest of platforms but random X coordinates.
        """
        self.generate_plat(150, 850)
        self.generate_plat(450, 850)
        for num in range(100,1400,self.spacing):
            self.plats_at_height(900-num,3)

    def background(self):
        if not portal.teleport_started:
            self.bgx1 += self.scroll*0.5
            self.bgx2 += self.scroll*0.5
            self.bgx3 += self.scroll*0.5
        screen.blit(map.stretched_bg,(0,self.bgx3))
        screen.blit(map.stretched_bg,(0,self.bgx2))
        screen.blit(map.stretched_bg,(0,self.bgx1))
        if self.bgx3 >= 0:
            self.bgx1 = 600
            self.bgx2 = 0
            self.bgx3 = -600


    def plats_at_height(self, y, freq_double_plats):
        """Create new platform object at specified Y coordinate

        Append platform object to platform object list. Draw the new platform on the screen.

        Parameter
        ----------
        y: int
            Y coordinate of center of new platform
        freq_double_plats: int
            1 in int chance of double plat at given x height
        """
        rando_placement = random.randint(15, screen_width -15)
        self.generate_plat(rando_placement, y)
        if random.randint(1,freq_double_plats) == 1:
            second_rando = random.randint(15 ,screen_width-15)
            while abs(rando_placement - second_rando) <= 120:
                second_rando = random.randint(15,screen_width-15)
            self.generate_plat(second_rando, y)

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
        if self.plat_obj[-1].position < -350 + self.spacing -10:
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
            self.plats_at_height(-355, 3)

    def call_portal(self):
        if not self.portal_active and random.randint(0,450) == 22:
            self.portal_active = True
            portal.x = random.randint(20, screen_width-20)
            portal.y = -70
            portal.rect = pg.Rect(portal.x  - (portal.size/4), portal.y - (portal.size/4), portal.size*1/2, portal.size*1/2)

    def run_map(self):
        """Run it all"""
        self.draw_map()
        self.off_the_edge()
        self.new_plat()
        self.call_portal()



class Game:
    def __init__(self):
        pass

    def score_board(self):
        george_head = pg.transform.scale(pg.image.load('sprites/Head1.png'),(50,50))
        george_score = font1.render(str(george.score), True, SUNBLEACHEDGRAPE)
        screen.blit(george_score,(80,15))
        screen.blit(george_head,(20,10))

        fred_head = pg.transform.scale(pg.image.load('sprites/Head2.png'),(50,50))
        fred_score = font1.render(str(fred.score), True, SUNBLEACHEDGRAPE)
        screen.blit(fred_score,(530,15))
        screen.blit(fred_head,(470,5))


    def reset(self):
        map.__init__()
        map.initialize()
        fred.__init__('Fred',RED, pg.K_LEFT, pg.K_RIGHT,2, 450, score = 0)
        george.__init__('George', BLUE, pg.K_a, pg.K_d,1, score = 0)
        portal.__init__()


    def portal_hit_who(self):
        if fred.hit_portal == False and george.hit_portal == False:
            return
        elif fred.hit_portal:
            george.sucked_in = True
            portal.portal_event(fred,george)
        else:
            fred.sucked_in = True
            portal.portal_event(george, fred)

    def run_game (self):
        map.run_map()
        self.score_board()
        george.run_character(fred)
        fred.run_character(george)
        self.portal_hit_who()


pg.mixer.music.set_volume(0.2)
pg.mixer.music.load('sprites/Sounds/bgm.ogg')
pg.mixer.music.play(-1)

play = Game()
map = Map()
map.initialize()
portal = Portal()
fred = Character('Fred',RED, pg.K_LEFT, pg.K_RIGHT, 2 ,450)
george = Character('George', BLUE, pg.K_a, pg.K_d, 1)


pause = False
startgame = False

# -------- Main Program Loop -----------
while not done:

    while startgame == False:
        screen.fill(WHITE)
        printtext(largerText,"Welcome to",80,200,RED)
        printtext(largeText,"Kangaroo Jump",90,300,BLUE)
        printtext(font3,"click anywhere to start", 80, 500,BLACK)
        fred.draw_character()
        george.draw_character()
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                startgame = True
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = True
            if event.key == pg.K_r:
                play.reset()


    if startgame == True:
        # Limit frames per second
        tick = clock.tick(FPS)

        # Clears old screen
        map.background()
        play.run_game()

        #Update the screen
    pg.display.flip()



# Close the window and quit.
pg.quit()
