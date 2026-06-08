
import pygame as pg
from configJogo import ConfigJogo
from time import time


class Aguardando:
    def __init__(self, tela):
        self.tela = tela 
        self.encerrada = False

        font_titulo = pg.font.SysFont(None, ConfigJogo.FONTE_TITULO)
        self.titulo = font_titulo.render(
            f'Aguardando outro jogador...', True, ConfigJogo.COR_TITULO)


    def desenha(self):
        self.tela.fill((255, 255, 255))
        self.desenha_titulo(self.tela)
        pg.display.flip()

    def desenha_titulo(self, tela):
        px = ConfigJogo.LARGURA_TELA // 2 - self.titulo.get_size()[0] // 2
        py = (0.2 * ConfigJogo.ALTURA_TELA // 2)
        tela.blit(self.titulo, (px, py))