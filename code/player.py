from email.mime import image
from time import time
from turtle import update
import pygame
from settings import *
from random import randint
from tiles import Tile
import time
from soundeffects import *


class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.sprites = []
        for i in range(0, 12):
            pathname = 'graphics/sprites/characters/idle' + str(i) + '.png'
            image = pygame.image.load(pathname)
            scale = pygame.transform.scale(image, (25, 45))
            self.sprites.append(scale)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 3
        self.gravity = 0.3
        self.jump_speed = -10

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.sprites = []
            for i in range(0, 8):

                pathname = 'graphics/sprites/characters/running' + \
                    str(i) + '.png'
                image = pygame.image.load(pathname)
                scale = pygame.transform.scale(image, (25, 45))
                self.sprites.append(scale)
            self.is_animating = False

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.sprites = []
            for i in range(0, 8):

                pathname = 'graphics/sprites/characters/running' + \
                    str(i) + '.png'
                fimage = pygame.image.load(pathname)
                fimage = pygame.transform.flip(fimage, True, False)
                scale = pygame.transform.scale(fimage, (25, 45))
                self.sprites.append(scale)

        else:
            self.direction.x = 0
            self.sprites = []
            for i in range(0, 12):
                pathname = 'graphics/sprites/characters/idle' + \
                    str(i) + '.png'
                image = pygame.image.load(pathname)
                scale = pygame.transform.scale(image, (25, 45))
                self.sprites.append(scale)
        if keys[pygame.K_SPACE]:
            self.sprites = []
            image = pygame.image.load(
                'graphics/sprites/characters/jump0.png')
            scale = pygame.transform.scale(image, (25, 45))
            self.sprites.append(scale)
            if self.direction.y == 0:
                self.jump()
                pygame.mixer.Sound.play(mariojump)

    def addgravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self, speed):
        self.get_input()
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
            self.is_animating = False

        self.image = self.sprites[int(self.current_sprite)]
