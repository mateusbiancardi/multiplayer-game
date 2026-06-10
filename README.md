# Arena Medieval — Multiplayer em Rede 🎮

Jogo de arena 2D para **2 jogadores pela rede**, feito para a disciplina de
Redes.

O jogo nasceu como um projeto local (2 jogadores no mesmo teclado) e foi
transformado em um jogo **cliente-servidor** com **servidor autoritativo** sobre
**UDP**.

![Jogo](https://pbs.twimg.com/media/FjtZrsuWYAMup-8?format=png&name=medium)

## Descrição

Cada jogador escolhe um personagem (Guerreiro, Mago, Xamã ou Arqueiro) e luta
contra o outro com movimentação e habilidades. Vence quem zerar a vida do
adversário; se o tempo acabar, vence quem tiver mais vida.

A arquitetura segue o modelo de **host**: um dos jogadores roda o servidor e um
cliente na mesma máquina; o outro roda apenas um cliente e conecta pelo IP do
host.

```
   Máquina do host (Jogador 1)        Máquina do Jogador 2
   ┌──────────────────┐
   │   servidor.py    │ ◄───────────────  cliente.py  (Jogador 2)
   │       ▲          │     rede UDP
   │       │          │
   │   cliente.py     │  (Jogador 1)
   └──────────────────┘
```

- O **servidor** roda toda a lógica do jogo (movimento, ataques, dano, tempo).
  É a única "verdade" — não há duas simulações divergindo.
- Os **clientes** são simples: leem o teclado/mouse, mandam o input, recebem o
  estado e desenham. Não calculam nada do jogo.

## Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Biblioteca gráfica:** [pygame](https://www.pygame.org/)
- **Rede:** módulo `socket` da biblioteca padrão (UDP / `SOCK_DGRAM`)
- **Serialização:** módulo `json` da biblioteca padrão

## Como Executar

### Requisitos

- Python 3.10 ou superior
- pygame (ver `requirements.txt`)

### Instruções de Execução

1. Clone o repositório:

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd PythonGame
   ```

2. (Opcional, recomendado) crie um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Linux/Mac
   venv\Scripts\activate           # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o servidor** (na máquina do host):

   ```bash
   python3 servidor.py
   ```

5. **Execute os clientes** (um para cada jogador):

   ```bash
   # No host, conectando no próprio servidor:
   python3 cliente.py 127.0.0.1

   # No outro jogador, conectando no IP do host:
   python3 cliente.py <IP_DO_HOST>
   ```

   Se nenhum IP for passado, o cliente usa `127.0.0.1` por padrão.
   Descubra o IP do host com `ip addr` (Linux) ou `ipconfig` (Windows).
   A porta usada é a `1234` (em `rede/configRede.py`); libere-a no firewall caso
   a conexão entre máquinas diferentes não funcione.

### Controles

| Ação            | Tecla / botão     |
|-----------------|-------------------|
| Mover           | W A S D           |
| Ataque 1        | Q                 |
| Ataque 2        | E                 |
| Disparo (mira)  | Clique do mouse   |
| Sair            | ESC ou fechar (X) |

## Como Testar

### Teste manual (jogo completo)

1. Abra **3 terminais** na mesma máquina.
2. Terminal 1: `python3 servidor.py`
3. Terminal 2: `python3 cliente.py 127.0.0.1`
4. Terminal 3: `python3 cliente.py 127.0.0.1`
5. Em cada cliente: pressione **espaço** no menu, escolha um personagem com as
   setas + **espaço**. Quando os dois escolherem, a partida começa.
6. Verifique que o movimento de um cliente aparece no outro (mesmo estado nos
   dois) e que a tela de vitória aparece ao fim da partida.

### Teste de robustez (tratamento de erros)

- **Servidor sem cliente:** suba só o servidor; ele fica em "Esperando
  jogadores" sem travar.
- **Cliente sem servidor:** suba só o cliente e passe pelo menu/seleção; ele
  mostra "Aguardando outro jogador" e, após o timeout (60s), desiste com uma
  mensagem em vez de travar.
- **Porta ocupada:** suba dois servidores; o segundo informa que não conseguiu
  fazer `bind` e encerra com mensagem clara, sem stack trace.
- **Pacote corrompido:** servidor e cliente ignoram pacotes UDP que não são JSON
  válido e continuam rodando.
- **Ctrl+C:** encerra servidor e cliente de forma limpa (fecha socket e pygame).

## Funcionalidades Implementadas

- Servidor **autoritativo** sobre **UDP** rodando a lógica do jogo headless.
- **Handshake** de conexão (`hello`) e identificação dos jogadores por endereço.
- **Seleção de personagem em rede**: cada cliente escolhe o seu e envia ao
  servidor.
- **Sincronização de estado** a ~60 FPS: o servidor envia o estado completo
  (posições, vidas, direção, tempo, desenhos de ataque) e o cliente só desenha.
- **Números de sequência** para descartar pacotes atrasados/duplicados.
- **Sockets não-bloqueantes** com drenagem da fila, ficando sempre com o pacote
  mais recente.
- Telas de **menu inicial**, **seleção**, **aguardando outro jogador** e
  **resultado final** integradas ao fluxo de rede.
- **Tratamento de erros**: falha de `bind`, pacotes malformados, falha de envio,
  servidor indisponível (timeout) e encerramento limpo.

## Possíveis Melhorias Futuras

- **Detecção de desconexão** de um jogador no meio da partida (heartbeat) e tela
  de "jogador saiu".
- **Reconexão** automática do cliente.
- **Interpolação / predição** no cliente para suavizar o movimento sob perda de
  pacotes.
- **Delta de estado** (enviar só o que mudou) para reduzir banda.
- **Lobby** para escolha de partida e mais jogadores.
