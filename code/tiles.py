from cmath import rect
import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, char_file):
        super().__init__()
        self.image = pygame.image.load('graphics/' + char_file)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, char_file):
        super().__init__()
        self.image = pygame.image.load('graphics/' + char_file)
        self.rect = self.image.get_rect(topleft=pos)

        self.health = 50
        self.direction = pygame.math.Vector2(0, 0)
        self.direction.x = 2
        self.gravity = 0.3

    def addgravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self, x_shift):
        self.rect.x += x_shift + self.direction.x

    def healthbar(self, pos_x, pos_y):
        pygame.draw.rect(screen, (255, 0, 0), (pos_x, pos_y, 50, 3))
        pygame.draw.rect(screen, (0, 200, 0), (pos_x, pos_y, self.health, 3))
        if self.health <= 0:
            Enemy.kill(self)

    def hit(self):
        if self.health > 0:
            self.health -= 25
