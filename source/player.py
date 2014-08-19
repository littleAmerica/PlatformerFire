__author__ = 'blah-blah'

import pygame
from auxiliary import *
from guns_and_roses import *


G = 1

MAX_SPEED_X = (-15, 15)
MAX_SPEED_Y = (-100, 100)
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

    def __init__(self, size=(16, 16)):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.Surface(self.size)

        self.rect = pygame.Rect(0, 0, *self.size)
        self.bound = None
        self.speed = [0, 0]
        self.move = [0, 0]

        self._onGround = False
        self.image.fill(pygame.Color("#0000ff"))

        self.gun = TestGun(self)


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
            self.rect.clamp_ip(self.bound)


    def shoot(self, to):
        return self.gun.shoot(to)


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
        self.rect.move_ip(0, self.speed[1])
        for box in self.solid_objects.sprites():
            if self.rect.colliderect(box.rect):
                if self.speed[1] > 0 and box.rect.top < self.rect.bottom: #object is fallen
                    self._onGround = True
                    self.rect.bottom = box.rect.top
                    self.speed[1] = 0
                if self.speed[1] < 0 and box.rect.bottom > self.rect.top:
                    self.speed[1] = 0
                    self.rect.top = box.rect.bottom


        self.rect.move_ip(self.speed[0], 0)
        for box in self.solid_objects.sprites():
            if self.rect.colliderect(box.rect):
                if self.speed[0] > 0 and self.rect.right > box.rect.left:
                    self.speed[0] = 0
                    self.rect.right = box.rect.left
                    print "Test"
                if self.speed[0] < 0 and box.rect.right > self.rect.left:
                    self.speed[0] = 0
                    self.rect.left = box.rect.right
                    print "Test"

        self.speed[0] = 0