import sys
import socket
from time import time

import pygame as pg

import rede.configRede as config
import rede.protocolo as pt
from rede.protocolo import enviar_msg, receber_msg, mais_novo

from configJogo import ConfigJogo
from telaPrincipal import telaPrincipal
from telaInicial import Menu
from selecaoPersonagem import telaSelecao
from telaAguardando import Aguardando
from telaFinal import telaFinal

FPS = 60
TIMEOUT_CONEXAO = 60  # segundos esperando o servidor antes de desistir


def ler_entrada_local() -> dict:
    # le o estado atual do teclado/mouse e monta o dict de input.
    # a fila de eventos ja foi bombeada no loop (pg.event.get), entao
    # get_pressed ja reflete o estado certo das teclas.
    teclas = pg.key.get_pressed()
    return {
        "left": bool(teclas[pg.K_a]),
        "right": bool(teclas[pg.K_d]),
        "up": bool(teclas[pg.K_w]),
        "down": bool(teclas[pg.K_s]),
        "atk1": bool(teclas[pg.K_q]),
        "atk2": bool(teclas[pg.K_e]),
        "click": bool(pg.mouse.get_pressed()[0]),
        "mouse": list(pg.mouse.get_pos()),
    }


def quer_sair() -> bool:
    # True se o jogador fechou a janela (X) ou apertou ESC
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return True
    if pg.key.get_pressed()[pg.K_ESCAPE]:
        return True
    return False


def espera_inicio(sock, tela, clock) -> bool:
    # mostra "aguardando outro jogador" ate o servidor comecar a mandar estado.
    # retorna True se conectou, False se deu timeout / o jogador fechou a janela.
    aguardando = Aguardando(tela)
    limite = time() + TIMEOUT_CONEXAO

    while True:
        if quer_sair():
            return False

        if time() > limite:
            print("[cliente] servidor nao respondeu a tempo. Verifique se ele esta rodando.")
            return False

        aguardando.desenha()
        pg.display.flip()

        # drena o que chegou; o primeiro "estado" significa que a partida comecou.
        # (nao dependo do 'personagem_escolhido' que e mandado 1x so e pode se perder)
        while True:
            try:
                msg, addr = pt.receber_msg(sock, pt.BUFSIZE)
            except BlockingIOError:
                break
            except OSError as e:
                print(f"[cliente] erro de socket ao aguardar: {e}")
                break

            if msg is None:
                continue
            if msg.get("tipo") == "estado":
                return True

        clock.tick(FPS)


def main():
    # IP do servidor: 1o argumento da linha de comando, ou 127.0.0.1 por padrao
    ip = sys.argv[1] if len(sys.argv) >= 2 else "127.0.0.1"
    servidor = (ip, config.SERVER_ADDRESS[1])

    pg.init()
    tela = pg.display.set_mode((ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_TELA))

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(servidor)
    except OSError as e:
        print(f"[cliente] nao foi possivel criar/conectar o socket em {servidor}: {e}")
        pg.quit()
        sys.exit(1)

    clock = pg.time.Clock()

    try:
        # 1) handshake
        enviar_msg(sock, {"tipo": "hello"})

        # 2) menu inicial (local)
        Menu(tela).rodar()

        # 3) selecao de personagem (cada cliente escolhe o seu)
        personagem = None
        while personagem is None:
            personagem = telaSelecao(tela).rodar()

        sock.setblocking(False)
        enviar_msg(sock, {"tipo": "personagem", "personagem": personagem})

        # 4) espera o outro jogador / o servidor comecar
        if not espera_inicio(sock, tela, clock):
            return  # timeout ou janela fechada -> cai no finally e limpa tudo

        # 5) loop principal: manda input, recebe estado, desenha
        jogo = telaPrincipal(tela, [1, 1])  # [1,1] e placeholder; o estado define os chars
        seq_input = 0
        ultimo_estado = None
        ultimo_seq_estado = -1

        while True:
            if quer_sair():
                break

            enviar_msg(sock, {"tipo": "input", "seq": seq_input, "input": ler_entrada_local()})
            seq_input += 1

            # drena estados; fica com o mais novo
            while True:
                try:
                    msg, addr = pt.receber_msg(sock, pt.BUFSIZE)
                except BlockingIOError:
                    break
                except OSError as e:
                    print(f"[cliente] erro de socket: {e}")
                    break

                if msg is None:
                    continue
                if msg.get("tipo") == "estado" and mais_novo(msg.get("seq", -1), ultimo_seq_estado):
                    ultimo_estado = msg.get("estado")
                    ultimo_seq_estado = msg.get("seq")

            if ultimo_estado is not None:
                jogo.desenhaJogo(ultimo_estado)
                pg.display.flip()
                if ultimo_estado.get("encerrada"):
                    break

            clock.tick(FPS)

        # 6) tela final (so se a partida terminou de verdade)
        if ultimo_estado is not None and ultimo_estado.get("encerrada"):
            telaFinal(tela, ultimo_estado["p1Vida"], ultimo_estado["p2Vida"]).rodar_final()

    except KeyboardInterrupt:
        print("\n[cliente] encerrado pelo usuario (Ctrl+C)")
    finally:
        sock.close()
        pg.quit()


if __name__ == "__main__":
    main()
