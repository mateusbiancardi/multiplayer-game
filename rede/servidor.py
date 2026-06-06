import socket
import protocolo as pt
import config as c


def espera_jogadores():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(c.SERVER_ADDRESS)
    sock.bind(c.SERVER_ADDRESS)

    print("Esperando jogadores")
    lista = []

    while len(lista) < 2:
        msg, addr = pt.receber_msg(sock, pt.BUFSIZE)
        if msg.get("type") == "hello" and addr not in lista:
            addr = addr[1]
            lista.append(addr)
            print(f"Adicionado: {addr}")

    return lista


espera_jogadores()
