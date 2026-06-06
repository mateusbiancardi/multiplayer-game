

import sys
import math
import pygame


def load_image(name, colorkey=None, scale=1.0):
    '''
    funcao para ler imagens
    '''
    image = pygame.image.load(name)

    size = image.get_size()
    size = (int(size[0] * scale), int(size[1] * scale))
    image = pygame.transform.scale(image, size)

    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
VELOCIDADE_BOLA = 0.25

# inicializacao basica
pygame.init()

# cria uma janela com o tamanho dado
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# carrega a imagem da bola
imagem_bola = load_image('bola.png', scale=0.1)

# obtem o tamanho e a largura da imagem
rect = imagem_bola.get_rect()
bola_largura = rect.width
bola_altura = rect.height

# inicialmente a posicao da bola e o alvo como
# o centro da tela
bola_x = SCREEN_WIDTH // 2
bola_y = SCREEN_HEIGHT // 2
alvo_x = SCREEN_WIDTH // 2
alvo_y = SCREEN_HEIGHT // 2

# enquanto a janela nao for fechada
while True:

    # para cada evento recebido
    for event in pygame.event.get():
        # se for recebido o evento de fechar a janela (ex.: usuario clicou no 'x')
        # ou se a tecla esc for pressionada...
        if (event.type == pygame.QUIT) or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or \
                (pygame.key.get_pressed()[pygame.K_ESCAPE]):
            # ... encerra o programa
            print("Encerrando o programa.")
            sys.exit()

        # atualiza a posicao do alvo quando a pessoa clicar com o mouse
        if (event.type == pygame.MOUSEBUTTONDOWN) or (pygame.mouse.get_pressed()[0]):
            mouse_position = pygame.mouse.get_pos()
            alvo_x = mouse_position[0]
            alvo_y = mouse_position[1]

    # Atualiza a velocidade da bola
    # Se a distancia para o alvo for maior que o limite,
    # define uma velocidade em direcao ao alvo. Senao,
    # define a velocidade como zero.
    dist = math.sqrt(
        (alvo_x - bola_x) ** 2 +
        (alvo_y - bola_y) ** 2
    )

    if dist > 1:
        # define o vetor velocidade
        # 1) primeiro calcula a direcao
        bola_vx = alvo_x - bola_x
        bola_vy = alvo_y - bola_y
        # 2) faz o tamanho do vetor igual a 1 (normalizacao)
        norma = math.sqrt(bola_vx ** 2 + bola_vy ** 2)
        bola_vx /= norma
        bola_vy /= norma
        # 3) ajusta o tamanho para ser igual à constante VELOCIDADE_BOLA
        bola_vx *= VELOCIDADE_BOLA
        bola_vy *= VELOCIDADE_BOLA
    else:
        bola_vx = 0
        bola_vy = 0

    # Atualiza a posicao da bola de acordo com a velocidade
    bola_x += bola_vx
    bola_y += bola_vy

    # preenche a tela com branco
    screen.fill((255, 255, 255))

    # desenha o alvo com 3 circulos
    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (alvo_x, alvo_y),
        30,
        width=2)

    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (alvo_x, alvo_y),
        20,
        width=2)

    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (alvo_x, alvo_y),
        10)

    # desenha a imagem da bola
    rect = pygame.rect.Rect(
        bola_x - bola_largura // 2,
        bola_y - bola_altura // 2,
        bola_largura,
        bola_altura
    )
    screen.blit(imagem_bola, rect)

    # atualiza a tela
    pygame.display.flip()
