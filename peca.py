import pygame
from constantes import TAMANHO, PRETO, COR_JOGADOR_1, COR_JOGADOR_2

class Peca:
  PADDING = 10 # Espaço entre a peça e a borda do quadrado
  BORDA = 2    # Espessura da borda da peça

  def __init__(self, linha, coluna, cor):
    self.linha = linha
    self.coluna = coluna
    self.cor = cor
    self.dama = False # Por enquanto todas são peças comuns6
    self.x = 0
    self.y = 0
    self.calc_pos()

  # Calcula a posição exata do CENTRO da peça na tela
  def calc_pos(self):
    self.x = TAMANHO * self.coluna + TAMANHO // 2
    self.y = TAMANHO * self.linha + TAMANHO // 2

  # Desenha o círculo na tela
  def desenhar(self, janela):
    rect_peca = pygame.Rect(self.x - TAMANHO // 2 + self.PADDING//2, self.y - TAMANHO // 4 - self.PADDING//2, TAMANHO-self.PADDING, TAMANHO // 2 + self.PADDING)
    rect_sombra = rect_peca.move(0, 8)

    repete = 1 if self.dama else 0
    if repete == 1:
      rect_peca = rect_peca.move(0, -12)
      rect_sombra = rect_sombra.move(0, -12)

    while repete >= 0:
      sobe = repete * 12
      pygame.draw.ellipse(janela, (180, 180, 180, 100), rect_sombra.move(0, sobe))
      pygame.draw.ellipse(janela, PRETO , rect_sombra.move(0, sobe), self.BORDA)

      pygame.draw.ellipse(janela, self.cor, rect_peca.move(0, sobe))
      pygame.draw.ellipse(janela, PRETO , rect_peca.move(0, sobe), self.BORDA)

      repete -=1


  def mover(self, linha, coluna):
    self.linha = linha
    self.coluna = coluna
    if (self.linha == 0 and self.cor == COR_JOGADOR_1) or \
       (self.linha == 7 and self.cor == COR_JOGADOR_2):
      self.dama = True
    self.calc_pos()