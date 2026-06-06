import math
import random
import sys
import pygame as pg
from configJogo import ConfigJogo
from time import time



class Cronometro:
    def __init__(self):
        self.reset()

    def reset(self):
        self.tempo_referencia = time()

    def tempo_passando(self):
        tempo_atual = time()
        return tempo_atual - self.tempo_referencia

class Menu:
    def __init__(self, tela):
        self.tela = tela 
        self.encerrada = False

        font_titulo = pg.font.SysFont(None, ConfigJogo.FONTE_TITULO)
        font_subtitulo = pg.font.SysFont(None, ConfigJogo.FONTE_SUBTITULO)
        self.titulo = font_titulo.render(
            f'Arena Medieval', True, ConfigJogo.COR_TITULO)
        self.subtitulo = font_subtitulo.render(
            f'Pressione espaço para iniciar', True, ConfigJogo.COR_TITULO)

        self.cronometro = Cronometro()
        self.mostrar_subtitulo = True

    def rodar(self):
        while not self.encerrada:
            self.eventos()
            self.atualiza_estado()
            self.desenha()

    def eventos(self):
        pg.event.get()
        
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            sys.exit(0)

        if pg.key.get_pressed()[pg.K_SPACE]:
            self.encerrada = True

    def atualiza_estado(self):
        if self.cronometro.tempo_passando() > 0.5:
            self.mostrar_subtitulo = not self.mostrar_subtitulo
            self.cronometro.reset()

    def desenha(self):
        self.tela.fill((255, 255, 255))
        self.desenha_titulo(self.tela)
        self.desenha_subtitulo(self.tela)
        pg.display.flip()

    def desenha_titulo(self, tela):
        px = ConfigJogo.LARGURA_TELA // 2 - self.titulo.get_size()[0] // 2
        py = (0.2 * ConfigJogo.ALTURA_TELA // 2)
        tela.blit(self.titulo, (px, py))

    def desenha_subtitulo(self, tela):
        if self.mostrar_subtitulo:
            px = ConfigJogo.LARGURA_TELA // 2 - \
                self.subtitulo.get_size()[0] // 2
            py = (0.2 * ConfigJogo.ALTURA_TELA // 2) + \
                (self.titulo.get_size()[1] * 1.5)
            tela.blit(self.subtitulo, (px, py))