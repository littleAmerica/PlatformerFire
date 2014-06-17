__author__ = 'matan'

import pygame
import operator


DISPLAY = (800, 640)

# key bindings
move_map = {pygame.K_LEFT: [-1, 0],
            pygame.K_RIGHT: [1, 0],
            pygame.K_SPACE: [0, -1],
            }

def Clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)

class Box(pygame.sprite.Sprite):
    def __init__(self, size=(32, 32), pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(pygame.Color("#ff0000"))
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.level = 1

    def update(self, dt):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, *Group):
        pygame.sprite.Sprite.__init__(self, Group)
        self.image = pygame.Surface((32, 32))
        self.size = (32, 32)
        self.rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.bound = None
        self.speed = [0, 0]
        self.max_speed_x = (-15, 15)
        self.max_speed_y = (-100, 100)
        self._onGround = False
        self.slowdownAcceleration = 1
        self.g = 1
        self.image.fill(pygame.Color("#0000ff"))

    def set_speed(self, speed):
        self.set_speed_x(speed[0])
        self.set_speed_y(speed[1])
        self.__clamp_speed()
        self._onGround = False

    def set_speed_x(self, speedX):
        self.speed[0] += speedX

    def set_speed_y(self, speedY):
        if self._onGround and speedY < 0 :
            self.speed[1] = speedY

    def update(self, dt):
        pressed = pygame.key.get_pressed()

        speed = [0, 0]
        if pressed[pygame.K_SPACE]:
            speed[1] = -400 * dt
        if pressed[pygame.K_LEFT]:
            speed[0] = -300 * dt
        if pressed[pygame.K_RIGHT]:
            speed[0] = 300 * dt
        self.set_speed(speed)

        self.__apply_acceleration()
        self.__clamp_speed()
        self.rect.move_ip(self.speed[0], self.speed[1])
        self.__collide(checkX=True, checkY=True)
        if self.bound:
            self.rect.clamp_ip(self.bound)

    def __clamp_speed(self):
        self.speed[0] = max(min(self.speed[0], self.max_speed_x[1]), self.max_speed_x[0])
        self.speed[1] = max(min(self.speed[1], self.max_speed_y[1]), self.max_speed_y[0])

    def __apply_acceleration(self):
        #G
        if not self._onGround:
            self.speed[1] += self.g
        else:
            self.speed[1] = 0

        if self.speed[0] < 0:
            self.speed[0] += self.slowdownAcceleration * 1
        elif self.speed[0] > 0:
            self.speed[0] += self.slowdownAcceleration * -1


    def __collide(self, checkX=False, checkY=False):
        if checkY:
            for box in self.solid_objects.sprites():
                if pygame.sprite.collide_rect(self, box):
                    if self.speed[1] > 0 and box.rect.top < self.rect.bottom: #object is fallen
                        self._onGround = True
                        self.rect.bottom = box.rect.top
                        self.speed[1] = 0
                        break
                    if self.speed[1] < 0 and box.rect.bottom > self.rect.top:
                        self.rect.top = box.rect.bottom
                        self.speed[1] = 0
                        break
        if checkX:
            for box in self.solid_objects.sprites():
               if pygame.sprite.collide_rect(self, box):
                    if self.speed[0] > 0 and self.rect.right > box.rect.left:
                        self.speed[0] = 0
                        self.rect.right = box.rect.left
                        break
                    if self.speed[0] < 0 and box.rect.right > self.rect.left:
                        self.speed[0] = 0
                        self.rect.left = box.rect.right
                        break


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

            screen.fill(pygame.Color("#000000"))
            entities.update(dt / 1000.0)
            entities.draw(screen)

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    Game().main(screen)