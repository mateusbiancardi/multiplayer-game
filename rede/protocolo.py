import json
import socket

BUFSIZE = 4096


def enviar_msg(sock: socket.socket, obj: dict, addr: tuple | None = None) -> bool:
    # Encode o dict como JSON e envia. Retorna True se conseguiu enviar.
    try:
        serialized = json.dumps(obj).encode("utf-8")
    except (TypeError, ValueError) as e:
        # objeto nao serializavel (ex: tipo pygame no dict de estado)
        print(f"[protocolo] erro ao serializar mensagem: {e}")
        return False

    try:
        if addr is None:
            sock.send(serialized)
        else:
            sock.sendto(serialized, addr)
        return True
    except OSError as e:
        # destino inalcancavel, socket fechado, etc. Em UDP nao queremos derrubar
        # o loop por causa de um envio que falhou — proximo frame tenta de novo.
        print(f"[protocolo] erro ao enviar para {addr}: {e}")
        return False


def receber_msg(sock: socket.socket, bufsize: int = 4096) -> tuple[dict | None, tuple | None]:
    # Recebe 1 datagrama. Devolve (dict, addr). Se o pacote estiver corrompido
    # (JSON invalido / bytes nao-utf8), devolve (None, addr) para o chamador ignorar.
    # BlockingIOError NAO e tratado aqui de proposito: os loops nao-bloqueantes
    # dependem dela para saber que a fila esvaziou.
    dados, addr = sock.recvfrom(bufsize)
    try:
        return json.loads(dados.decode("utf-8")), addr
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"[protocolo] pacote malformado de {addr}: {e}")
        return None, addr


def mais_novo(seq_recebido: int, ultimo_seq: int) -> bool:
    # Retorna True se seq_recebido e mais novo que ultimo_seq (descarta reordenado/repetido)
    return seq_recebido > ultimo_seq
