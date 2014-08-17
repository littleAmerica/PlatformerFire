__author__ = 'dmytro.poberezhnyi'

import pygame
import constants
from auxiliary import *

class TestGun():
    def __init__(self, owner):
        self.owner = owner
        self.bullet_speed = (100, 100)
        self.max_bullet_range = 250

    def shoot(self, to):
        bullet = Bullet(pos=self.get_pos())
        bullet_direction = normalize(sub(to, self.get_pos()))
        bullet.speed = multiply(self.bullet_speed, bullet_direction)
        bullet.max_passed_way = self.max_bullet_range
        return bullet

    def get_pos(self):
        return self.owner.rect.center


class Bullet(pygame.sprite.Sprite):
    def __init__(self, size=(4, 4), pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(constants.GREEN)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.size = size
        self.origin_center = self.rect.center

        self.speed = (0, 0)
        self.age = 0

    def update(self, dt):
        #getting older
        self.age += dt

        self.passed_way = multiplybyNumber(self.speed, self.age)
        self.rect.center = add(self.origin_center, self.passed_way)

        if not self.if_alive():
            self.kill()

    def if_alive(self):
        """
        Check if the bullet still exists. Otherwise we should remove it from the drawing group

         There can be several ways to stop the bullets.
         It can smash into another object or it can have limited time or radius of moving
        """
        return magnitude(self.passed_way) < self.max_passed_way

       #  if not self.rect.colliderect(self.bound):
       #      #well if the object leave the object it should be remove
       # #     self.kill()
