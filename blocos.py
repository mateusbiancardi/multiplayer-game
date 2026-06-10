import pygame as pg
import os
from configJogo import *

class bloco(pg.sprite.Sprite):

    # mapeia o codigo do bloco no nome do sprite
    SPRITES = {
        8: 'madeira.png',
        5: 'roxo.png',
        0: 'pedra.png',
        9: 'lava.png',
        4: 'branco.png',
        1: 'preto.png',
    }

    def __init__(self, pos, grupos, tipo_png):
        super().__init__(grupos)

        self.tipo_png = tipo_png

        self.image = pg.image.load(os.path.join('sprites', self.SPRITES[tipo_png]))

        # convert_alpha so funciona com modo de video ativo (cliente).
        # No servidor (sem tela) ele e dispensavel: so usamos o rect pra colisao.
        if pg.display.get_surface() is not None:
            self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
