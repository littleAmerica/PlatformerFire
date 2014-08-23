__author__ = 'blah-blah'

import pygame
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


    move_map = {pygame.K_SPACE: lambda player: Player.jump(player),
                 pygame.K_a: lambda player: Player.move_left(player),
                 pygame.K_d: lambda player: Player.move_right(player)}

    def __init__(self, size=(16, 16), camera=None):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.Surface(self.size)

        self.true_rect = pygame.Rect(0, 0, *self.size)
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
            self.true_rect.clamp_ip(self.bound)

    def shoot(self, to):
        return self.gun.shoot(to)

    @property
    def rect(self):
        if self.camera is not None:
            return self.camera.apply(self.true_rect)
        return self.true_rect

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
        self.true_rect.move_ip(0, self.speed[1])
        for box in self.solid_objects.sprites():
            if self.true_rect.colliderect(box.true_rect):
                if self.speed[1] > 0 and box.true_rect.top < self.true_rect.bottom:
                    self._onGround = True
                    self.true_rect.bottom = box.true_rect.top
                    self.speed[1] = 0
                if self.speed[1] < 0 and box.true_rect.bottom > self.true_rect.top:
                    self.speed[1] = 0
                    self.true_rect.top = box.true_rect.bottom

        if self.true_rect.bottom > self.bound.bottom:
            self.true_rect.bottom = self.bound.bottom
            self.speed[1] = 0
            self._onGround = True

        self.true_rect.move_ip(self.speed[0], 0)
        for box in self.solid_objects.sprites():
            if self.true_rect.colliderect(box.true_rect):
                if self.speed[0] > 0 and self.true_rect.right > box.true_rect.left:
                    self.speed[0] = 0
                    self.true_rect.right = box.true_rect.left
                if self.speed[0] < 0 and box.true_rect.right > self.true_rect.left:
                    self.speed[0] = 0
                    self.true_rect.left = box.true_rect.right

        self.speed[0] = 0