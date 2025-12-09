import pygame
from constantes import QUADRADO, CINZA

class Peca:
  PADDING = 15 # Espaço entre a peça e a borda do quadrado
  BORDA = 2    # Espessura da borda da peça

  def __init__(self, linha, coluna, cor):
    self.linha = linha
    self.coluna = coluna
    self.cor = cor
    self.dama = False # Por enquanto todas são peças comuns
    self.x = 0
    self.y = 0
    self.calc_pos()

  # Calcula a posição exata do CENTRO da peça na tela
  def calc_pos(self):
    self.x = QUADRADO * self.coluna + QUADRADO // 2
    self.y = QUADRADO * self.linha + QUADRADO // 2

  # Desenha o círculo na tela
  def desenhar(self, janela):
    raio = QUADRADO // 2 - self.PADDING
      
    # Desenha a borda (círculo cinza atrás)
    pygame.draw.circle(janela, CINZA, (self.x, self.y), raio + self.BORDA)
      
    # Desenha a peça principal
    pygame.draw.circle(janela, self.cor, (self.x, self.y), raio)

  def mover(self, linha, coluna):
    self.linha = linha
    self.coluna = coluna
    self.calc_pos()