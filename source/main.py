__author__ = 'matan'

import pygame
from player import Player
from simple_sprite import *
from auxiliary import *
#import tmx

#Tower like in ice climbers
#TODO Animation module
#TODO Parser TMX module

class Game(object):

    DISPLAY = (800, 640)
    
    keyboard_map = {}

    def __init__(self):
        self.entities = pygame.sprite.Group()
    #     layers = parseTMX(tmx_file_name())
    #     enteties = getAllObject(layers)
    #     player = Player(enteties)
    #     player.solid_objects = getTouchable(layers)
    
    def init_player(self):
        self.player = Player(self.entities)

        #make closure action (delay evaluation of method call - when we only need it)
        make_action = lambda object, method: lambda :method(object)
        player_map = {key: make_action(self.player, action) for key, action in Player.move_map.items()}

        Game.keyboard_map = dict_union(Game.keyboard_map, player_map)


    def main(self, screen):
        timer = pygame.time.Clock()
        dt = timer.tick(30)

        self.init_player()

        boxes = pygame.sprite.Group(self.entities)
        bullets = pygame.sprite.Group(self.entities)

        self.player.bound = screen.get_rect()
 #       self.entities.add(player)

        for i in range(Game.DISPLAY[0]//256):
            box = Box(pos=(32 * i * 8, Game.DISPLAY[1] - 128))
            boxes.add(box)

        boxes.add(Box(pos=(0, Game.DISPLAY[1] - 32), size=(Game.DISPLAY[0], 32)))
        boxes.add(Box(pos=(128, Game.DISPLAY[1] - 64), size=(32, 32)))

        self.player.solid_objects = boxes

        self.entities.add(boxes)
        self.entities.add(bullets)

        while True:
            timer.tick(60)
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == constants.LEFT_MOUSE:
                    bullet = self.player.gun.shoot(ev.pos)
                    self.entities.add(bullet)
                elif ev.button == constants.RIGHT_MOUSE:
                    self.player.jump()

            pressed = pygame.key.get_pressed()

            for key, execute in Game.keyboard_map.items():
                if pressed[key]:
                    print key, execute
                    Game.keyboard_map[key]()

            screen.fill(constants.BLACK)
            self.entities.update(dt / 1000.0)
            self.entities.draw(screen)

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(Game.DISPLAY)
    Game().main(screen)