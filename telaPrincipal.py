import pygame as pg
import sys
import os
import math
import time
from configJogo import ConfigJogo
from selecaoPersonagem import telaSelecao
from personagens import Personagem
from cooldownCast import CooldownCast
from time import time
from blocos import bloco

class telaPrincipal():
    def __init__(self, tela, escolhidos):
        self.tela = tela
        self.encerrada = False
        self.primeiroCastE = True
        self.primeiroCastQ = True
        self.primeiroCastM = True
        self.primeiroCastN = True
        
        self.posicaoAdquirida = False
        self.mouse_pos = ()
        
        self.tempoInicio = time()
        
        p1 = Personagem(escolhidos[0], self.tela)
        p2 = Personagem(escolhidos[1], self.tela)
        
        self.CastE = CooldownCast()
        self.CastQ = CooldownCast()
        
        self.CastM = CooldownCast()
        self.CastN = CooldownCast()
        
        p1.stats()
        p2.stats()
        
        self.p1AtaqueE = False
        self.p1AtaqueQ = False
        
        self.p2AtaqueM = False
        self.p2AtaqueN = False
        
        
        self.p1Velocidade = p1.status[0]
        self.p2Velocidade = p2.status[0]
        self.p1VelocidadePadrao = p1.status[0]
        self.p2VelocidadePadrao = p2.status[0]
        
        self.v_Flecha = 2.0
        
        self.xP1FlechaEsquerda = 0
        self.xP1FlechaDireita = 0
        self.yP1FlechaCima = 0
        self.yP1FlechaBaixo = 0
        
        self.xP2FlechaEsquerda = 0
        self.xP2FlechaDireita = 0
        self.yP2FlechaCima = 0
        self.yP2FlechaBaixo = 0
        
        self.p1Vida = p1.status[1]
        self.p2Vida = p2.status[1]
        self.p1VidaAntes = p1.status[1]
        self.p2VidaAntes = p2.status[1]
        self.p1VidaTotal = p1.status[1]
        self.p2VidaTotal = p2.status[1]
        
        self.p1 = p1.status[2]
        self.p2 = p2.status[2]
        
        self.p1VelocidadeAtq = p1.status[3]
        self.p2VelocidadeAtq = p2.status[3]
        
        self.p1Dano = p1.status[4]
        self.p2Dano = p2.status[4]
        self.p1DanoPadrao = p1.status[4]
        self.p2DanoPadrao = p2.status[4]
        
        self.xP1 = ConfigJogo.LARGURA_TELA * (1/3)
        self.yP1 = ConfigJogo.ALTURA_TELA // 2
        self.v_xP1 = 0
        self.v_yP1 = 0
        
        self.v_Lacaio = 1.55
        self.xP1Lacaio = 0
        self.yP1Lacaio = 0
        self.xP2Lacaio = 0
        self.yP2Lacaio = 0
        
        self.xP2 = ConfigJogo.LARGURA_TELA * (2/3)
        self.yP2 = ConfigJogo.ALTURA_TELA // 2
        self.v_xP2 = 0
        self.v_yP2 = 0
    
        self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'guerreiro.png'))
        self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'mago.png'))
        self.sprite3_tamanho = pg.image.load(os.path.join('sprites', 'xama.png'))
        self.sprite4_tamanho = pg.image.load(os.path.join('sprites', 'arqueiro.png'))
        
        self.imagerect = self.sprite1_tamanho.get_rect()
        
        self.display_surface = pg.display.get_surface()
        self.sprites_visiveis = pg.sprite.Group()
        self.sprites_obstaculos = pg.sprite.Group()
        self.criar_mapa()

        self.raioATQGiratorio = 50
        self.raioATQProjetil = 5
        
        self.xEsquerdaP1 = True
        self.xDireitaP1 = False
        self.xEsquerdaP2 = True
        self.xDireitaP2 = False

    def endGame(self):
        self.tempo()
        if self.tempoJogo == 0:
            self.encerrada = True
            
        if self.p1Vida <= 0 or self.p2Vida <= 0:
            self.encerrada = True
            
    #Tempo que falta para acabar a partida
    def tempo(self):
        self.tempoAtual = time()
        self.tempoPassado = self.tempoAtual - self.tempoInicio
        self.tempoJogo = int(ConfigJogo.DURACAO_PARTIDA - self.tempoPassado)
        
        font_tempo = pg.font.SysFont(None, ConfigJogo.FONTE_TEMPO)
        self.textoTempo = font_tempo.render(
            f'{self.tempoJogo}', True, ConfigJogo.COR_TEMPO)
        
        self.tela.blit(self.textoTempo, ((ConfigJogo.LARGURA_TELA // 2) - 30, ConfigJogo.ALTURA_TELA*0.05))
        

    def criar_mapa(self):
        for row_index, row in enumerate(ConfigJogo.MAPA_JOGO):
            for col_index, col in enumerate(row):
                x = col_index * 32
                y = row_index * 32

                if col == 8:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 8)
                if col == 5:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 5)
                if col == 4:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 4)
                if col == 9:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 9)
                if col == 1:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 1)
                if col == 0:
                    bloco((x,y), [self.sprites_visiveis, self.sprites_obstaculos], 0)
          
    def rodar(self):
        while not self.encerrada:
            self.tela.fill((102, 255, 51))
            self.sprites_visiveis.draw(self.display_surface)
            self.tratamentoEventos()
            self.ataques()
            self.movimento()
            self.carregarPersonagem()
            self.endGame()

            pg.display.flip()
        return (self.p1Vida, self.p2Vida)
            
    def tratamentoEventos(self):
        events = pg.event.get()
            
        for event in events:
            #Personagem 1 (W A S D)
            #Movimentação (xEsquerdaP1 e xDireitaP1 são usados para inverter os sprites dos personagens de acordo com a
            # direção de movimento)
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_a)) or (pg.key.get_pressed()[pg.K_a]):
                self.v_xP1 = -self.p1Velocidade
                self.xEsquerdaP1 = True
                self.xDireitaP1 = False

            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_d)) or (pg.key.get_pressed()[pg.K_d]):
                self.v_xP1 = self.p1Velocidade
                self.xEsquerdaP1 = False
                self.xDireitaP1 = True
                
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_w)) or (pg.key.get_pressed()[pg.K_w]):
                self.v_yP1 = -self.p1Velocidade

            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_s)) or (pg.key.get_pressed()[pg.K_s]):
                self.v_yP1 = self.p1Velocidade
                
            #Se o botão de movimento é solto, zera a velocidade do personagem
            if ((event.type == pg.KEYUP) and (event.key == pg.K_a)) or \
                        ((event.type == pg.KEYUP) and (event.key == pg.K_d)):
                self.v_xP1 = 0
                
            if ((event.type == pg.KEYUP) and (event.key == pg.K_w)) or \
                        ((event.type == pg.KEYUP) and (event.key == pg.K_s)):
                self.v_yP1 = 0
                   
            #Ataque E
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_e)) or (pg.key.get_pressed()[pg.K_e]):
                cooldownCastE = self.CastE.diferenca()
                
                if (cooldownCastE > self.p1VelocidadeAtq) or self.primeiroCastE:
                    self.p1AtaqueE = True
                    self.CastE.resetar()
                    self.duracaoCastE = time()
                    self.primeiroCastE = False
                    
                    self.posicaoAdquirida = False
                    self.clique = False
                    
                    self.p1VidaLacaio = 3
                    
                    self.xP1FlechaEsquerda = self.xP1+20
                    self.xP1FlechaDireita = self.xP1+20
                    self.yP1FlechaCima = self.yP1+25
                    self.yP1FlechaBaixo = self.yP1+25
                    
                    self.xP1Flecha = self.xP1+20
                    self.yP1Flecha = self.yP1+25
                    
                    self.xP1Lacaio = self.xP1
                    self.yP1Lacaio = self.yP1
                    
                    
            
            #Ataque Q
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_q)) or (pg.key.get_pressed()[pg.K_q]):
                cooldownCastQ = self.CastQ.diferenca()
                
                if (cooldownCastQ > self.p1VelocidadeAtq*3) or self.primeiroCastQ:
                    self.p1AtaqueQ = True
                    self.CastQ.resetar()
                    self.duracaoCastQ = time()
                    self.primeiroCastQ = False
            
            #Personagem 2 (setinhas)
            #Movimentação
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_LEFT)) or (pg.key.get_pressed()[pg.K_LEFT]):
                self.v_xP2 = -self.p2Velocidade
                self.xEsquerdaP2 = True
                self.xDireitaP2 = False

            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_RIGHT)) or (pg.key.get_pressed()[pg.K_RIGHT]):
                self.v_xP2 = self.p2Velocidade
                self.xEsquerdaP2 = False
                self.xDireitaP2 = True
                
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_UP)) or (pg.key.get_pressed()[pg.K_UP]):
                self.v_yP2 = -self.p2Velocidade

            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_DOWN)) or (pg.key.get_pressed()[pg.K_DOWN]):
                self.v_yP2 = self.p2Velocidade
                
            if ((event.type == pg.KEYUP) and (event.key == pg.K_LEFT)) or \
                        ((event.type == pg.KEYUP) and (event.key == pg.K_RIGHT)):
                self.v_xP2 = 0
                
            if ((event.type == pg.KEYUP) and (event.key == pg.K_UP)) or \
                        ((event.type == pg.KEYUP) and (event.key == pg.K_DOWN)):
                self.v_yP2 = 0
                
                
            #Ataque M
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_m)) or (pg.key.get_pressed()[pg.K_m]):
                cooldownCastM = self.CastM.diferenca()
                
                if (cooldownCastM > self.p2VelocidadeAtq) or self.primeiroCastM:
                    self.p2AtaqueM = True
                    self.CastM.resetar()
                    self.duracaoCastM = time()
                    self.primeiroCastM = False
                    self.posicaoAdquirida = False
                    self.clique = False
                    
                    self.xP2Flecha = self.xP2+20
                    self.yP2Flecha = self.yP2+25
                    
                    
                    self.xP2FlechaEsquerda = self.xP2+20
                    self.xP2FlechaDireita = self.xP2+20
                    self.yP2FlechaCima = self.yP2+25
                    self.yP2FlechaBaixo = self.yP2+25
                    
                    self.xP2Lacaio = self.xP2
                    self.yP2Lacaio = self.yP2
            
            #Ataque N
            if ((event.type == pg.KEYDOWN) and (event.key == pg.K_n)) or (pg.key.get_pressed()[pg.K_n]):
                cooldownCastN = self.CastN.diferenca()
                
                if (cooldownCastN > self.p2VelocidadeAtq*3) or self.primeiroCastN:
                    self.p2AtaqueN = True
                    self.CastN.resetar()
                    self.duracaoCastN = time()
                    self.primeiroCastN = False
                    
            #Mouse
            if event.type == pg.MOUSEBUTTONUP:
                
                
                self.mouse_pos = pg.mouse.get_pos()
                self.clique = True
           
                
        # evento de saida
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            sys.exit(0)
    
    def movimento(self):
        
        #Colisão com os limites do mapa
        if ((self.xP1 + self.v_xP1 < 0) or (self.xP1 + self.v_xP1 > ConfigJogo.LARGURA_TELA-50)):
            self.v_xP1 = 0
        if ((self.yP1 + self.v_yP1 < 0) or (self.yP1 + self.v_yP1 > ConfigJogo.ALTURA_TELA-50)):
            self.v_yP1 = 0
            
        if ((self.xP2 + self.v_xP2 < 0) or (self.xP2 + self.v_xP2 > ConfigJogo.LARGURA_TELA-50)):
            self.v_xP2 = 0
        if ((self.yP2 + self.v_yP2 < 0) or (self.yP2 + self.v_yP2 > ConfigJogo.ALTURA_TELA-50)):
            self.v_yP2 = 0
        
        #Parede de pedra
        if (((self.xP1 + self.v_xP1 > 96) and (self.xP1 + self.v_xP1 < 192)) or\
        ((self.xP1 + self.v_xP1 > 928) and (self.xP1 + self.v_xP1 < 1024))) and\
        (((self.yP1 + self.v_yP1 > 96) and (self.yP1 + self.v_yP1 < 192)) or\
        ((self.yP1 + self.v_yP1 > 416) and (self.yP1 + self.v_yP1 < 512))):
            self.v_xP1 = 0 
            self.v_yP1 = 0
        
        if (((self.xP2 + self.v_xP2 > 96) and (self.xP2 + self.v_xP2 < 192)) or\
        ((self.xP2 + self.v_xP2 > 928) and (self.xP2 + self.v_xP2 < 1024))) and\
        (((self.yP2 + self.v_yP2 > 96) and (self.yP2 + self.v_yP2 < 192)) or\
        ((self.yP2 + self.v_yP2 > 416) and (self.yP2 + self.v_yP2 < 512))):
            self.v_xP2 = 0 
            self.v_yP2 = 0
        
            #laterais
        if(((self.xP1 + self.v_xP1 > 96) and (self.xP1 + self.v_xP1 < 192)) or\
        ((self.xP1 + self.v_xP1 > 928) and (self.xP1 + self.v_xP1 < 1024))) and\
        (((self.yP1 + self.v_yP1 > 64) and (self.yP1 + self.v_yP1 < 96)) or\
        ((self.yP1 + self.v_yP1 > 192) and (self.yP1 + self.v_yP1 < 224)) or\
        ((self.yP1 + self.v_yP1 > 384) and (self.yP1 + self.v_yP1 < 416)) or\
        ((self.yP1 + self.v_yP1 > 512) and (self.yP1 + self.v_yP1 < 544))):
            self.v_xP1 = 0 
            self.v_yP1 = 0
        
        if(((self.xP2 + self.v_xP2 > 96) and (self.xP2 + self.v_xP2 < 192)) or\
        ((self.xP2 + self.v_xP2 > 928) and (self.xP2 + self.v_xP2 < 1024))) and\
        (((self.yP2 + self.v_yP2 > 64) and (self.yP2 + self.v_yP2 < 96)) or\
        ((self.yP2 + self.v_yP2 > 192) and (self.yP2 + self.v_yP2 < 224)) or\
        ((self.yP2 + self.v_yP2 > 384) and (self.yP2 + self.v_yP2 < 416)) or\
        ((self.yP2 + self.v_yP2 > 512) and (self.yP2 + self.v_yP2 < 544))):
            self.v_xP2 = 0 
            self.v_yP2 = 0                 
            
            #cima e baixo
        if(((self.xP1 + self.v_xP1 > 64) and (self.xP1 + self.v_xP1 < 96)) or\
        ((self.xP1 + self.v_xP1 > 192) and (self.xP1 + self.v_xP1 < 224)) or\
        ((self.xP1 + self.v_xP1 > 896) and (self.xP1 + self.v_xP1 < 928)) or\
        ((self.xP1 + self.v_xP1 > 1024) and (self.xP1 + self.v_xP1 < 1056))) and\
        (((self.yP1 + self.v_yP1 > 96) and (self.yP1 + self.v_yP1 < 192)) or\
        ((self.yP1 + self.v_yP1 > 416) and (self.yP1 + self.v_yP1 < 512))):
            self.v_xP1 = 0 
            self.v_yP1 = 0 

        if(((self.xP2 + self.v_xP2 > 64) and (self.xP2 + self.v_xP2 < 96)) or\
        ((self.xP2 + self.v_xP2 > 192) and (self.xP2 + self.v_xP2 < 224)) or\
        ((self.xP2 + self.v_xP2 > 896) and (self.xP2 + self.v_xP2 < 928)) or\
        ((self.xP2 + self.v_xP2 > 1024) and (self.xP2 + self.v_xP2 < 1056))) and\
        (((self.yP2 + self.v_yP2 > 96) and (self.yP2 + self.v_yP2 < 192)) or\
        ((self.yP2 + self.v_yP2 > 416) and (self.yP2 + self.v_yP2 < 512))):
            self.v_xP2 = 0 
            self.v_yP2 = 0 
        #Parede de madeira
        if ((self.xP1 + self.v_xP1 > 502) and (self.xP1 + self.v_xP1 < 608))and\
        ((self.yP1 + self.v_yP1 > 128) and (self.yP1 + self.v_yP1 < 224)):
            self.v_xP1 = 0 
            self.v_yP1 = 0
        
        if ((self.xP2 + self.v_xP2 > 502) and (self.xP2 + self.v_xP2 < 608))and\
        ((self.yP2 + self.v_yP2 > 128) and (self.yP2 + self.v_yP2 < 224)):
            self.v_xP2 = 0 
            self.v_yP2 = 0

        #flechas
        self.xP1FlechaEsquerda += -self.v_Flecha
        self.xP1FlechaDireita += self.v_Flecha
        self.yP1FlechaCima += -self.v_Flecha
        self.yP1FlechaBaixo += self.v_Flecha
        
        self.xP2FlechaEsquerda += -self.v_Flecha
        self.xP2FlechaDireita += self.v_Flecha
        self.yP2FlechaCima += -self.v_Flecha
        self.yP2FlechaBaixo += self.v_Flecha
        
        #Movimentação
        self.xP1 += self.v_xP1
        self.yP1 += self.v_yP1
            
        self.xP2 += self.v_xP2
        self.yP2 += self.v_yP2
    
    def carregarPersonagem(self):
        if self.p1 == 1 and self.xEsquerdaP1:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'guerreiro.png'))
        
        elif self.p1 == 1 and self.xDireitaP1:
            #inverte o sprite
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'guerreiro.png'))
            self.sprite1_tamanho = pg.transform.flip(self.sprite1_tamanho, True, False)
            
            
        if self.p1 == 2 and self.xEsquerdaP1:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'mago.png'))
            
        elif self.p1 == 2 and self.xDireitaP1:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'mago.png'))
            self.sprite1_tamanho = pg.transform.flip(self.sprite1_tamanho, True, False)
           
            
        if self.p1 == 3 and self.xEsquerdaP1:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'xama.png'))
            
        elif self.p1 == 3 and self.xDireitaP1:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'xama.png'))
            self.sprite1_tamanho = pg.transform.flip(self.sprite1_tamanho, True, False)
            
            
        if self.p1 == 4 and self.xEsquerdaP1:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'arqueiro.png'))
        
        elif self.p1 == 4 and self.xDireitaP1:
            self.sprite1_tamanho = pg.image.load(os.path.join('sprites', 'arqueiro.png'))
            self.sprite1_tamanho = pg.transform.flip(self.sprite1_tamanho, True, False)
            
            
            
            
        if self.p2 == 1 and self.xEsquerdaP2:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'guerreiro.png'))
        
        elif self.p2 == 1 and self.xDireitaP2:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'guerreiro.png'))
            self.sprite2_tamanho = pg.transform.flip(self.sprite2_tamanho, True, False)
            
        if self.p2 == 2 and self.xEsquerdaP2:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'mago.png'))
        
        elif self.p2 == 2 and self.xDireitaP2:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'mago.png'))
            self.sprite2_tamanho = pg.transform.flip(self.sprite2_tamanho, True, False)
            
        if self.p2 == 3 and self.xEsquerdaP2:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'xama.png'))
        
        elif self.p2 == 3 and self.xDireitaP2:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'xama.png'))
            self.sprite2_tamanho = pg.transform.flip(self.sprite2_tamanho, True, False)
            
        if self.p2 == 4 and self.xEsquerdaP2:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'arqueiro.png'))
        
        elif self.p2 == 4 and self.xDireitaP2:
            self.sprite2_tamanho = pg.image.load(os.path.join('sprites', 'arqueiro.png'))
            self.sprite2_tamanho = pg.transform.flip(self.sprite2_tamanho, True, False)
            
        self.sprite3_minion = pg.image.load(os.path.join('sprites', 'minion.png'))
            
        self.personagem()
            
    
    def personagem (self):
        
        self.berserker = pg.image.load(os.path.join('sprites', 'berserker.png'))
        self.lacaio = pg.image.load(os.path.join('sprites', 'minion.png'))
        font_vida = pg.font.SysFont(None, ConfigJogo.FONTE_VIDA)
        self.textoVida1 = font_vida.render(
            f'{int(self.p1Vida)}/{self.p1VidaTotal}', True, ConfigJogo.COR_VIDA)
        
        self.textoVida2 = font_vida.render(
            f'{int(self.p2Vida)}/{self.p2VidaTotal}', True, ConfigJogo.COR_VIDA)
        
        self.tela.blit(self.textoVida1, (self.xP1, self.yP1-20))
        self.tela.blit(self.textoVida2, (self.xP2, self.yP2-20))
        
        self.tela.blit(self.sprite1_tamanho, (self.xP1, self.yP1))
        self.tela.blit(self.sprite2_tamanho, (self.xP2, self.yP2)) 
        
    def ataques(self):
        # Posicão centralizada dos personagens
        self.xP1CirculoCentralizado = self.xP1+30
        self.yP1CirculoCentralizado = self.yP1+25
        
        self.xP2CirculoCentralizado = self.xP2+30
        self.yP2CirculoCentralizado = self.yP2+25
        
        #Jogador 1
        #Guerreiro
        #Ataque Giratório (E)
        if self.p1 == 1 and self.p1AtaqueE:
            #Duração da skill
            if time() - self.duracaoCastE < 0.1:
                pg.draw.circle(self.tela, (0,0,0), (self.xP1CirculoCentralizado, self.yP1CirculoCentralizado), self.raioATQGiratorio, 5)
                #Se o p2 está localizado na área de p1:
                if ((int(self.xP2) in range (int(self.xP1CirculoCentralizado-self.raioATQGiratorio), int(self.xP1CirculoCentralizado+self.raioATQGiratorio)) or \
                    int (self.xP2+40) in range (int(self.xP1CirculoCentralizado-self.raioATQGiratorio), int(self.xP1CirculoCentralizado+self.raioATQGiratorio))) and \
                        (int(self.yP2) in range (int(self.yP1CirculoCentralizado-self.raioATQGiratorio), int(self.yP1CirculoCentralizado+self.raioATQGiratorio)) or \
                            int(self.yP2+55) in range (int(self.yP1CirculoCentralizado-self.raioATQGiratorio), int(self.yP1CirculoCentralizado+self.raioATQGiratorio)))) and \
                                self.p2Vida - self.p2VidaAntes == 0:
                                    self.p2Vida = self.p2Vida-self.p1Dano
                pos_madeira=[(544,160),(544,192),(576,160),(576,192)]
                for x in pos_madeira:
                    if bloco(x, [self.sprites_visiveis, self.sprites_obstaculos], 5)\
                        in range (int(self.xP1CirculoCentralizado-self.raioATQGiratorio), int(self.xP1CirculoCentralizado+self.raioATQGiratorio)):
                            self.tela.blit(bloco(x, [self.sprites_visiveis, self.sprites_obstaculos], 8))
            else:
                self.p2VidaAntes = self.p2Vida
        
        #Berserk - Aumenta o dano e velocidade de ataque por um breve momento (Q)   
        if self.p1 == 1 and self.p1AtaqueQ:
            if time() - self.duracaoCastQ < 3:
                self.tela.blit(self.berserker, (self.xP1+10, self.yP1-50))
                self.p1Velocidade = 1.55
                self.p1Dano = 10
            else:
                self.p1Velocidade = self.p1VelocidadePadrao
                self.p1Dano = self.p1DanoPadrao
                
        #Mago
        #Bola de fogo (E + Mouse)

        if self.p1 == 2 and self.p1AtaqueE:
            if time() - self.duracaoCastE < 2:
                if self.clique:
                    self.posicaoAdquirida = True
                
                if self.posicaoAdquirida: 
                    pg.draw.circle(self.tela, (255,0,0), (self.mouse_pos[0], self.mouse_pos[1]), self.raioATQGiratorio, 5)  
                
                
                    #Se o p2 está localizado na área da bola de fogo:
                    if ((int(self.xP2) in range (int(self.mouse_pos[0]-self.raioATQGiratorio), int(self.mouse_pos[0]+self.raioATQGiratorio)) or \
                        int (self.xP2+40) in range (int(self.mouse_pos[0]-self.raioATQGiratorio), int(self.mouse_pos[0]+self.raioATQGiratorio))) and \
                            (int(self.yP2) in range (int(self.mouse_pos[1]-self.raioATQGiratorio), int(self.mouse_pos[1]+self.raioATQGiratorio)) or \
                                int(self.yP2+55) in range (int(self.mouse_pos[1]-self.raioATQGiratorio), int(self.mouse_pos[1]+self.raioATQGiratorio)))) and \
                                    (self.p2Vida - self.p2VidaAntes == 0 or time() - self.cooldownFireballP1 > 0.9):
                                        self.p2Vida = self.p2Vida-self.p1Dano
                                        self.cooldownFireballP1 = time()
            else:
                self.p2VidaAntes = self.p2Vida
                
        #Xamã
        #Invocar Lacaio (E)
        if self.p1 == 3 and self.p1AtaqueE:
            if time() - self.duracaoCastE < 3:
                self.tela.blit(self.lacaio, (self.xP1Lacaio, self.yP1Lacaio))
                
                distP2 = math.sqrt(
                    (self.xP2 - self.xP1Lacaio) ** 2 +
                    (self.yP2 - self.yP1Lacaio) ** 2
                )

                if distP2 > 1:
                    
                    # 1) primeiro calcula a direcao
                    self.P1v_x = self.xP2 - self.xP1Lacaio
                    self.P1v_y = self.yP2 - self.yP1Lacaio
                    # 2) faz o tamanho do vetor igual a 1 (normalizacao)
                    normaP1 = math.sqrt(self.P1v_x ** 2 + self.P1v_y ** 2)
                    self.P1v_x /= normaP1
                    self.P1v_y /= normaP1
                    # 3) ajusta o tamanho para ser igual à constante self.v_Lacaio
                    self.P1v_x *= self.v_Lacaio
                    self.P1v_y *= self.v_Lacaio
                else:
                    if self.p2VidaAntes == self.p2Vida or time() - self.cooldownATKMinionP1 > 1.2:
                        self.p2Vida = self.p2Vida-self.p1Dano
                        self.cooldownATKMinionP1 = time()
                    self.P1v_x = 0
                    self.P1v_y = 0

                # Atualiza a posicao do lacaio de acordo com a velocidade
                self.xP1Lacaio += self.P1v_x
                self.yP1Lacaio += self.P1v_y
                
            else:
                self.p2VidaAntes = self.p2Vida
                
        #Arqueiro
        #Ataque de flecha (E) - Atira flecha nas 4 direções
        if self.p1 == 4 and self.p1AtaqueE:
            if time() - self.duracaoCastE < 1:
                
                pg.draw.circle(self.tela, (0,0,0), (self.xP1FlechaEsquerda, self.yP1Flecha), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP1FlechaDireita, self.yP1Flecha), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP1Flecha, self.yP1FlechaCima), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP1Flecha, self.yP1FlechaBaixo), self.raioATQProjetil, 5)
                
                #se o p2 está na área de alcance do ataque de projétil:
                #projetil da esquerda
                if (((int(self.xP1FlechaEsquerda - self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) or \
                    int(self.xP1FlechaEsquerda + self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) and \
                        ((int(self.yP1Flecha - self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55))) or \
                            int(self.yP1Flecha + self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55)))) and \
                                self.p2Vida - self.p2VidaAntes == 0:
                                    self.p2Vida = self.p2Vida-self.p1Dano
                   
                #projetil da direita                 
                if (((int(self.xP1FlechaDireita - self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) or \
                    int(self.xP1FlechaDireita + self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) and \
                        ((int(self.yP1Flecha - self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55))) or \
                            int(self.yP1Flecha + self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55)))) and \
                                self.p2Vida - self.p2VidaAntes == 0:
                                    self.p2Vida = self.p2Vida-self.p1Dano
                                    
                #projetil de cima                
                if (((int(self.xP1Flecha - self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) or \
                    int(self.xP1Flecha + self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) and \
                        ((int(self.yP1FlechaCima - self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55))) or \
                            int(self.yP1FlechaCima + self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55)))) and \
                                self.p2Vida - self.p2VidaAntes == 0:
                                    self.p2Vida = self.p2Vida-self.p1Dano
                                    
                #projetil de baixo               
                if (((int(self.xP1Flecha - self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) or \
                    int(self.xP1Flecha + self.raioATQProjetil) in range (int(self.xP2), int(self.xP2+40))) and \
                        ((int(self.yP1FlechaBaixo - self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55))) or \
                            int(self.yP1FlechaBaixo + self.raioATQProjetil) in range (int(self.yP2), int(self.yP2+55)))) and \
                                self.p2Vida - self.p2VidaAntes == 0:
                                    self.p2Vida = self.p2Vida-self.p1Dano

            else:
                self.p2VidaAntes = self.p2Vida  
                
          
        #Jogador 2
        #Guerreiro
        #Ataque Giratório (M)        
        if self.p2 == 1 and self.p2AtaqueM:
            if time() - self.duracaoCastM < 0.1:
                pg.draw.circle(self.tela, (0,0,0), (self.xP2CirculoCentralizado, self.yP2CirculoCentralizado), self.raioATQGiratorio, 5)
                #Se o p1 está localizado na área de p2:
                if ((int(self.xP1) in range (int(self.xP2CirculoCentralizado-self.raioATQGiratorio), int(self.xP2CirculoCentralizado+self.raioATQGiratorio)) or \
                    int (self.xP1+40) in range (int(self.xP2CirculoCentralizado-self.raioATQGiratorio), int(self.xP2CirculoCentralizado+self.raioATQGiratorio))) and \
                        (int(self.yP1) in range (int(self.yP2CirculoCentralizado-self.raioATQGiratorio), int(self.yP2CirculoCentralizado+self.raioATQGiratorio)) or \
                            int(self.yP1+55) in range (int(self.yP2CirculoCentralizado-self.raioATQGiratorio), int(self.yP2CirculoCentralizado+self.raioATQGiratorio)))) and \
                                self.p1Vida - self.p1VidaAntes == 0:
                                    self.p1Vida = self.p1Vida-self.p2Dano
                pos_madeira=[(544,160),(544,192),(576,160),(576,192)]
                for x in pos_madeira:
                    if bloco(x, [self.sprites_visiveis, self.sprites_obstaculos], 5)\
                        in range (int(self.xP1CirculoCentralizado-self.raioATQGiratorio), int(self.xP1CirculoCentralizado+self.raioATQGiratorio)):
                            self.tela.blit(bloco(x, [self.sprites_visiveis, self.sprites_obstaculos], 8))
            else:
                self.p1VidaAntes = self.p1Vida
        
        #Berserk - Aumenta o dano e velocidade de movimento por um breve momento (N)   
        if self.p2 == 1 and self.p2AtaqueN:
            if time() - self.duracaoCastN < 3:
                self.tela.blit(self.berserker, (self.xP2+10, self.yP2-50))
                self.p2Velocidade = 1.55
                self.p2Dano = 10
            else:
                self.p2Velocidade = self.p2VelocidadePadrao
                self.p2Dano = self.p2DanoPadrao
        
        #Mago
        #Bola de fogo (M + Mouse)        
        if self.p2 == 2 and self.p2AtaqueM:
            
            if time() - self.duracaoCastM < 2:
                if self.clique:
                    self.posicaoAdquirida = True
                
                if self.posicaoAdquirida: 
                    pg.draw.circle(self.tela, (255,0,0), (self.mouse_pos[0], self.mouse_pos[1]), self.raioATQGiratorio, 5)  
                    
                    #Se o p1 está localizado na área da bola de fogo:
                    if ((int(self.xP1) in range (int(self.mouse_pos[0]-self.raioATQGiratorio), int(self.mouse_pos[0]+self.raioATQGiratorio)) or \
                        int (self.xP1+40) in range (int(self.mouse_pos[0]-self.raioATQGiratorio), int(self.mouse_pos[0]+self.raioATQGiratorio))) and \
                            (int(self.yP1) in range (int(self.mouse_pos[1]-self.raioATQGiratorio), int(self.mouse_pos[1]+self.raioATQGiratorio)) or \
                                int(self.yP1+55) in range (int(self.mouse_pos[1]-self.raioATQGiratorio), int(self.mouse_pos[1]+self.raioATQGiratorio)))) and \
                                    (self.p1Vida - self.p1VidaAntes == 0 or time() - self.cooldownFireballP2 > 0.9):
                                        self.p1Vida = self.p1Vida-self.p2Dano
                                        self.cooldownFireballP2 = time()
            else:
                self.p1VidaAntes = self.p1Vida
                
        #Xamã  
        #Invocar Lacaio (M)
        if self.p2 == 3 and self.p2AtaqueM:
            if time() - self.duracaoCastM < 3:
                self.tela.blit(self.lacaio, (self.xP2Lacaio, self.yP2Lacaio))
                
                distP1 = math.sqrt(
                    (self.xP1 - self.xP2Lacaio) ** 2 +
                    (self.yP1 - self.yP2Lacaio) ** 2
                )

                if distP1 > 1:
                    
                    # 1) primeiro calcula a direcao
                    self.P2v_x = self.xP1 - self.xP2Lacaio
                    self.P2v_y = self.yP1 - self.yP2Lacaio
                    # 2) faz o tamanho do vetor igual a 1 (normalizacao)
                    normaP2 = math.sqrt(self.P2v_x ** 2 + self.P2v_y ** 2)
                    self.P2v_x /= normaP2
                    self.P2v_y /= normaP2
                    # 3) ajusta o tamanho para ser igual à constante self.v_Lacaio
                    self.P2v_x *= self.v_Lacaio
                    self.P2v_y *= self.v_Lacaio
                else:
                    if self.p1VidaAntes == self.p1Vida or time() - self.cooldownATKMinionP2 > 1.2:
                        self.p1Vida = self.p1Vida-self.p2Dano
                        self.cooldownATKMinionP2 = time()
                    self.P2v_x = 0
                    self.P2v_y = 0

                # Atualiza a posicao do lacaio de acordo com a velocidade
                self.xP2Lacaio += self.P2v_x
                self.yP2Lacaio += self.P2v_y
                
            else:
                self.p1VidaAntes = self.p1Vida
                
        #Arqueiro
        #Ataque de flecha (M) - Atira flecha nas 4 direções
        if self.p2 == 4 and self.p2AtaqueM:
            if time() - self.duracaoCastM < 1:
                
                pg.draw.circle(self.tela, (0,0,0), (self.xP2FlechaEsquerda, self.yP2Flecha), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP2FlechaDireita, self.yP2Flecha), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP2Flecha, self.yP2FlechaCima), self.raioATQProjetil, 5)
                pg.draw.circle(self.tela, (0,0,0), (self.xP2Flecha, self.yP2FlechaBaixo), self.raioATQProjetil, 5)
                
                #se o p2 está na área de alcance do ataque de projétil:
                #projetil da esquerda
                if (((int(self.xP2FlechaEsquerda - self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) or \
                    int(self.xP2FlechaEsquerda + self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) and \
                        ((int(self.yP2Flecha - self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55))) or \
                            int(self.yP2Flecha + self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55)))) and \
                                self.p1Vida - self.p1VidaAntes == 0:
                                    self.p1Vida = self.p1Vida-self.p2Dano
                   
                #projetil da direita                 
                if (((int(self.xP2FlechaDireita - self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) or \
                    int(self.xP2FlechaDireita + self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) and \
                        ((int(self.yP2Flecha - self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55))) or \
                            int(self.yP2Flecha + self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55)))) and \
                                self.p1Vida - self.p1VidaAntes == 0:
                                    self.p1Vida = self.p1Vida-self.p2Dano
                                    
                #projetil de cima                
                if (((int(self.xP2Flecha - self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) or \
                    int(self.xP2Flecha + self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) and \
                        ((int(self.yP2FlechaCima - self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55))) or \
                            int(self.yP2FlechaCima + self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55)))) and \
                                self.p1Vida - self.p1VidaAntes == 0:
                                    self.p1Vida = self.p1Vida-self.p2Dano
                                    
                #projetil de baixo               
                if (((int(self.xP2Flecha - self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) or \
                    int(self.xP2Flecha + self.raioATQProjetil) in range (int(self.xP1), int(self.xP1+40))) and \
                        ((int(self.yP2FlechaBaixo - self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55))) or \
                            int(self.yP2FlechaBaixo + self.raioATQProjetil) in range (int(self.yP1), int(self.yP1+55)))) and \
                                self.p1Vida - self.p1VidaAntes == 0:
                                    self.p1Vida = self.p1Vida-self.p2Dano

            else:
                self.p1VidaAntes = self.p1Vida
            
        #Dano da lava
        if (((self.xP1 + self.v_xP1 > 542) and\
        (self.xP1 + self.v_xP1 < 608)) and\
        ((self.yP1 + self.v_yP1 > 96) and (self.yP1 + self.v_yP1 < 128))):
            self.p1Vida -= 0.05

        if ((self.xP2 + self.v_xP2 > 542)\
        and (self.xP2 + self.v_xP2 < 608)) and\
        ((self.yP2 + self.v_yP2 > 96) and (self.yP2 + self.v_yP2 < 128)):
            self.p2Vida -= 0.05
        
        if (((self.xP1 + self.v_xP1 > 64) and\
        (self.xP1 + self.v_xP1 < 128)) or\
        ((self.xP1 + self.v_xP1 > 1056) and\
        (self.xP1 + self.v_xP1 < 1120))) and\
        (((self.yP1 + self.v_yP1 > 576) and (self.yP1 + self.v_yP1 < 608))):
            self.p1Vida -= 0.05

        if (((self.xP2 + self.v_xP2 > 64) and\
        (self.xP2 + self.v_xP2 < 128)) or\
        ((self.xP2 + self.v_xP2 > 1056) and\
        (self.xP2 + self.v_xP2 < 1120))) and\
        (((self.yP2 + self.v_yP2 > 576) and (self.yP1 + self.v_yP1 < 608))):
            self.p2Vida -= 0.05

        if (((self.xP1 + self.v_xP1 > 128) and\
        (self.xP1 + self.v_xP1 < 192)) or\
        ((self.xP1 + self.v_xP1 > 960) and\
        (self.xP1 + self.v_xP1 < 1024))) and\
        (((self.yP1 + self.v_yP1 > 320) and (self.yP1 + self.v_yP1 < 352))):
            self.p1Vida -= 0.05

        if (((self.xP2 + self.v_xP2 > 128) and\
        (self.xP2 + self.v_xP2 < 192)) or\
        ((self.xP2 + self.v_xP2 > 960) and\
        (self.xP2 + self.v_xP2 < 1024))) and\
        (((self.yP2 + self.v_yP2 > 320) and (self.yP2 + self.v_yP2 < 352))):
            self.p2Vida -= 0.05