import pygame as pg

class Personagem:
    def __init__(self, escolhido, tela) :
        self.personagem = escolhido
        self.tela = tela
    
    def stats(self):
        
        #guerreiro
        if self.personagem == 1:
            
            VELOCIDADE = 1.3
            VIDA = 40
            VELOCIDADE_ATQ = 2
            DANO = 5
            self.status = (VELOCIDADE, VIDA, 1, VELOCIDADE_ATQ, DANO)
          
        #mago  
        elif self.personagem == 2:
            
            VELOCIDADE = 1.5
            VIDA = 20
            VELOCIDADE_ATQ = 2
            DANO = 5
            self.status = (VELOCIDADE, VIDA, 2, VELOCIDADE_ATQ, DANO)
          
        #xamã  
        elif self.personagem == 3:
            
            VELOCIDADE = 1.5
            VIDA = 30
            VELOCIDADE_ATQ = 4
            DANO = 4
            self.status = (VELOCIDADE, VIDA, 3, VELOCIDADE_ATQ, DANO)
          
        #arqueiro  
        elif self.personagem == 4:
            
            VELOCIDADE = 1.5
            VIDA = 30
            VELOCIDADE_ATQ = 1
            DANO = 3
            self.status = (VELOCIDADE, VIDA, 4, VELOCIDADE_ATQ, DANO)
    