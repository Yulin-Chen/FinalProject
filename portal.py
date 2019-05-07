import pygame as pg
import random
import time
import math

class Portal:
    """Creates portal sprites. Portals switch the two kangaroos positions when hit."""
    def __init__(self):
        self.size = 30
        self.surf = pg.Surface((self.size,self.size))
        self.surf.fill(MAGENTA)

    def draw_portal(self, x, y):
        """ Blit surface that represents character. """
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x  - (self.size/2), self.y - (self.size/2), self.size, self.size)
        #Draw and blit character to screen
        screen.blit(self.surf,(self.x - self.size/2, self.y - self.size/2))
