from cgitb import text
from turtle import speed
import pygame
import sys
from settings import *
from level import Level
from soundeffects import *
from UI import *
from tiles import Enemy


pygame.mixer.Sound.play(backgroundmusic)
clock = pygame.time.Clock()
level_1 = Level(level_map, screen)


background = pygame.image.load(
    'graphics/skybackground.jpg')
backgroundscale = pygame.transform.scale(background, (1000, 640))

run = True
while run:
    screen.blit(backgroundscale, (0, 0))
    pygame.mouse.set_visible(False)
    level_1.run()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
