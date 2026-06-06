import pygame as pg
from telaInicial import Menu
from configJogo import ConfigJogo
from selecaoPersonagem import telaSelecao
from telaPrincipal import telaPrincipal
from telaFinal import telaFinal

class JogoArena():
    def __init__(self):
        pg.init()

        self.tela = pg.display.set_mode((
            ConfigJogo.LARGURA_TELA, 
            ConfigJogo.ALTURA_TELA
        ))

    def rodar(self):
        cena = Menu(self.tela)
        cena.rodar()

        
        while True:
            selecao = telaSelecao(self.tela)
            personagens = selecao.rodar()
            telaPrincipalRodando = telaPrincipal(self.tela, personagens)
            vidaPersonagens = telaPrincipalRodando.rodar()
            telaFinalRodando = telaFinal(self.tela, vidaPersonagens[0], vidaPersonagens[1])
            telaFinalRodando.rodar_final()