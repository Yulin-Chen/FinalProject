import pygame as pg
import random
import time
import math


class Character():
    """Build character

    Create and add character to screen. Set constant jump. Move with arrow keys.
    Detect collisions wih platforms and react appropriatley.

    End Goal:
    Currently the characters are represented as square surfaces. This will be changed to animated sprites.
    """

    def __init__(self, color, left, right, x = 150, y = 825):
        self.left = left
        self.right = right
        self.x = x
        self.y = y
        self.size = 40
        self.v = -60
        self.g = 9.81
        self.delta_y = 0
        self.surf = pg.Surface((self.size,self.size))
        self.surf.fill(color)


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
            self.x += -4
        if pg.key.get_pressed()[self.right]:
            self.x += 4

    def boundry_detection(self):
        """ Detect screen boundries and adjust accordingly.

        If the character falls off the bottom they reappear at the top. If they go
        off a side they loop to the other side.
        """
        if self.y > screen_height:
            self.y = 400
        if self.x > screen_width:
            self.x = 0
        if self.x < 0:
            self.x = screen_width

    def scroll_detection(self):
        if self.delta_y > 0:
            map.scroll = 0
        else:
            if self.y <= map.scroll_point:
                map.scroll = map.scroll_point - self.y
                self.y = map.scroll_point
                map.move_map()

    def opponent_scroll_detection(self):
        if map.scroll != 0 and self.y > map.scroll_point:
            self.y += map.scroll


    def collision_detection(self, obj_list):
        """Checks for collison with platforms and adjusts accordingly. """
        #Creates a list of platform location using their rectangles
        rect_list = []
        for obj in obj_list:
            rect_list.append(obj.rect)
        #Collider rect created under character
        self.bottom_collider = pg.Rect(self.x-(self.size/2), self.y + (self.size/2), self.size, 5)
        #Checks for collision and, if so, records which platform was collided with
        self.current_plat = self.bottom_collider.collidelist(rect_list)
        #Checks which platform was collided with and if the character is falling
        if self.current_plat != -1 and self.delta_y > 0:
            #Places character on top of platform it collided with
            self.y = (rect_list[self.current_plat].top) - (self.size/2)
            #Starts a new jump
            self.v = -60

    def run_character(self):
        """Run character functions"""
        self.draw_character()
        self.move()
        self.boundry_detection()
        self.scroll_detection()
        self.opponent_scroll_detection()
        self.collision_detection(map.plat_obj)
