rom laser import Laser
from consts import HEIGHT


class Ship:                                                     
    def __init__(self, x, y, health=1, cool_down=30):
        self.x = x
        self.y = y
        self.health = health
        self.cool_down = cool_down
        self.cool_down_counter = 0                                 #cooldown_time
        self.ship_img = None
        self.laser_img = None
        self.lasers = []                      # data type list

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):              
        self.cooling_down()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 5
                
                
                self.lasers.remove(laser)


    def cooling_down(self):
        if self.cool_down_counter >= self.cool_down:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser_width = self.laser_img.get_width()
            ship_width, ship_height = self.mask.get_size()
            laser = Laser(round(self.x - laser_width / 2 + ship_width / 2), self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
