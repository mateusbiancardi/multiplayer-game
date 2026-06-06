"""
cliente.py — cliente (UDP). Lê SEU input, manda pro servidor, recebe ESTADO, desenha.

Uso:
    python cliente.py <IP_DO_SERVIDOR>      (ex: python cliente.py 127.0.0.1)

Fluxo:
  1. Cria socket UDP, manda {"tipo":"hello"} pro servidor.
  2. Loop ~60 fps:
       - lê o input local (teclado/mouse DESTE jogador)
       - manda {"tipo":"input", ...} pro servidor
       - recebe o ESTADO mais recente que chegou
       - desenha o estado na tela
  3. Sai quando estado["encerrada"].

Importante: este cliente lê SÓ as teclas do próprio jogador. Mas qual jogador ele é?
  - Mais simples: ambos usam o MESMO esquema de teclas (ex: WASD + E/Q + mouse). O servidor
    sabe quem é slot 1 e slot 2 pela ordem de conexão; cada cliente sempre manda left/right/...
    como "atk1/atk2" e o servidor mapeia pro personagem certo. Recomendo isso.
  - (Alternativa: servidor responde com o slot no 'hello' e o cliente escolhe o set de teclas.)
"""

import sys
import socket
import pygame as pg

from rede.protocolo import enviar_msg, receber_msg, mais_novo
from configJogo import ConfigJogo
from telaPrincipal import telaPrincipal

PORTA = 5000
FPS = 60


def ler_entrada_local() -> dict:
    """Lê teclado/mouse deste jogador e devolve o dict de INPUT (ver protocolo).

    Use o MESMO esquema de teclas pros dois clientes (WASD + E/Q + clique). Campos do
    dict: left/right/up/down/atk1/atk2 (bool), click (bool), mouse ([x,y]).
    Dicas:
      - estado contínuo de teclas (segurar pra andar): pg.key.get_pressed()
      - clique é um EVENTO pontual: precisa varrer pg.event.get() e olhar MOUSEBUTTONUP
      - aproveite o pg.event.get() pra tratar pg.QUIT (fechar janela) também
      - posição do mouse: pg.mouse.get_pos() (manda como list, não tuple — JSON)
    """
    raise NotImplementedError("implementar ler_entrada_local")


def main():
    if len(sys.argv) < 2:
        print("uso: python cliente.py <IP_DO_SERVIDOR>")
        sys.exit(1)
    servidor = (sys.argv[1], PORTA)

    pg.init()
    tela = pg.display.set_mode((ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_TELA))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
    # 'connect' num socket UDP só fixa o destino padrão -> dá pra usar send/recv sem addr
    sock.connect(servidor)

    # 1) TODO: handshake — manda um {"tipo":"hello"} pro servidor te registrar.

    # telaPrincipal reaproveitado SÓ pra desenhar (mapa estático + método desenhar_estado).
    # Os personagens são definidos pelo estado que o servidor manda; o [1,1] aqui é só placeholder.
    jogo = telaPrincipal(tela, [1, 1])

    sock.setblocking(False)
    clock = pg.time.Clock()
    seq_input = 0
    ultimo_estado = None
    ultimo_seq_estado = -1

    while True:
        # 2) TODO: ler o input local, marcar tipo "input" + um seq crescente, e enviar.

        # 3) TODO: drenar os pacotes de estado que chegaram (loop até BlockingIOError) e
        #    ficar só com o mais novo (use mais_novo contra ultimo_seq_estado).

        # 4) TODO: se já tem algum estado, desenhar (jogo.desenhar_estado — método da Fase 2),
        #    dar flip na tela, e sair do loop quando o estado disser encerrada=True.

        clock.tick(FPS)

    sock.close()
    pg.quit()


if __name__ == "__main__":
    main()
