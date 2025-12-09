import pygame
from constantes import *
from tabuleiro import Tabuleiro

class Jogo:
    def __init__(self, janela):
        self._init()
        self.janela = janela
    
    def desenhar(self):
        self.tabuleiro.desenhar(self.janela)
        self.desenhar_movimentos_validos(self.movimentos_validos)
        pygame.display.update()

    def _init(self):
        self.selecionado = None
        self.tabuleiro = Tabuleiro()
        self.turno = COR_JOGADOR_1
        self.movimentos_validos = {}

    def resetar(self):
        self._init()

    def selecionar(self, linha, coluna):
        if self.selecionado:
            resultado = self._mover(linha, coluna)
            if not resultado:
                self.movimentos_validos = {}
                self.selecionado = None
                self.selecionar(linha, coluna) # Tenta selecionar outra peça
        
        peca = self.tabuleiro.obter_peca(linha, coluna)
        if peca != 0 and peca.cor == self.turno:
            self.selecionado = peca
            # Aqui calcularemos regras complexas depois, por enquanto vamos improvisar
            self.calcular_movimentos_simples()
            return True

        return False

    def _mover(self, linha, coluna):
        peca = self.tabuleiro.obter_peca(linha, coluna)
        
        # Se clicou num lugar vazio e é um movimento válido
        if self.selecionado and peca == 0 and (linha, coluna) in self.movimentos_validos:
            self.tabuleiro.mover_peca(self.selecionado, linha, coluna)

            capturadas = self.movimentos_validos[(linha, coluna)]
            if capturadas:
                self.tabuleiro.remover(capturadas)
                
            self.mudar_turno()
            return True

        return False
            

    def desenhar_movimentos_validos(self, movimentos):
        for move in movimentos:
            linha, coluna = move
            pygame.draw.circle(self.janela, COR_PONTO, (coluna * QUADRADO + QUADRADO//2, linha * QUADRADO + QUADRADO//2), 15)

    def mudar_turno(self):
        self.movimentos_validos = {} # Limpa movimentos
        if self.turno == COR_JOGADOR_1:
            self.turno = COR_JOGADOR_2
        else:
            self.turno = COR_JOGADOR_1

    # Função temporária apenas para testar movimentação (diagonal simples de 1 casa)
    def calcular_movimentos_simples(self):
        self.movimentos_validos = {}
        linha = self.selecionado.linha
        coluna = self.selecionado.coluna
        
        # Verifica as 4 diagonais possíveis (apenas 1 casa de distância)
        possiveis = [(linha-1, coluna-1), (linha-1, coluna+1), (linha+1, coluna-1), (linha+1, coluna+1)]
        
        for l, c in possiveis:
            if 0 <= l < 8 and 0 <= c < 8: # Dentro do tabuleiro
                if self.tabuleiro.obter_peca(l, c) == 0: # Se estiver vazio
                    self.movimentos_validos[(l, c)] = [] # Adiciona como válido