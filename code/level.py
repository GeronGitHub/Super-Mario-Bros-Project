from cmath import rect
import sys
from turtle import speed, width
import pygame
from tiles import Enemy
from tunnel import Tunnel
from tiles import Tile
from tunnel import Tunnel, Coin
from settings import *
from player import Player
import time
from soundeffects import *

COLLISION_TOLERANCE = 40


class Level:
    def __init__(self, level_data, surface):

        # level setup
        self.display_surface = surface
        self.setup_level(level_data)

        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.tunnels = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.victory = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.block = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * 49
                y = row_index * tile_size

                if cell == 'D':
                    tile = Tile((x, y + 63), 'grassblock50.png')
                    self.tiles.add(tile)

                if cell == 'X':
                    tile = Tile((x, y + 63), 'dirtblock50.png')
                    self.tiles.add(tile)

                if cell == 'T':
                    tile = Tunnel((x, y + 50))
                    self.tunnels.add(tile)

                if cell == 'B':
                    tile = Tile((x, y), 'block.png')
                    self.block.add(tile)
                    self.tiles.add(tile)

                if cell == 'P':
                    playersprite = Player((x, y))
                    self.player.add(playersprite)

                if cell == 'G':
                    enemy = Enemy((x, y + 73), 'goomba (2).png')
                    self.enemies.add(enemy)

                if cell == 'W':
                    tile = Coin((x, y))
                    self.coins.add(tile)

                if cell == 'V':
                    tile = Coin((x, y))
                    self.victory.add(tile)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < 400 and direction_x < 0:
            self.world_shift = 3
            player.speed = 0
        elif player_x > 600 and direction_x > 0:
            self.world_shift = -3
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 3

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.addgravity()

        if player.rect.y > screen_height + 50:
            print("YOU LOST")
            pygame.QUIT()

        # tile collision
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.direction.y = 2
                    player.rect.top = sprite.rect.bottom
            # BLOCK COLLISION FROM UNDERNEATH
            for sprite in self.block.sprites():
                if sprite.rect.colliderect(player.rect):
                    if (sprite.rect.bottom - player.rect.top) < COLLISION_TOLERANCE:
                        pygame.mixer.Sound.play(bumpblock)
                        sprite.kill()

        # tunnels collision
        for sprite in self.tunnels.sprites():
            if sprite.rect.colliderect(player.rect):
                pygame.mixer.Sound.stop(backgroundmusic)
                pygame.mixer.Sound.stop(mariojump)
                pygame.mixer.Sound.play(mariodies)
                time.sleep(4)
                pygame.QUIT()

    def standard_collision(self):
        player = self.player.sprite

        # COINS COLLISION
        for sprite in self.coins.sprites():
            if sprite.rect.colliderect(player.rect):
                pygame.mixer.Sound.stop(coincollect)
                pygame.mixer.Sound.play(coincollect)
                sprite.kill()

        # WIN COIN COLLISION
        for sprite in self.victory.sprites():
            if sprite.rect.colliderect(player.rect):
                pygame.mixer.Sound.play(coincollect)
                sprite.kill()
                print("YOU WON !")
                pygame.QUIT()

        # GOOMBA STOMP COLLISION
        for sprite in self.enemies.sprites():
            Enemy.addgravity(sprite)
            Enemy.healthbar(sprite, sprite.rect.x - 4, sprite.rect.y - 20)

            if sprite.rect.colliderect(player.rect):
                if (player.rect.bottom - sprite.rect.top) < COLLISION_TOLERANCE:
                    pygame.mixer.Sound.play(stompsound)
                    player.direction.y = -10
                    Enemy.hit(sprite)

                else:
                    pygame.mixer.Sound.stop(backgroundmusic)
                    pygame.mixer.Sound.play(mariodies)
                    time.sleep(4)
                    pygame.QUIT()

    def goombaVerticalCollision(self):

        for goomba in self.enemies.sprites():
            for tile in self.tiles.sprites():
                if goomba.rect.colliderect(tile.rect):
                    if goomba.direction.y > 0:
                        if (goomba.rect.bottom - tile.rect.top) < 5:
                            goomba.rect.bottom = tile.rect.top
                            goomba.direction.y = 0

    def goombaHorizontalCollision(self):
        for goomba in self.enemies.sprites():
            for tile in self.tiles.sprites():
                if goomba.rect.colliderect(tile.rect):
                    if goomba.direction.x > 0:
                        goomba.direction.x = -2
                    elif goomba.direction.x < 0:
                        goomba.direction.x = 2
            for tunnel in self.tunnels.sprites():
                if goomba.rect.colliderect(tunnel.rect):
                    if goomba.direction.x > 0:
                        goomba.direction.x = -2
                    elif goomba.direction.x < 0:
                        goomba.direction.x = 2

    def run(self):

        # YOUWINCOIN
        self.victory.update(self.world_shift)
        self.victory.draw(self.display_surface)

        # level coins
        self.coins.update(self.world_shift)
        self.coins.draw(self.display_surface)

        # level tunnels
        self.tunnels.update(self.world_shift)
        self.tunnels.draw(self.display_surface)

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        # level enemies
        self.enemies.update(self.world_shift)
        self.enemies.draw(self.display_surface)

        self.scroll_x()
        self.player.update(0.4)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.standard_collision()
        self.player.draw(self.display_surface)
        self.goombaVerticalCollision()
        self.goombaHorizontalCollision()
