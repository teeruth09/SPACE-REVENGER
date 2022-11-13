import pygame
import os
from item import Item

from ship import Ship
from consts import WIDTH, HEIGHT, RED, GREEN,BLUE,DARKBLUE

#sound
from pygame import mixer
pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()

#Load SpaceShip
PLAYER_SPACE_SHIP = pygame.transform.scale(pygame.image.load("Textures/ship2.png"),(70,70))
PLAYER_LASER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Textures/pow.png"),(30,30)),90)

#Load sounds
laser_fx = pygame.mixer.Sound("SoundEffect/laser.wav")
laser_fx.set_volume(0.10)

explosion_fx = pygame.mixer.Sound("SoundEffect/explosion.wav")
explosion_fx.set_volume(0.10)

class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y, health=100)
        self.ship_img = PLAYER_SPACE_SHIP
        self.laser_img = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health =100
        self.vel = 8                        #player speed 
        self.damage = 5                     #laser player damage
 
        #playerScore
        self.Playerscore = 0

    def move(self, key):
        if key[pygame.K_a] and self.x - self.vel > 0:  # left
            self.x -= self.vel
        elif key[pygame.K_d] and self.x + self.vel + self.get_width() < WIDTH:  # right
            self.x += self.vel
        else:                                                  
            self.ship_img = PLAYER_SPACE_SHIP

        if key[pygame.K_w] and self.y - self.vel > 0:  # up
            self.y -= self.vel
        if key[pygame.K_s] and self.y + self.vel + self.get_height() + 15 < HEIGHT:  # down
            self.y += self.vel

        if key[pygame.K_SPACE ]:                  #shoot laser       
            laser_fx.play()
            self.shoot()

    def move_lasers(self, vel, objs):                 #self vel = velocity 
        self.cooling_down()
        for laser in self.lasers:
            laser.move(vel)                           #laser move with speed
            if laser.off_screen(HEIGHT):              
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if obj.health - self.damage <= 0:       #enemies died
                            explosion_fx.play()
                            objs.remove(obj)
                            if obj.__class__.__name__ == 'Boss':
                                ##scoreplayer ++ when Boss died
                                self.Playerscore +=30
                                
                                if laser in self.lasers:
                                    self.lasers.remove(laser) 

                                pass
                                break
                            #scoreplayer ++ when enemy died
                            self.Playerscore += 10
                            
                        else:                                                     #enemy have not died
                            obj.health -= self.damage

                        if laser in self.lasers:
                            self.lasers.remove(laser)  

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)               #draw health_bar

    def health_bar(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, GREEN,
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))
        