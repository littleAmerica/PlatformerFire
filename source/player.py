__author__ = 'blah-blah'

import pygame
from auxiliary import *
from guns_and_roses import *


G = 1

MAX_SPEED_X = (-15, 15)
MAX_SPEED_Y = (-100, 20)
PLAYER_SPEED = 6
PLAYER_JUMP = -10


PLAYER_SLOW_ACCELERATION = 1
PLAYER_SPEED_ACCELERATION = 2
PLAYER_JUMP_ACCELERATION = 8

class Player(pygame.sprite.Sprite):

    move_map = {
                pygame.K_SPACE: lambda player: Player.jump(player),
                pygame.K_a: lambda player: Player.move_left(player),
                pygame.K_d: lambda player: Player.move_right(player),
                }

    def __init__(self, size=(16, 16), camera=None):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.Surface(self.size)

        self._rect = pygame.Rect(0, 0, *self.size)
        self.bound = None
        self.speed = [0, 0]
        self.move = [0, 0]

        self._onGround = False
        self.image.fill(pygame.Color("#0000ff"))

        self.gun = TestGun(self)
        self.camera = camera


    def move_right(self):
        self.speed[0] = PLAYER_SPEED
        self._onGround = False


    def move_left(self):
        self.speed[0] = -PLAYER_SPEED
        self._onGround = False


    def jump(self):
        if self._onGround:
            if self.speed[1] == 0:
                self.speed[1] = PLAYER_JUMP
            self._onGround = False


    def update(self, dt):
        self._move_rect()
        self.__apply_speed()

        if self.bound:
            self._rect.clamp_ip(self.bound)


    def shoot(self, to):
        return self.gun.shoot(to)

    @property
    def rect(self):
        if self.camera is not None:
            return self.camera.apply(self._rect)
        return self._rect

    def __apply_speed(self):

        # apply slowdown acceleration + G
        if not self._onGround:
            self.speed[1] += G
        self.__clamp_speed()

    def __clamp_speed(self):
        self.speed[0] = clamp(self.speed[0], *MAX_SPEED_X)
        self.speed[1] = clamp(self.speed[1], *MAX_SPEED_Y)


    def _move_rect(self):
        """
            Moving a player with taking in account of solid objects
        """
        self._rect.move_ip(0, self.speed[1])
        for box in self.solid_objects.sprites():
            if self._rect.colliderect(box._rect):
                if self.speed[1] > 0 and box._rect.top < self._rect.bottom: #object is fallen
                    self._onGround = True
                    self._rect.bottom = box._rect.top
                    self.speed[1] = 0
                if self.speed[1] < 0 and box._rect.bottom > self._rect.top:
                    self.speed[1] = 0
                    self._rect.top = box._rect.bottom

        # if self._rect.bottom > self.bound.bottom:
        #     self._rect.bottom = self.bound.bottom
        #     self.speed[1] = 0
        #     self._onGround = True


        self._rect.move_ip(self.speed[0], 0)
        for box in self.solid_objects.sprites():
            if self._rect.colliderect(box._rect):
                if self.speed[0] > 0 and self._rect.right > box._rect.left:
                    self.speed[0] = 0
                    self._rect.right = box._rect.left
                if self.speed[0] < 0 and box._rect.right > self._rect.left:
                    self.speed[0] = 0
                    self._rect.left = box._rect.right

        self.speed[0] = 0