

import random
from pygame import Surface
import pygame
from barra import Barra
from config_jogo import ConfigJogo


class Bola:
    def __init__(self):
        self.resetar()

    def resetar(self):
        px = ConfigJogo.LARGURA_TELA // 2
        py = ConfigJogo.ALTURA_TELA // 2
        self.posicao = [px, py]
        self.atribuir_velocidade_aleatoria()

    def verifica_e_trata_colisao_barra(self, barra: Barra):
        pass

    def atribuir_velocidade_aleatoria(self):
        v = ConfigJogo.VELOCIDADE_BOLA
        vx = random.choice([-v, v])
        vy = random.choice([-v, v])
        self.velocidade = [vx, vy]

    def atualizar_posicao(self):
        # posicao em x eh sempre atualizada porque posicoes
        # invalidas viram goals e isso eh tratado depois no
        # jogo.
        self.posicao[0] = self.posicao[0] + self.velocidade[0]

        # posicao y so' eh atualizada se posicao destino for valida
        novo_y = self.posicao[1] + self.velocidade[1]

        if (novo_y >= 0) and (novo_y <= ConfigJogo.ALTURA_TELA):
            self.posicao[1] = novo_y
        else:
            self.velocidade[1] = -self.velocidade[1]

    def desenha(self, tela: Surface):
        pygame.draw.circle(tela, ConfigJogo.COR_BOLA,
                           self.posicao, ConfigJogo.RAIO_BOLA)
