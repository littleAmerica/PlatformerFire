__author__ = 'matan'

import pygame
from Player import Player
import constants
from auxiliary import *
#import tmx

LEFT_MOUSE = 1
RIGHT_MOUSE = 3

#Tower like in ice climbers

DISPLAY = (800, 640)

# key bindings
move_map = {pygame.K_LEFT: [-1, 0],
            pygame.K_RIGHT: [1, 0],
            pygame.K_SPACE: [0, -1],
            }



class Box(pygame.sprite.Sprite):
    def __init__(self, size=(32, 32), pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(constants.RED)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.level = 1

    def update(self, dt):
        pass


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

    @classmethod
    def from_mouse_even(cls, gun, mouse_even):
        bullet = Bullet(pos=gun.get_pos())

        mouse_pos = mouse_even.pos
        bullet_direction = normalize(sub(mouse_pos, gun.get_pos()))

        bullet.speed = multiply(gun.bullet_speed, bullet_direction)
        return bullet

    def update(self, dt):
        #getting older
        self.age += dt

        general_passed_way = multiplybyNumber(self.speed, self.age)
        self.rect.center = add(self.origin_center, general_passed_way)

        print(self.rect)

      #  if not self.rect.colliderect(self.bound):
            #well if the object leave the object it should be remove
       #     self.kill()


class Game(object):
    def main(self, screen):
        timer = pygame.time.Clock()
        dt = timer.tick(30)

        entities = pygame.sprite.Group()
        boxes = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player(entities)
        player.bound = screen.get_rect()
 #       entities.add(player)

        for i in range(DISPLAY[0]//256):
            box = Box(pos=(32 * i * 8, DISPLAY[1] - 128))
            boxes.add(box)

        boxes.add(Box(pos=(0, DISPLAY[1] - 32), size=(DISPLAY[0], 32)))
        boxes.add(Box(pos=(128, DISPLAY[1] - 64), size=(32, 32)))

        entities.add(boxes)
        entities.add(bullets)

        player.solid_objects = boxes

        while True:
            timer.tick(60)
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == LEFT_MOUSE:
                    entities.add(Bullet.from_mouse_even(player.gun, ev))
                elif ev.button == RIGHT_MOUSE:
                    jump = -500 * dt / 1000.0
                    player.set_speed_y(jump)

            pressed = pygame.key.get_pressed()
            speed = [0, 0]
            if pressed[pygame.K_LEFT]:
                speed[0] = -500 * dt / 1000.0
            if pressed[pygame.K_RIGHT]:
                speed[0] = 500 * dt / 1000.0
            player.set_speed(speed)

            screen.fill(constants.BLACK)
            entities.update(dt / 1000.0)
            entities.draw(screen)

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    Game().main(screen)