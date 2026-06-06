
from typing import Tuple
import pygame as pg

from config_jogo import ConfigJogo


class Barra:
    def __init__(self, posicao):
        self.posicao = posicao
        self.velocidade = 0

    def mover_para_cima(self):
        self.velocidade = -ConfigJogo.VELOCIDADE_BARRAS

    def mover_para_baixo(self):
        self.velocidade = ConfigJogo.VELOCIDADE_BARRAS

    def parar(self):
        self.velocidade = 0

    def atualizar_posicao(self):
        x, y = self.posicao
        novo_y = y + self.velocidade

        if (novo_y >= 0) and \
                ((novo_y + ConfigJogo.ALTURA_BARRA) <= ConfigJogo.ALTURA_TELA):
            self.posicao = (x, novo_y)

    def desenha(self, tela):
        x = self.posicao[0]
        y = self.posicao[1]
        l = ConfigJogo.LARGURA_BARRA
        a = ConfigJogo.ALTURA_BARRA
        pg.draw.rect(
            tela,
            ConfigJogo.COR_BARRA,
            pg.rect.Rect(x, y, l, a)
        )

    def rect(self) -> Tuple[float, float, float, float]:
        """ retorna os dados da barra como os retangulos sao representados 
            no pygame, i.e., como uma tupla do tipo (px, py, largura, altura).
        """
        return self.posicao + (ConfigJogo.LARGURA_BARRA, ConfigJogo.ALTURA_BARRA)
