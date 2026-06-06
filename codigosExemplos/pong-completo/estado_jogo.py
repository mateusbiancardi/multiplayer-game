

from pygame import Surface
import pygame

from config_jogo import ConfigJogo
from cronometro import Cronometro


class EstadoJogo:
    def __init__(self):
        # salvamos a fonte para nao precisar criar ela toda hora
        self.font = pygame.font.SysFont(None, 24)
        # cronometro para medir o tempo de jogo
        self.cronometro = Cronometro()
        # reinicia o numero de goals e o tempo.
        self.resetar()

    def resetar(self):
        self.goals_jogador_1 = 0
        self.goals_jogador_2 = 0
        self.cronometro.reset()

    def incrementar_goals_jogador_1(self):
        self.goals_jogador_1 += 1

    def incrementar_goals_jogador_2(self):
        self.goals_jogador_2 += 1

    def jogo_terminou(self):
        if (self.goals_jogador_1 >= 10) or \
            (self.goals_jogador_2 >= 10) or \
                (self.cronometro.tempo_passado() > ConfigJogo.DURACAO_PARTIDA):
            return True
        else:
            return False

    def vencedor(self):
        if self.goals_jogador_1 > self.goals_jogador_2:
            return "Jogador 1"
        elif self.goals_jogador_2 > self.goals_jogador_1:
            return "Jogador 2"
        else:
            return "Empate"

    def desenha(self, tela: Surface):
        self.desenha_placar(tela)
        self.desenha_tempo(tela)

    def desenha_placar(self, tela: Surface):
        g1 = self.goals_jogador_1
        g2 = self.goals_jogador_2
        img = self.font.render(f'{g1} x {g2}', True, ConfigJogo.COR_ESTADO)
        px = ConfigJogo.LARGURA_TELA // 2 - img.get_size()[0] // 2
        py = ConfigJogo.ALTURA_PLACAR
        tela.blit(img, (px, py))

    def desenha_tempo(self, tela: Surface):
        tempo = ConfigJogo.DURACAO_PARTIDA - self.cronometro.tempo_passado()
        img = self.font.render(f'{tempo:.0f}',
                               True, ConfigJogo.COR_ESTADO)
        px = ConfigJogo.LARGURA_TELA // 2 - img.get_size()[0] // 2
        py = ConfigJogo.ALTURA_TEMPO
        tela.blit(img, (px, py))
