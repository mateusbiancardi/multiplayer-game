

import sys
import pygame as pg
from cena_principal import CenaPrincipal

from config_jogo import ConfigJogo
from cronometro import Cronometro


class CenaVencedor:
    def __init__(self, tela, cena_principal: CenaPrincipal):
        self.tela = tela
        self.cena_anterior = cena_principal
        self.encerrada = False

        font_titulo = pg.font.SysFont(None, ConfigJogo.FONTE_TITULO)
        font_subtitulo = pg.font.SysFont(None, ConfigJogo.FONTE_SUBTITULO)

        if cena_principal.estado.vencedor() == "Empate":
            self.titulo = font_titulo.render(
                f'Empate', True, ConfigJogo.COR_TITULO)

            self.subtitulo = None

        else:
            self.titulo = font_titulo.render(
                f'Vitória', True, ConfigJogo.COR_TITULO)

            self.subtitulo = font_subtitulo.render(
                cena_principal.estado.vencedor(), True, ConfigJogo.COR_TITULO)

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

        # desenha os objetos como estavam no fim do jogo
        self.cena_anterior.barra_direita.desenha(self.tela)
        self.cena_anterior.barra_esquerda.desenha(self.tela)
        self.cena_anterior.bola.desenha(self.tela)

        self.desenha_titulo(self.tela)
        self.desenha_subtitulo(self.tela)

        pg.display.flip()

    def desenha_titulo(self, tela):
        # desenha o titulo no meio da tela
        px = ConfigJogo.LARGURA_TELA // 2 - self.titulo.get_size()[0] // 2
        py = (0.2 * ConfigJogo.ALTURA_TELA // 2)
        tela.blit(self.titulo, (px, py))

    def desenha_subtitulo(self, tela):
        if (self.mostrar_subtitulo) and (self.subtitulo is not None):
            # desenha o subtitulo centralizado horizontalmente, mas verticalmente
            # abaixo do titulo. Ao somar "self.titulo.get_size()[1] * 1.5" no py,
            # estamos deslocando 1.5x a altura do titulo para baixo.
            px = ConfigJogo.LARGURA_TELA // 2 - \
                self.subtitulo.get_size()[0] // 2
            py = (0.2 * ConfigJogo.ALTURA_TELA // 2) + \
                (self.titulo.get_size()[1] * 1.5)
            tela.blit(self.subtitulo, (px, py))
