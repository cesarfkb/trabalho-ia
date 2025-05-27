# Mutorere (Jogo Tradicional Māori)

Mutorere é um jogo de tabuleiro tradicional Māori para dois jogadores. Este projeto é uma implementação digital do jogo.

## Regras do Jogo

### 1. Peças

- Cada jogador controla **quatro peças**, chamadas _perepere_. Existem peças brancas e pretas.

### 2. O Tabuleiro

- O tabuleiro consiste em **oito pontos externos** (_kewai_) dispostos em círculo e **um ponto central** (_pūtahi_).

### 3. Preparação

- No início do jogo:
  - Cada jogador coloca suas quatro peças em **quatro kewai consecutivos**.
  - O _pūtahi_ (centro) permanece vazio.

### 4. Turnos & Movimentação

- Os jogadores se revezam, alternando entre si.
- Em cada turno, o jogador deve:
  - Mover uma de suas peças para um **ponto adjacente vazio**.
  - O movimento é permitido apenas para **pontos diretamente conectados (adjacentes)**.
  - Uma peça pode mover-se para o _pūtahi_ (centro) **apenas se estiver adjacente a uma peça do oponente**.

### 5. Objetivo

- O vencedor é o jogador que **bloquear todas as peças do oponente**, deixando-o sem movimentos legais.

### 6. Observações Adicionais

- As peças **não podem pular sobre outras peças**.
- Apenas **uma peça pode ocupar um ponto por vez**.

---

## Estrutura do Projeto

- `main.py` — Ponto de entrada, executa o loop do jogo
- `board.py` — Desenho do tabuleiro e lógica de estado
- `ai.py` — Lógica de IA aleatória e IA Minimax
