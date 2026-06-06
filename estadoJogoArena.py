from pygame import Surface
import pygame as pg

from configJogo import ConfigJogo
from cronometroArena import Cronometro 

from telaPrincipal import telaPrincipal

class EstadoJogo:
    def __init__(self):
        self.cronometro = Cronometro()
        self.resetar()

    def resetar(self):
        self.cronometro.reset()

    def fim_de_jogo(self):
        if (self.cronometro.tempo_passando()>ConfigJogo.DURACAO_PARTIDA) or (telaPrincipal.p1Vida == 0) or (telaPrincipal.p2Vida == 0):
            return True 
        else:
            return False 