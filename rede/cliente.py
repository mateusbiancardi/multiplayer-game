import socket
import protocolo as pt
import config as c


def manda_mensagem():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(c.SERVER_ADDRESS)

    pt.enviar_msg(sock, {"type": "hello"}, c.SERVER_ADDRESS)


manda_mensagem()
