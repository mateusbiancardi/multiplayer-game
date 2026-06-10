import sys
import rede.configRede as config
import rede.protocolo as pt

import socket
import pygame as pg

from rede.protocolo import enviar_msg, receber_msg, mais_novo
from telaPrincipal import telaPrincipal

FPS = 60
PERSONAGENS_VALIDOS = (1, 2, 3, 4)

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


def espera_jogadores(sock: socket.socket) -> list:
    print("Esperando jogadores")
    lista = []

    while len(lista) < 2:
        try:
            msg, addr = pt.receber_msg(sock, pt.BUFSIZE)
        except OSError as e:
            print(f"[servidor] erro de socket ao esperar jogadores: {e}")
            continue

        if msg is None:  # pacote corrompido — ignora
            continue

        if msg.get("tipo") == "hello" and addr not in lista:
            lista.append(addr)
            print(f"Adicionado: {addr[0]}:{addr[1]}")
        elif addr in lista:
            print(f"Jogador {addr[0]}:{addr[1]} já conectado. Ignorando.")

    return lista


def espera_personagem(sock: socket.socket, addr_j1: tuple, addr_j2: tuple) -> list:
    print("Esperando escolha de personagem")
    personagens = {}

    while len(personagens) < 2:
        try:
            msg, addr = pt.receber_msg(sock, pt.BUFSIZE)
        except OSError as e:
            print(f"[servidor] erro de socket ao esperar personagem: {e}")
            continue

        if msg is None:
            continue

        if msg.get("tipo") == "personagem" and addr in (addr_j1, addr_j2):
            escolha = msg.get("personagem")
            if escolha in PERSONAGENS_VALIDOS:
                personagens[addr] = escolha
                print(f"Jogador {addr[0]}:{addr[1]} escolheu personagem {escolha}")
            else:
                # escolha invalida — assume guerreiro (1) para nao travar a partida
                personagens[addr] = 1
                print(f"Jogador {addr[0]}:{addr[1]} mandou escolha invalida ({escolha}); usando 1")
        elif addr not in (addr_j1, addr_j2):
            print(f"Mensagem de {addr[0]}:{addr[1]} ignorada. Jogador não conectado.")

    return [personagens[addr_j1], personagens[addr_j2]]


def loop_partida(sock, addr_j1, addr_j2, escolhidos):
    jogo = telaPrincipal(None, escolhidos)  # 'tela' = None: servidor não desenha

    # guarda o último input de cada jogador (e o último seq pra descartar pacote velho)
    inputs = {addr_j1: dict(INPUT_NEUTRO), addr_j2: dict(INPUT_NEUTRO)}
    ultimo_seq = {addr_j1: -1, addr_j2: -1}

    sock.setblocking(False)
    clock = pg.time.Clock()
    seq_estado = 0

    while not jogo.encerrada:
        # 1) drena TODOS os inputs que chegaram (socket nao-bloqueante)
        while True:
            try:
                msg, addr = pt.receber_msg(sock, pt.BUFSIZE)
            except BlockingIOError:
                break  # fila vazia — sai do dreno
            except OSError as e:
                print(f"[servidor] erro de socket no dreno de input: {e}")
                break

            if msg is None:  # pacote corrompido
                continue
            if msg.get("tipo") != "input" or addr not in inputs:
                continue
            if not mais_novo(msg.get("seq", -1), ultimo_seq[addr]):
                continue

            novo_input = msg.get("input")
            if isinstance(novo_input, dict):  # so aceita input bem formado
                ultimo_seq[addr] = msg["seq"]
                inputs[addr] = novo_input

        # 2) roda 1 frame de simulacao (servidor autoritativo)
        try:
            estado = jogo.passo(inputs[addr_j1], inputs[addr_j2])
        except Exception as e:
            # um erro na simulacao nao deve matar o servidor silenciosamente
            print(f"[servidor] erro na simulacao: {e}")
            raise

        # 3) numera e envia o estado para os 2 clientes (enviar_msg ja trata falha de envio)
        estado["seq"] = seq_estado
        pacote = {"tipo": "estado", "seq": seq_estado, "estado": estado}
        enviar_msg(sock, pacote, addr_j1)
        enviar_msg(sock, pacote, addr_j2)
        seq_estado += 1

        clock.tick(FPS)

    # manda o estado final algumas vezes extra: UDP pode perder o ultimo pacote
    # e o cliente precisa do "encerrada" para mostrar a tela de vitoria.
    estado["encerrada"] = True
    for _ in range(5):
        enviar_msg(sock, {"tipo": "estado", "seq": seq_estado, "estado": estado}, addr_j1)
        enviar_msg(sock, {"tipo": "estado", "seq": seq_estado, "estado": estado}, addr_j2)
        seq_estado += 1
        clock.tick(FPS)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(config.SERVER_ADDRESS)
    except OSError as e:
        # porta ja em uso, endereco invalido, sem permissao, etc.
        print(f"[servidor] nao foi possivel fazer bind em {config.SERVER_ADDRESS}: {e}")
        sock.close()
        sys.exit(1)

    print(f"servidor UDP em {config.SERVER_ADDRESS[0]}:{config.SERVER_ADDRESS[1]}")

    try:
        addr_j1, addr_j2 = espera_jogadores(sock)

        pg.init()  # inicia pygame sem abrir janela (servidor nao desenha)

        escolhidos = espera_personagem(sock, addr_j1, addr_j2)
        print(f"Personagens escolhidos: {escolhidos[0]} (jogador 1), {escolhidos[1]} (jogador 2)")
        enviar_msg(sock, {"tipo": "personagem_escolhido"}, addr_j1)
        enviar_msg(sock, {"tipo": "personagem_escolhido"}, addr_j2)

        loop_partida(sock, addr_j1, addr_j2, escolhidos)
        print("Partida encerrada")
    except KeyboardInterrupt:
        print("\n[servidor] encerrado pelo usuario (Ctrl+C)")
    finally:
        sock.close()
        pg.quit()


if __name__ == "__main__":
    main()
