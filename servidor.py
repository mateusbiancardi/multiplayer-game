"""
servidor.py — servidor autoritativo (UDP). Roda a lógica do jogo, SEM janela.

Fluxo:
  1. bind numa porta UDP.
  2. Espera 2 clientes mandarem {"tipo":"hello"}. Guarda o endereço (ip,porta) de cada.
     O 1o vira jogador 1 (slot 1), o 2o vira jogador 2 (slot 2).
  3. Cria UM telaPrincipal headless (a lógica do jogo).
  4. Loop ~60 fps:
       - lê os inputs mais recentes que chegaram de cada cliente
       - roda um passo de simulação
       - serializa o estado e manda pros 2 clientes
  5. Quando estado["encerrada"], manda o estado final e encerra (ou volta pro passo 2).

Headless: o servidor não desenha. SDL_VIDEODRIVER=dummy faz o pygame não abrir tela.
"""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"   # tem que vir ANTES de importar/iniciar pygame

import socket
import pygame as pg

from rede.protocolo import enviar_msg, receber_msg, mais_novo
from telaPrincipal import telaPrincipal

HOST = "0.0.0.0"     # escuta em todas as interfaces
PORTA = 5000
FPS = 60

# input "neutro" — usado enquanto um cliente ainda não mandou nada nesse frame
INPUT_NEUTRO = {"left": False, "right": False, "up": False, "down": False,
                "atk1": False, "atk2": False, "click": False, "mouse": [0, 0]}


def esperar_jogadores(sock):
    """Espera 2 'hello' e retorna [addr_j1, addr_j2].

    Fica recebendo pacotes até 2 endereços DIFERENTES mandarem {"tipo":"hello"}.
    1o a chegar = jogador 1, 2o = jogador 2. Cuidado: o mesmo cliente pode mandar
    hello mais de uma vez (pacote repetido) — não conte o mesmo addr duas vezes.
    Ferramentas: receber_msg, msg.get("tipo"), uma lista de endereços.
    """
    raise NotImplementedError("implementar esperar_jogadores")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # SOCK_DGRAM = UDP
    sock.bind((HOST, PORTA))
    print(f"servidor UDP em {HOST}:{PORTA}")

    addr_j1, addr_j2 = esperar_jogadores(sock)

    pg.init()
    # Fase 3: personagens hardcoded pra testar a rede. Fase 5: receber escolha de cada cliente.
    escolhidos = [1, 2]   # [char do j1, char do j2]
    jogo = telaPrincipal(None, escolhidos)   # 'tela' = None: servidor não desenha

    # guarda o último input de cada jogador (e o último seq pra descartar pacote velho)
    inputs = {addr_j1: dict(INPUT_NEUTRO), addr_j2: dict(INPUT_NEUTRO)}
    ultimo_seq = {addr_j1: -1, addr_j2: -1}

    sock.setblocking(False)   # não travar o loop esperando pacote
    clock = pg.time.Clock()
    seq_estado = 0

    while not jogo.encerrada:
        # 1) TODO: drenar TODOS os pacotes de input que chegaram (socket é non-blocking,
        #    então leia em loop até dar BlockingIOError). Pra cada pacote "input":
        #    se for de um jogador conhecido E for mais_novo que o último seq dele,
        #    atualiza ultimo_seq[addr] e guarda em inputs[addr]. Ignora pacote velho/repetido.

        # 2) TODO: rodar 1 frame de simulação com os inputs mais recentes dos 2 jogadores.
        #    Use o método jogo.passo(in_j1, in_j2) que você cria no telaPrincipal (Fase 2).
        #    Ele devolve o dict de estado.

        # 3) TODO: numerar o estado (seq_estado crescente) e mandar pros 2 endereços.

        clock.tick(FPS)

    print("partida encerrada")
    sock.close()


if __name__ == "__main__":
    main()
