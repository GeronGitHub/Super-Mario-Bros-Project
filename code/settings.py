import pygame

level_map = [

    '                      V                WW                              X',
    '                                          D                            X',
    '                           D         D                                 X',
    '                      G         D                                      X',
    '                    WWWW                                               X',
    '                             D                                         X',
    '                  GDD  DD                     B                        X',
    '                 DDXX  XXDD          WWWW  B          B                X',
    '         B      DXXXX  XXXXD    B    BBBB         B          V         X',
    '               DXXXXX  XXXXXD                                          X',
    'X    P   G  T DXXXXXX  XXXXXXD   T   G   G   T G      TT               X',
    'DDDDDDDDDDDDDDXXXXXXX  XXXXXXXDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDX'
]


tile_size = 50

screen_width = 1000
screen_height = 640  # len(level_map) * tile_size #500
FPS = 60


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('ULTRA MARIO BROS.')
