__author__ = 'blah-blah'

import pygame
import constants

class Box(pygame.sprite.Sprite):
    def __init__(self, size=(32, 32), pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(constants.RED)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.level = 1

    def update(self, dt):
        pass
