__author__ = 'matan'

import pygame
from player import Player
from simple_sprite import *
from auxiliary import *
import tile

#Tower like in ice climbers
#TODO Animation - addmodule
#TODO Camera - add module
#TODO Phisics - something goes terrible wrong
#TODO Phisics - events on touching with the screen
#TODO Tiled - adding alpha for surfaces

TILED_FILE = "../tiled/level1.tmx"

class Camera(object):
    def __init__(self, camera_size, level_size):
        self.camera_size = camera_size
        self.state = pygame.Rect((0, 0), camera_size)
        self.level_size = level_size

    def apply(self, target):
        return target.move(self.state.topleft)

    def update(self, target_rect):
        top_left = target_rect.topleft
        #new width = - old  width + camera_width / 2
        new_top_left = add(multiply(top_left, -1), multiply(self.camera_size, 0.5))

        self.state = pygame.Rect(new_top_left, target_rect.size)


class Game(object):

    DISPLAY = (400, 400)
    LEVEL_SIZE = (1600, 320)
    
    keyboard_map = {}

    def __init__(self):
        self.player = None
        self.entities = pygame.sprite.LayeredUpdates()
        self.tiled = tile.get_tiled(TILED_FILE)

        self.camera = Camera(Game.DISPLAY, Game.LEVEL_SIZE)

        for layer in self.tiled:
            if layer.level == "1":
                self.solid = layer.cells
            self.entities.add(layer.cells, layer=layer.level)

        self.init_player()

        for sprite in self.entities.sprites():
            sprite.camera = self.camera


    def init_player(self):
        self.player = Player()
        self.player.bound = pygame.Rect((0, 0), Game.LEVEL_SIZE)

        #make closure action (delay evaluation of method call - when we only need it)
        make_action = lambda obj, method: lambda: method(obj)
        player_map = {key: make_action(self.player, action) for key, action in Player.move_map.items()}

        self.player.solid_objects = self.solid

        Game.keyboard_map = dict_union(Game.keyboard_map, player_map)
        self.player.entities = self.entities
        self.entities.add(self.player)

    def main(self, screen):
        timer = pygame.time.Clock()
        dt = timer.tick(30)

        bullets = pygame.sprite.Group()
        self.entities.add(bullets)

        while True:
            timer.tick(60)
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == constants.LEFT_MOUSE:
                    bullet = self.player.shoot(ev.pos)
                    bullets.add(bullet)
                    self.entities.add(bullet)
                elif ev.button == constants.RIGHT_MOUSE:
                    self.player.jump()

            pressed = pygame.key.get_pressed()

            self.camera.update(self.player._rect)

            for key, action in Game.keyboard_map.items():
                if pressed[key]:
                    action()


            screen.fill(constants.SKY_BLUE)

            self.entities.update(dt / 1000.0)
            self.entities.draw(screen)

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(Game.DISPLAY)
    Game().main(screen)