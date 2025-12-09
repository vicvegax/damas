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
        if peca != 0:# and peca.cor == self.turno:
            self.selecionado = peca
            self.movimentos_validos = self.obter_movimentos_validos(peca)
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
            pygame.draw.circle(self.janela, COR_PONTO, (coluna * TAMANHO + TAMANHO//2, linha * TAMANHO + TAMANHO//2), 15)

    def mudar_turno(self):
        self.movimentos_validos = {} # Limpa movimentos
        if self.turno == COR_JOGADOR_1:
            self.turno = COR_JOGADOR_2
        else:
            self.turno = COR_JOGADOR_1

    # Função temporária apenas para testar movimentação (diagonal simples de 1 casa)
    def obter_movimentos_validos(self, peca):
        movimentos = {}
        esquerda = peca.coluna - 1
        direita = peca.coluna + 1
        linha = peca.linha
        
        if peca.cor == COR_JOGADOR_1 or peca.dama:
            movimentos.update(self._percorrer_esquerda(linha - 1, max(linha - 3, -1), -1, peca.cor, esquerda))
            movimentos.update(self._percorrer_direita(linha - 1, max(linha - 3, -1), -1, peca.cor, direita))
        
        if peca.cor == COR_JOGADOR_2 or peca.dama:
            movimentos.update(self._percorrer_esquerda(linha + 1, min(linha + 3, 8), 1, peca.cor, esquerda))
            movimentos.update(self._percorrer_direita(linha + 1, min(linha + 3, 8), 1, peca.cor, direita))
    
        return movimentos
    
    # Função recursiva que olha para a diagonal Esquerda
    def _percorrer_esquerda(self, inicio, fim, passo, cor, esquerda, capturados=[]):
        movimentos = {}
        ultimo = []
        for r in range(inicio, fim, passo):
            if esquerda < 0:
                break
            
            atual = self.tabuleiro.obter_peca(r, esquerda)
            
            # 1. Encontrou casa vazia
            if atual == 0:
                if capturados and not ultimo:
                    break
                elif capturados:
                    movimentos[(r, esquerda)] = ultimo + capturados
                else:
                    movimentos[(r, esquerda)] = ultimo
                
                if ultimo: # Se pulou alguém, verifica se dá pra pular de novo (pulo duplo)
                    if passo == -1:
                        linha = max(r-3, -1)
                    else:
                        linha = min(r+3, 8)
                    movimentos.update(self._percorrer_esquerda(r+passo, linha, passo, cor, esquerda-1, capturados=ultimo))
                    movimentos.update(self._percorrer_direita(r+passo, linha, passo, cor, esquerda+1, capturados=ultimo))
                break
            
            # 2. Encontrou peça da mesma cor (bloqueio)
            elif atual.cor == cor:
                break
            
            # 3. Encontrou peça inimiga (prepara para capturar)
            else:
                ultimo = [atual]

            esquerda -= 1
        
        return movimentos

    # Função recursiva que olha para a diagonal Direita (espelho da esquerda)
    def _percorrer_direita(self, inicio, fim, passo, cor, direita, capturados=[]):
        movimentos = {}
        ultimo = []
        for r in range(inicio, fim, passo):
            if direita >= 8: # Saiu do tabuleiro
                break
            
            atual = self.tabuleiro.obter_peca(r, direita)
            
            if atual == 0:
                if capturados and not ultimo:
                    break
                elif capturados:
                    movimentos[(r, direita)] = ultimo + capturados
                else:
                    movimentos[(r, direita)] = ultimo
                
                if ultimo:
                    if passo == -1:
                        linha = max(r-3, -1)
                    else:
                        linha = min(r+3, 8)
                    movimentos.update(self._percorrer_esquerda(r+passo, linha, passo, cor, direita-1, capturados=ultimo))
                    movimentos.update(self._percorrer_direita(r+passo, linha, passo, cor, direita+1, capturados=ultimo))
                break
            
            elif atual.cor == cor:
                break
            
            else:
                ultimo = [atual]

            direita += 1
        
        return movimentos