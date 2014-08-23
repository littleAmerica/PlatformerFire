__author__ = 'blah-blah'

import pygame
import constants

class Box(pygame.sprite.Sprite):
    def __init__(self, image, pos=(0, 0), camera=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.size = image.get_size()
        self._rect = pygame.Rect(self.pos, self.size)
        self.level = 1


    def update(self, dt):
        pass





class Cell(pygame.sprite.Sprite):
    def __init__(self, image, pos=(0, 0), camera=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.size = image.get_size()
        self.pos = pos
        self.true_rect = pygame.Rect(self.pos, self.size)
        self.camera = camera

    def update(self, dt):
        pass


    @property
    def rect(self):
        if self.camera is not None:
            return self.camera.apply(self.true_rect)
        return self.true_rect