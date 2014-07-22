__author__ = 'blah-blah'

import pygame

def Clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)

class Player(pygame.sprite.Sprite):
    def __init__(self, *Group):
        pygame.sprite.Sprite.__init__(self, Group)
        self.image = pygame.Surface((32, 32))
        self.size = (32, 32)
        self.rect = pygame.Rect(0, 0, *self.size)
        self.bound = None
        self.speed = [0, 0]
        self.max_speed_x = (-15, 15)
        self.max_speed_y = (-100, 100)
        self._onGround = False
        self.slowdownAcceleration = 1
        self.g = 1
        self.image.fill(pygame.Color("#0000ff"))

    def set_speed(self, speed):
        self.set_speed_x(speed[0])
        self.set_speed_y(speed[1])
        self.__clamp_speed()
        self._onGround = False

    def set_speed_x(self, speedX):
        self.speed[0] = +speedX

    def set_speed_y(self, speedY):
        if self._onGround and speedY < 0 :
            self.speed[1] = speedY

    def update(self, dt):
        self.__apply_acceleration()
        self.__clamp_speed()
        self.__collide()
        self.rect.move_ip(*self.speed)
        if self.bound:
            self.rect.clamp_ip(self.bound)

    def __clamp_speed(self):
        self.speed[0] = Clamp(self.speed[0], *self.max_speed_x)
        self.speed[1] = Clamp(self.speed[1], *self.max_speed_y)

    def __apply_acceleration(self):
        #G
        if not self._onGround:
            self.speed[1] += self.g
        else:
            self.speed[1] = 0

        if self.speed[0] < 0:
            self.speed[0] += self.slowdownAcceleration * 1
        elif self.speed[0] > 0:
            self.speed[0] += self.slowdownAcceleration * -1


    def __collide(self):
        temp_rect = self.rect.move(0, self.speed[1])
        for box in self.solid_objects.sprites():
            if temp_rect.colliderect(box.rect):
                if self.speed[1] > 0 and box.rect.top < temp_rect.bottom: #object is fallen
                    self._onGround = True
                    self.speed[1] = 0
                if self.speed[1] < 0 and box.rect.bottom > temp_rect.top:
                    self.speed[1] = 0

        temp_rect = self.rect.move(self.speed[0], 0)
        for box in self.solid_objects.sprites():
           if temp_rect.colliderect(box.rect):
                if self.speed[0] > 0 and temp_rect.right > box.rect.left:
                    self.speed[0] = 0
                if self.speed[0] < 0 and box.rect.right > temp_rect.left:
                    self.speed[0] = 0

