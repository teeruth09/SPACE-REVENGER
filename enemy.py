from ship import Ship
import pygame
import os

from consts import WIDTH,HEIGHT, RED, GREEN,BLUE,DARKBLUE

# Load images
RED_SPACE_SHIP = pygame.transform.scale(pygame.image.load("Textures/en2.png"),(60,60))
GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load("Textures/en1.png"),(70,70))
BLUE_SPACE_SHIP = pygame.transform.scale(pygame.image.load("Textures/en3.png"),(70,70))
BOSS_SHIP = pygame.transform.scale(pygame.image.load("Textures/Boss.png"),(90,90))


# Lasers
RED_LASER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Textures/redbullet.png"),(30,30)),180)
GREEN_LASER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Textures/greenbullet.png"),(30,30)),180)
BLUE_LASER = pygame.transform.rotate(pygame.image.load("Textures/Bullet.png"),-90)
BOSS_LASER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Textures/pow.png"),(80,80)),-90)


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel = 1
       
    def move(self):                                          
        self.y += self.vel        
        
class Boss(Ship):
    def __init__(self, x, y, level):
        super().__init__(x, y, health=30, cool_down=2)
        self.ship_img = BOSS_SHIP
        self.laser_img = BOSS_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel = 3 + level                                      #Boss speed + level
        self.direction = 'down'
        self.max_health = 30
        self.health = 30 + (level*10)                  #Boss HP: level1 40 level2 50 level3 60 level4 70 level5 80  level6 90 level7 100

    def move(self):
        if self.direction == 'down':
            if self.y + self.vel <= 100:
                self.y += self.vel
            else:
                self.direction = 'left'

        if self.direction == 'left':
            if self.x - self.vel >= 0:
                self.x -= self.vel                                #Boss move left
            else:
                self.direction = 'right'

        if self.direction == 'right':
            if self.x + self.vel + self.get_width() <= WIDTH:
                self.x += self.vel                                   #Boss move right
            else:
                self.direction = 'left'


    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y - 10, self.ship_img.get_width(), 10))
             
        if self.health >= 40:
            pygame.draw.rect(window,RED , (self.x-5, self.y - 10, self.ship_img.get_width()+(self.health / self.max_health)+20, 10))
            if self.health >= 50:
                pygame.draw.rect(window, "#DC143C", (self.x-5, self.y - 10, self.ship_img.get_width() + (self.health / self.max_health)+25, 10))
                if self.health >= 60: 
                    pygame.draw.rect(window, "#B22222", (self.x-10, self.y - 10, self.ship_img.get_width()+(self.health / self.max_health)+30, 10))
                    if self.health >= 70: 
                        pygame.draw.rect(window, "#800000", (self.x-10, self.y - 10, self.ship_img.get_width()+(self.health / self.max_health)+35, 10))
                        if self.health >= 80:
                            pygame.draw.rect(window, "#8B0000", (self.x-15, self.y - 10, self.ship_img.get_width()+(self.health / self.max_health)+40, 10))
