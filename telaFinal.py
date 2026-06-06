import pygame as pg
import sys
from telaPrincipal import telaPrincipal
from configJogo import ConfigJogo

class telaFinal:
    def __init__(self, tela_f, p1Vida, p2Vida):
        self.tela_f = tela_f
        self.encerrado = False
        font_vitoria = pg.font.SysFont(None, ConfigJogo.FONTE_TITULO)

        if p2Vida <= 0:
            self.vitoria = font_vitoria.render(
                f'Vitória do Jogador 1!', True, ConfigJogo.COR_TITULO)
            
        elif p1Vida <= 0:
            self.vitoria = font_vitoria.render(
                f'Vitória do Jogador 2!', True, ConfigJogo.COR_TITULO)
            
        elif p1Vida > p2Vida:
            self.vitoria = font_vitoria.render(
                f'Vitória do Jogador 1!', True, ConfigJogo.COR_TITULO)
            
        elif p1Vida < p2Vida:
            self.vitoria = font_vitoria.render(
                f'Vitória do Jogador 2!', True, ConfigJogo.COR_TITULO)
            
        elif p1Vida == p2Vida:
            self.vitoria = font_vitoria.render(
                f'Empate!', True, ConfigJogo.COR_TITULO)
    
    def rodar_final(self):
        while not self.encerrado:
            self.desenha()
            self.eventos()

    def eventos(self):
        pg.event.get()
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            self.encerrado = True
            sys.exit(0)

    def desenha(self):
        self.tela_f.fill((255, 255, 255))
        self.desenha_vitoria(self.tela_f)
        pg.display.flip()

    def desenha_vitoria(self, tela_f):       
        cx = ConfigJogo.LARGURA_TELA//2 - self.vitoria.get_size()[0]//2
        cy = ConfigJogo.ALTURA_TELA//2

        tela_f.blit(self.vitoria, (cx, cy))