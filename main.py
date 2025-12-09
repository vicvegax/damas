import pygame
from pygame import *
from constantes import LARGURA, ALTURA, QUADRADO
from jogo import Jogo

# Configuração Inicial
FPS = 60
JANELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Damas em Python')

def main():
  rodando = True
  relogio = pygame.time.Clock()
  jogo = Jogo(JANELA)

  while rodando:
    relogio.tick(FPS)

    # 1. Checa eventos (cliques, fechar janela)
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        rodando = False
      
      if evento.type == pygame.KEYUP:
        print('Apertaram', evento.key)
        if evento.key == K_ESCAPE:
          rodando = False

      # Apenas para teste: Mostra onde clicou
      if evento.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        linha, coluna = get_posicao_mouse(pos)
        jogo.selecionar(linha, coluna)
        # print(f"Clicou na Linha: {linha}, Coluna: {coluna}")

    # 2. Desenha na tela
    jogo.desenhar()

    # 3. Atualiza o display
    pygame.display.update()

  pygame.quit()

def get_posicao_mouse(pos):
  x, y = pos
  linha = y // QUADRADO
  coluna = x // QUADRADO
  return linha, coluna

if __name__ == '__main__':
    main()