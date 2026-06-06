
import sys
from typing import Tuple
import pygame as pg
from bola import Bola

from config_jogo import ConfigJogo
from barra import Barra
from estado_jogo import EstadoJogo


class CenaPrincipal:
    def __init__(self, tela):
        self.tela = tela

        py = ConfigJogo.ALTURA_TELA // 2 - ConfigJogo.ALTURA_BARRA // 2
        px_esq = ConfigJogo.POS_X_BARRA_ESQUERDA
        px_dir = ConfigJogo.POS_X_BARRA_DIREITA

        self.barra_esquerda = Barra(posicao=(px_esq, py))
        self.barra_direita = Barra(posicao=(px_dir, py))
        self.bola = Bola()
        self.estado = EstadoJogo()

        self.encerrada = False

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

        # barra da esquerda
        if pg.key.get_pressed()[pg.K_w]:
            self.barra_esquerda.mover_para_cima()
        elif pg.key.get_pressed()[pg.K_s]:
            self.barra_esquerda.mover_para_baixo()
        else:
            self.barra_esquerda.parar()

        # barra da direita
        if pg.key.get_pressed()[pg.K_i]:
            self.barra_direita.mover_para_cima()
        elif pg.key.get_pressed()[pg.K_j]:
            self.barra_direita.mover_para_baixo()
        else:
            self.barra_direita.parar()

    def atualiza_estado(self):
        self.barra_esquerda.atualizar_posicao()
        self.barra_direita.atualizar_posicao()
        self.bola.atualizar_posicao()
        self.trata_goals()
        self.trata_colisao_bola_barra()

        if self.estado.jogo_terminou():
            self.encerrada = True

    def desenha(self):
        self.tela.fill((255, 255, 255))
        self.barra_direita.desenha(self.tela)
        self.barra_esquerda.desenha(self.tela)
        self.bola.desenha(self.tela)
        self.estado.desenha(self.tela)
        pg.display.flip()

    def trata_goals(self):
        if self.bola.posicao[0] < 0:
            self.estado.incrementar_goals_jogador_1()
            self.bola.resetar()
        elif self.bola.posicao[0] >= ConfigJogo.LARGURA_TELA:
            self.estado.incrementar_goals_jogador_2()
            self.bola.resetar()

    def trata_colisao_bola_barra(self):
        colisao_esquerda = self.circ_rect_collision(
            ConfigJogo.RAIO_BOLA,
            self.bola.posicao,
            self.barra_esquerda.rect()
        )

        colisao_direita = self.circ_rect_collision(
            ConfigJogo.RAIO_BOLA,
            self.bola.posicao,
            self.barra_direita.rect()
        )

        if colisao_esquerda or colisao_direita:
            self.bola.velocidade[0] = -self.bola.velocidade[0]

    def circ_rect_collision(self,
                            raio_circulo: float,
                            posicao_circulo: Tuple[float, float],
                            dados_retangulo: Tuple[float, float, float, float]
                            ) -> bool:
        c_px, c_py = posicao_circulo
        r_px, r_py, r_larg, r_alt = dados_retangulo
        DeltaX = c_px - max(r_px, min(c_px, r_px + r_larg))
        DeltaY = c_py - max(r_py, min(c_py, r_py + r_alt))
        return (DeltaX * DeltaX + DeltaY * DeltaY) < (raio_circulo * raio_circulo)
