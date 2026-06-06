

import sys
import pygame as pg
from bola import Bola

from config_jogo import ConfigJogo
from barra import Barra
from cronometro import Cronometro


class CenaInicial:
    def __init__(self, tela):
        self.tela = tela
        self.encerrada = False

        # cria os objetos do jogo so' para compor o design da tela inicial
        py = ConfigJogo.ALTURA_TELA // 2 - ConfigJogo.ALTURA_BARRA // 2
        px_esq = ConfigJogo.POS_X_BARRA_ESQUERDA
        px_dir = ConfigJogo.POS_X_BARRA_DIREITA
        self.barra_esquerda = Barra(posicao=(px_esq, py))
        self.barra_direita = Barra(posicao=(px_dir, py))
        self.bola = Bola()

        # cria os textos que serao mostrados na tela
        font_titulo = pg.font.SysFont(None, ConfigJogo.FONTE_TITULO)
        font_subtitulo = pg.font.SysFont(None, ConfigJogo.FONTE_SUBTITULO)
        self.titulo = font_titulo.render(
            f'Jogo de Pong', True, ConfigJogo.COR_TITULO)
        self.subtitulo = font_subtitulo.render(
            f'Pressione Espaço para Iniciar', True, ConfigJogo.COR_TITULO)

        # variaveis usadas para fazer o subtitulo piscar
        self.cronometro = Cronometro()
        self.mostrar_subtitulo = True

    def rodar(self):
        while not self.encerrada:
            self.tratamento_eventos()
            self.atualiza_estado()
            self.desenha()

    def tratamento_eventos(self):
        pg.event.get()

        # evento de saida
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            sys.exit(0)

        # evento de prosseguimento
        if pg.key.get_pressed()[pg.K_SPACE]:
            self.encerrada = True

    def atualiza_estado(self):
        if self.cronometro.tempo_passado() > 0.1:
            self.mostrar_subtitulo = not self.mostrar_subtitulo
            self.cronometro.reset()

    def desenha(self):
        self.tela.fill((255, 255, 255))
        self.barra_direita.desenha(self.tela)
        self.barra_esquerda.desenha(self.tela)
        self.bola.desenha(self.tela)
        self.desenha_titulo(self.tela)
        self.desenha_subtitulo(self.tela)
        pg.display.flip()

    def desenha_titulo(self, tela):
        # desenha o titulo no meio da tela
        px = ConfigJogo.LARGURA_TELA // 2 - self.titulo.get_size()[0] // 2
        py = (0.2 * ConfigJogo.ALTURA_TELA // 2)
        tela.blit(self.titulo, (px, py))

    def desenha_subtitulo(self, tela):
        if self.mostrar_subtitulo:
            # desenha o subtitulo centralizado horizontalmente, mas verticalmente
            # abaixo do titulo. Ao somar "self.titulo.get_size()[1] * 1.5" no py,
            # estamos deslocando 1.5x a altura do titulo para baixo.
            px = ConfigJogo.LARGURA_TELA // 2 - \
                self.subtitulo.get_size()[0] // 2
            py = (0.2 * ConfigJogo.ALTURA_TELA // 2) + \
                (self.titulo.get_size()[1] * 1.5)
            tela.blit(self.subtitulo, (px, py))
