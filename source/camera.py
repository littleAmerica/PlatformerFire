from auxiliary import add, multiply
import pygame


class Camera(object):
    def __init__(self, camera_size, bound=None):
        self.camera_size = camera_size
        self.camera_rect = pygame.Rect((0, 0), camera_size)
        self.bound = bound

    def apply(self, target):
        return target.move(multiply(self.camera_rect.topleft, -1))

    def update(self, target_rect):

        camera_top_left = add(target_rect.topleft, multiply(self.camera_size, -0.5))
        self.camera_rect.topleft = camera_top_left

        if self.bound is not None:
            self.camera_rect.clamp_ip(self.bound)
