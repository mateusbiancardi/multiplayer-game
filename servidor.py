import os
from configJogo import ConfigJogo
import rede.configRede as config
import rede.protocolo as pt

os.environ["SDL_VIDEODRIVER"] = "dummy"  # tem que vir ANTES de importar/iniciar pygame

import socket
import pygame as pg

from rede.protocolo import enviar_msg, receber_msg, mais_novo
from telaPrincipal import telaPrincipal

FPS = 60

# input "neutro" — usado enquanto um cliente ainda não mandou nada nesse frame
INPUT_NEUTRO = {
    "left": False,
    "right": False,
    "up": False,
    "down": False,
    "atk1": False,
    "atk2": False,
    "click": False,
    "mouse": [0, 0],
}


def espera_jogadores(sock: socket.socket) -> tuple[int, int]:
    print("Esperando jogadores")
    lista = []

    while len(lista) < 2:
        msg, addr = pt.receber_msg(sock, pt.BUFSIZE)
        if msg.get("tipo") == "hello" and addr not in lista:
            lista.append(addr)
            print(f"Adicionado: {addr[0]}:{addr[1]}")
        elif addr in lista:
            print(f"Jogador {addr[0]}:{addr[1]} já conectado. Ignorando.")

    return lista


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(config.SERVER_ADDRESS)
    print(f"servidor UDP em {config.SERVER_ADDRESS[0]}:{config.SERVER_ADDRESS[1]}")

    addr_j1, addr_j2 = espera_jogadores(sock)

    pg.init()
    pg.display.set_mode((ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_TELA))
    # Fase 3: personagens hardcoded pra testar a rede. Fase 5: receber escolha de cada cliente.
    escolhidos = [1, 2]  # [char do j1, char do j2]
    jogo = telaPrincipal(None, escolhidos)  # 'tela' = None: servidor não desenha

    # guarda o último input de cada jogador (e o último seq pra descartar pacote velho)
    inputs = {addr_j1: dict(INPUT_NEUTRO), addr_j2: dict(INPUT_NEUTRO)}
    ultimo_seq = {addr_j1: -1, addr_j2: -1}

    sock.setblocking(False)
    clock = pg.time.Clock()
    seq_estado = 0

    while not jogo.encerrada:
        try:
            while True:
                msg, addr = pt.receber_msg(sock, pt.BUFSIZE)
                if addr in inputs and mais_novo(msg.get("seq", -1), ultimo_seq[addr]):
                    ultimo_seq[addr] = msg["seq"]
                    inputs[addr] = msg["input"]

        except BlockingIOError:
            pass

        estado = jogo.passo(inputs[addr_j1], inputs[addr_j2])

        estado["seq"] = seq_estado
        enviar_msg(
            sock, {"tipo": "estado", "seq": seq_estado, "estado": estado}, addr_j1
        )
        enviar_msg(
            sock, {"tipo": "estado", "seq": seq_estado, "estado": estado}, addr_j2
        )
        seq_estado += 1

        clock.tick(FPS)

    print("partida encerrada")
    sock.close()


if __name__ == "__main__":
    main()
