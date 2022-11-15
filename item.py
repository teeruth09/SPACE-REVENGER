from consts import HEIGHT,BLACK, WIDTH
from ship import Ship
import pygame
import os

import random

from utils import collide

# Load images
MED_KIT = pygame.transform.scale(pygame.image.load("SourceCode/Textures/heal.png"),(20,20))
POWER_UP = pygame.transform.scale(pygame.image.load("SourceCode/Textures/itemSpeed.png"),(20,20))

LIVE_UP = pygame.transform.scale(pygame.image.load("SourceCode/Textures/hpitem.png"),(20,20))

class Item:
    ITEM_MAP = {
        "med_kit": MED_KIT,
    }

    def __init__(self, x, y, item = "med_kit"):
       
        self.x = x
        self.y = y
        self.ship_img = self.ITEM_MAP[item]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel = 1

    def draw(self, window):
        self.move()
        window.blit(self.ship_img, (self.x, self.y))

    def move(self):
        self.y += self.vel

    def collision(self, player):
        return collide(self, player)

class PowerUp:
    
    ITEM_MAP = {
        "power_Up": POWER_UP,
    }

    def __init__(self, x, y, item = "power_Up"):
       
        self.x = x
        self.y = y
        self.ship_img = self.ITEM_MAP[item]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel = 1

    def draw(self, window):
        self.move()
        window.blit(self.ship_img, (self.x, self.y))

    def move(self):
        self.y += self.vel

    def collision(self, player):
        return collide(self, player)

class LiveUp:
    
    ITEM_MAP = {
        "live_Up": LIVE_UP,
    }

    def __init__(self, x, y, item = "live_Up"):
       
        self.x = x
        self.y = y
        self.ship_img = self.ITEM_MAP[item]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel = 1

    def draw(self, window):
        self.move()
        window.blit(self.ship_img, (self.x, self.y))

    def move(self):
        self.y += self.vel

    def collision(self, player):
        return collide(self, player)
