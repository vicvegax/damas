import pygame

from constantes import *
from peca import Peca

class Tabuleiro:
  def __init__(self):
    self.tabuleiro = []
    self.pecas_jogador_1 = 12
    self.pecas_jogador_2 = 12
    self.damas_jogador_1 = 0
    self.damas_jogador_2 = 0
    self.criar_tabuleiro()
    
  def quadrados(self, janela):
    janela.fill(MARROM)

    for linha in range(LINHAS):
      for coluna in range(linha % 2, COLUNAS, 2):
        pygame.draw.rect(janela, CREME, (coluna * TAMANHO, linha * TAMANHO, TAMANHO, TAMANHO))

  def criar_tabuleiro(self):
    for linha in range(LINHAS):
      self.tabuleiro.append([])
      for coluna in range(COLUNAS):
        # Regra: Peças ficam apenas nas linhas pares se a coluna for ímpar, e vice-versa
        # E apenas nas 3 primeiras e 3 últimas linhas  
        if coluna % 2 == ((linha + 1) % 2):
          if linha < 3:
            self.tabuleiro[linha].append(Peca(linha, coluna, COR_JOGADOR_2))
          elif linha > 4:
            self.tabuleiro[linha].append(Peca(linha, coluna, COR_JOGADOR_1))
          else:
            self.tabuleiro[linha].append(0)
        else:
          self.tabuleiro[linha].append(0)

  def desenhar(self, janela):
    self.quadrados(janela)

    for linha in range(LINHAS):
      for coluna in range(COLUNAS):
        peca = self.tabuleiro[linha][coluna]
        if peca != 0:
          peca.desenhar(janela)

  def obter_peca(self, linha, coluna):
    return self.tabuleiro[linha][coluna]
  
  def mover_peca(self, peca, linha, coluna):
    self.tabuleiro[peca.linha][peca.coluna], self.tabuleiro[linha][coluna] = self.tabuleiro[linha][coluna], self.tabuleiro[peca.linha][peca.coluna]

    peca.mover(linha, coluna)

  def remover(self, pecas):
    for peca in pecas:
      self.tabuleiro[peca.linha][peca.coluna] = 0
      if peca.cor != 0:
        if peca.cor == COR_JOGADOR_1:
          self.pecas_jogador_1 -= 1
        else:
          self.pecas_jogador_2 -= 1
