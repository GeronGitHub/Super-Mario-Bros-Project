import pygame


class Tunnel(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics/greenpipe64.png')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.coins = []
        for i in range(0, 16):
            pathname = 'graphics/coin/coin' + str(i) + '.png'
            image = pygame.image.load(pathname)
            self.coins.append(image)

        self.current_coin = 0
        self.image = self.coins[self.current_coin]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift

        self.current_coin += 0.4
        if int(self.current_coin) >= len(self.coins):
            self.current_coin = 0
            self.is_animating = False

        self.image = self.coins[int(self.current_coin)]
