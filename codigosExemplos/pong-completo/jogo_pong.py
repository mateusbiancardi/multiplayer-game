
from enum import Enum
import pygame as pg
from cena_inicial import CenaInicial
from cena_principal import CenaPrincipal
from cena_vencedor import CenaVencedor

from config_jogo import ConfigJogo


class NomeCena(Enum):
    """ Enums servem para dar nomes legiveis para valores """
    INICIAL = 0
    PRINCIPAL = 1
    FIM_PARTIDA = 2


class JogoPong:
    def __init__(self):
        pg.init()

        self.tela = pg.display.set_mode((
            ConfigJogo.LARGURA_TELA,
            ConfigJogo.ALTURA_TELA
        ))

    def rodar(self):
        # cria a cena inicial
        cena = CenaInicial(self.tela)
        # fica na cena ate o usuario pressionar enter
        cena.rodar()

        # fica infinitamente rodando uma partida e
        # ao final mostrando o vencedor
        while True:
            # cria a cena principal do jogo
            cena_principal = CenaPrincipal(self.tela)
            # roda a cena ate' um dos jogadores ganhar ou
            # chegar ao fim do jogo
            cena_principal.rodar()

            # cria a cena final do jogo
            cena_final = CenaVencedor(self.tela, cena_principal)
            # fica na tela ate' o usuario digitar espaco
            cena_final.rodar()