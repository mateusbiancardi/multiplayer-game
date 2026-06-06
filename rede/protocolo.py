import json
import socket

BUFSIZE = 4096


def enviar_msg(sock: socket.socket, obj: dict, addr: tuple | None = None) -> None:
    # Encode no dict como Json e envia
    serialized = json.dumps(obj).encode("utf-8")
    if addr is None:
        sock.send(serialized)
    else:
        sock.sendto(serialized, addr)


def receber_msg(sock: socket.socket, bufsize: int = 4096) -> tuple[dict, tuple]:
    # sock.setblocking(False)

    dados, addr = sock.recvfrom(bufsize)
    return json.loads(dados.decode("utf-8")), addr


def mais_novo(seq_recebido: int, ultimo_seq: int) -> bool:
    # Rertorna True se seq_recebido é mais novo que ultimo_seq

    return seq_recebido > ultimo_seq
