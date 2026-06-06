import pygame as pg
import os
from configJogo import *

class bloco(pg.sprite.Sprite):
    
    def __init__(self, pos, grupos, tipo_png):
        super().__init__(grupos)
        
        self.tipo_png = tipo_png
        
        if self.tipo_png == 8:
            self.image = pg.image.load(os.path.join('sprites', 'madeira.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft = pos)
        
        elif self.tipo_png == 5:
            self.image = pg.image.load(os.path.join('sprites', 'roxo.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft = pos)

        elif self.tipo_png == 0:
            self.image = pg.image.load(os.path.join('sprites', 'pedra.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft = pos)
        
        elif self.tipo_png == 9:
            self.image = pg.image.load(os.path.join('sprites', 'lava.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft = pos)

        elif self.tipo_png == 4:
            self.image = pg.image.load(os.path.join('sprites', 'branco.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft = pos)

        elif self.tipo_png == 1:
            self.image = pg.image.load(os.path.join('sprites', 'preto.png')).convert_alpha()
            self.rect = self.image.get_rect(topleft = pos)