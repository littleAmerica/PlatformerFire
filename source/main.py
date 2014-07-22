__author__ = 'matan'

import pygame
from Player import Player
#import tmx


#TODO fix the bug with jumping player near the boxes

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
        self.image.fill(pygame.Color("#ff0000"))
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.level = 1

    def update(self, dt):
        pass


class Game(object):
    def main(self, screen):
        timer = pygame.time.Clock()
        dt = timer.tick(30)

        entities = pygame.sprite.Group()
        boxes = pygame.sprite.Group()

        player = Player(entities)
        player.bound = screen.get_rect()
        entities.add(player)

        for i in range(DISPLAY[0]/256):
            box = Box(pos=(32 * i * 8, DISPLAY[1] - 128))
            boxes.add(box)

        boxes.add(Box(pos=(0 , DISPLAY[1] - 32), size=(DISPLAY[0], 32)))
        boxes.add(Box(pos=(128 , DISPLAY[1] - 64), size=(32, 32)))

        entities.add(boxes)
        player.solid_objects = boxes



        while(1):
            timer.tick(60)
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break
            pressed = pygame.key.get_pressed()
            speed = [0, 0]
            if pressed[pygame.K_SPACE]:
                speed[1] = -500 * dt / 1000.0
            if pressed[pygame.K_LEFT]:
                speed[0] = -500 * dt / 1000.0
            if pressed[pygame.K_RIGHT]:
                speed[0] = 500 * dt / 1000.0
            player.set_speed(speed)

            screen.fill(pygame.Color("#000000"))
            entities.update(dt / 1000.0)
            entities.draw(screen)

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    Game().main(screen)