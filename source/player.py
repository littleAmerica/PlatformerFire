__author__ = 'blah-blah'

import pygame
from auxiliary import *
from guns_and_roses import *




class Player(pygame.sprite.Sprite):

    move_map = {
                pygame.K_SPACE: lambda player: Player.jump(player),
                pygame.K_a: lambda player: Player.move_left(player),
                pygame.K_d: lambda player: Player.move_right(player),
                }

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

        self.gun = TestGun(self)

    def move_right(self):
        self.speed[0] += 10
        self._onGround = False

    def move_left(self):
        self.speed[0] -= 10
        self._onGround = False

    def jump(self):
        if self._onGround:
            self.speed[1] = -30
            self._onGround = False

    def update(self, dt):
        self.__apply_acceleration()
        self.__clamp_speed()
        self.__collide()
        self.rect.move_ip(*self.speed)
        if self.bound:
            self.rect.clamp_ip(self.bound)

    def __clamp_speed(self):
        self.speed[0] = clamp(self.speed[0], *self.max_speed_x)
        self.speed[1] = clamp(self.speed[1], *self.max_speed_y)

    def __apply_acceleration(self):
        #G
        if not self._onGround:
            self.speed[1] += self.g

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
                    self.rect.bottom = box.rect.top
                    self.speed[1] = 0
                if self.speed[1] < 0 and box.rect.bottom > temp_rect.top:
                    self.speed[1] = 0
                    self.rect.top = box.rect.bottom

        temp_rect = self.rect.move(self.speed[0], 0)
        for box in self.solid_objects.sprites():
            if temp_rect.colliderect(box.rect):
                if self.speed[0] > 0 and temp_rect.right > box.rect.left:
                    self.speed[0] = 0
                    self.rect.right = box.rect.left
                if self.speed[0] < 0 and box.rect.right > temp_rect.left:
                    self.speed[0] = 0
                    self.rect.left = box.rect.right