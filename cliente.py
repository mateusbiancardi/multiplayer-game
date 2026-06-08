import rede.configRede as config
import sys
import socket
import pygame as pg
import rede.protocolo as pt

from rede.protocolo import enviar_msg, receber_msg, mais_novo
from configJogo import ConfigJogo
from telaPrincipal import telaPrincipal

FPS = 60


def ler_entrada_local() -> dict:
    inputs = {}

    pg.event.pump()

    teclas = pg.key.get_pressed()
    inputs["left"] = bool(teclas[pg.K_a])
    inputs["right"] = bool(teclas[pg.K_d])
    inputs["up"] = bool(teclas[pg.K_w])
    inputs["down"] = bool(teclas[pg.K_s])
    inputs["atk1"] = bool(teclas[pg.K_q])
    inputs["atk2"] = bool(teclas[pg.K_e])
    inputs["click"] = bool(pg.mouse.get_pressed()[0])
    inputs["mouse"] = pg.mouse.get_pos()

    return inputs


def main():
    # if len(sys.argv) < 2:
    #     print("uso: python cliente.py <IP_DO_SERVIDOR>")
    #     sys.exit(1)
    # servidor = (sys.argv[1], config.SERVER_ADDRESS[1])
    servidor = (config.SERVER_ADDRESS[0], config.SERVER_ADDRESS[1])

    pg.init()
    tela = pg.display.set_mode((ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_TELA))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.connect(servidor)

    enviar_msg(sock, {"tipo": "hello"})

    jogo = telaPrincipal(tela, [1, 1])

    sock.setblocking(False)
    clock = pg.time.Clock()
    seq_input = 0
    ultimo_estado = None
    ultimo_seq_estado = -1

    while True:
        inputs = ler_entrada_local()
        enviar_msg(sock, {"tipo": "input", "seq": seq_input, "input": inputs})
        seq_input += 1

        try:
            while True:
                msg, addr = pt.receber_msg(sock, pt.BUFSIZE)
                if msg.get("tipo") == "estado" and mais_novo(
                    msg.get("seq", -1), ultimo_seq_estado
                ):
                    ultimo_estado = msg.get("estado")
                    ultimo_seq_estado = msg.get("seq")
        except BlockingIOError:
            pass

        if ultimo_estado is not None:
            jogo.desenhaJogo(ultimo_estado)
            pg.display.flip()
            if ultimo_estado.get("encerrada"):
                break

        clock.tick(FPS)

    sock.close()
    pg.quit()


if __name__ == "__main__":
    main()
