# Multiplayer — Roadmap (trabalho de redes)

Arquitetura escolhida: **cliente-servidor com servidor autoritativo**, transporte **UDP**,
**um jogador hospeda** (roda servidor + cliente na mesma máquina; o outro só conecta).

UDP: datagrama (1 envio = 1 recebimento, sem precisar delimitar), sem conexão, pode perder
ou reordenar pacote. Como mandamos input+estado TODO frame, perda é tolerável (próximo frame
corrige). Contra reordenação: campo `seq` (número de sequência) — descarta pacote mais velho
que o último visto. Servidor descobre o endereço de cada cliente pelo `hello` que chega.

```
   Cliente 1 (jogador host)            Cliente 2 (jogador remoto)
   - lê SEU teclado/mouse              - lê SEU teclado/mouse
   - envia INPUT  ───────┐      ┌───── envia INPUT
   - recebe ESTADO       │      │      recebe ESTADO
   - desenha             v      v      desenha
                    ┌─────────────────┐
                    │     SERVIDOR    │   (autoritativo, SEM render)
                    │  roda a lógica  │
                    │ do telaPrincipal│
                    └─────────────────┘
```

Por frame:
1. Cada cliente lê só o PRÓPRIO input → manda pro servidor.
2. Servidor junta os 2 inputs → roda `tratamentoEventos` + `ataques` + `movimento` + `endGame`.
3. Servidor serializa o ESTADO (posições, vidas, ataques a desenhar, tempo) → manda pros 2 clientes.
4. Cada cliente desenha o que recebeu.

Servidor manda a VERDADE. Cliente é "burro": input entra, pixels saem. Anti-cheat de graça,
sem desync (o `time()` espalhado no código só roda no servidor, então não tem 2 simulações divergindo).

---

## Mensagens (protocolo)

Tudo JSON, 1 datagrama UDP por mensagem (sem `\n`, a fronteira do datagrama já separa).
Todo pacote leva `"tipo"` e, quando for stream de jogo, um `"seq"` crescente.

### HELLO (cliente → servidor), 1 vez ao conectar
```json
{"tipo": "hello"}
```
Server registra o endereço (ip,porta) do remetente. 1o = jogador 1, 2o = jogador 2.

### INPUT (cliente → servidor), todo frame
```json
{"tipo": "input", "seq": 137,
 "left": false, "right": true, "up": false, "down": false,
 "atk1": false, "atk2": false, "click": false, "mouse": [320, 200]}
```
- `atk1` = tecla E (jogador 1) ou M (jogador 2). `atk2` = Q (j1) ou N (j2).
- O servidor sabe QUEM é cada cliente (slot 1 ou 2), então mapeia pro personagem certo.
- Cliente manda booleano de tecla CRUA. Quem decide velocidade/cooldown é o servidor.

### ESTADO (servidor → cliente), todo frame
```json
{"seq":2050,
 "xP1":390,"yP1":336,"xP2":780,"yP2":336,
 "p1Vida":40,"p2Vida":20,"p1VidaTotal":40,"p2VidaTotal":20,
 "p1":1,"p2":2,
 "xEsquerdaP1":true,"xDireitaP1":false,"xEsquerdaP2":true,"xDireitaP2":false,
 "tempoJogo":58,"encerrada":false,
 "desenhos":[ ["circle",[0,0,0],[420,361],50,5], ["sprite","minion",300,200] ]}
```
- `desenhos` = lista de comandos de render dos ATAQUES (círculos, sprites de lacaio/berserker/flecha).
  O servidor gera essa lista no lugar de chamar `pg.draw`/`blit`. O cliente executa.
- Personagens P1/P2 o cliente desenha sozinho (sabe char id + direção → escolhe sprite).

---

## Fases (faça nessa ordem, testando cada uma)

**Fase 0 — protocolo isolado.** Implementa `rede/protocolo.py` (`enviar_msg`, `receber_msg`, `mais_novo`).
Testa com 2 scripts bobos: um faz `sendto` de um dict, o outro `recvfrom` e imprime. Sem pygame ainda.

**Fase 1 — hello/conexão.** `servidor.py` faz bind UDP e espera 2 `hello` (guarda os endereços).
`cliente.py` manda `hello`. Sem jogo ainda: só prova que os 3 processos se falam.

**Fase 2 — refatorar `telaPrincipal` (ver seção abaixo).** Separa INPUT, LÓGICA e RENDER.
Testa que o jogo LOCAL ainda roda igual depois do refactor (não quebrou nada).

**Fase 3 — servidor roda a lógica.** Servidor cria 1 `telaPrincipal` headless, recebe os 2 inputs,
roda um passo de simulação, manda estado. Personagens hardcoded (ex: p1=1, p2=2) pra testar.

**Fase 4 — cliente desenha estado.** Cliente manda input local, recebe estado, desenha. Joga!

**Fase 5 (opcional) — seleção de personagem em rede.** Cada cliente escolhe seu char, manda
pro servidor, servidor começa a partida com os 2. Antes disso, deixa hardcoded.

**Fase 6 (opcional) — robustez.** Tratar desconexão, tela de "esperando jogador 2", FPS fixo (clock.tick).

---

## Refactor do `telaPrincipal` (Fase 2) — passos exatos

Hoje `rodar()` faz tudo junto. Você vai separar em métodos que rodam em lugares diferentes:

1. **Input vira parâmetro.** Mude:
   ```python
   def tratamentoEventos(self):
       events = pg.event.get()
       ... pg.key.get_pressed()[pg.K_a] ...
   ```
   para:
   ```python
   def tratamentoEventos(self, in1, in2):
       # in1, in2 = dicts de input (ver protocolo). NADA de pg.event aqui.
       # troca pg.key.get_pressed()[pg.K_a]  ->  in1["left"]
       #       pg.key.get_pressed()[pg.K_d]  ->  in1["right"]   (etc)
       #       tecla E (j1) -> in1["atk1"] ;  Q (j1) -> in1["atk2"]
       #       setas (j2)   -> in2["left/right/up/down"]
       #       M (j2) -> in2["atk1"] ;  N (j2) -> in2["atk2"]
       #       mouse: in1["click"]/in1["mouse"] e in2["click"]/in2["mouse"]
       # MANTÉM toda a lógica de cooldown/duracaoCast/primeiroCast aqui (é estado do jogo = servidor).
   ```
   A leitura de teclado CRU (pg.key.get_pressed) sai daqui e vai pro CLIENTE (função nova
   `ler_entrada_local()` no cliente.py).

2. **Render dos ataques vira lista de comandos.** Dentro de `ataques()` e `tempo()`, troca:
   ```python
   pg.draw.circle(self.tela, cor, (x,y), r, w)   ->  self.desenhos.append(["circle", cor, [x,y], r, w])
   self.tela.blit(self.lacaio, (x,y))            ->  self.desenhos.append(["sprite", "minion", x, y])
   self.tela.blit(self.berserker, (x,y))         ->  self.desenhos.append(["sprite", "berserker", x, y])
   ```
   Zera a lista no começo de cada passo: `self.desenhos = []`.
   A LÓGICA de dano (mexe em p1Vida/p2Vida) fica intacta. Só os desenhos viram dados.

3. **Passo de simulação (servidor).** Cria um método sem render:
   ```python
   def passo(self, in1, in2):
       self.desenhos = []
       self.tratamentoEventos(in1, in2)
       self.ataques()
       self.movimento()
       self.endGame()
       return self.serializar_estado()
   ```

4. **Serializar/desenhar estado.** Dois métodos novos:
   ```python
   def serializar_estado(self):  # servidor: monta o dict de ESTADO (ver protocolo)
       ...
   def desenhar_estado(self, estado):  # cliente: lê o dict e desenha tudo na self.tela
       ...   # bg, executa estado["desenhos"], desenha sprites P1/P2 (escolhe pela direção),
             # texto de vida e tempo
   ```
   Repare: `carregarPersonagem`/`personagem` (escolha de sprite + flip) vira base do `desenhar_estado`,
   roda no CLIENTE. `criar_mapa`/blocos podem rodar no cliente pra desenhar o mapa (são estáticos).

5. **Headless no servidor.** O servidor não tem janela. Antes de `pg.init()` no servidor, use o
   driver dummy pra pygame não abrir tela:
   ```python
   import os
   os.environ["SDL_VIDEODRIVER"] = "dummy"
   ```
   (Você ainda pode precisar de `pg.font`/`pg.image` — com dummy funciona. Se der ruim, mova o
   cálculo de tempo/fonte 100% pro cliente.)

Depois do refactor, dá pra manter um modo LOCAL (1 máquina) chamando `passo()` com os 2 inputs
lidos localmente — útil pra debugar sem rede.

---

## Como rodar (quando pronto)

```bash
# Máquina do host (jogador 1):
python servidor.py            # terminal 1
python cliente.py 127.0.0.1   # terminal 2  (conecta no próprio servidor)

# Máquina do jogador 2:
python cliente.py <IP_DO_HOST>
```
Descobre o IP do host na mesma rede com `ip addr` (Linux) / `ipconfig` (Windows).
Libera a porta no firewall se não conectar.
