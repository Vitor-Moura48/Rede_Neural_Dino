from config.configuracoes import time, pygame, tela, largura, altura
from ..Rede_Neural import estrategia_evolutiva
from ..Jogo.obstaculos import Obstaculos

class Visualizador:
    def __init__(self):
        self.contador_frames = 0
        self.tempo_inicial = 0
        self.fonte = pygame.font.Font(None, 32)

    def update(self):

        self.contador_frames += 1
        tempo_atual = time.time()
        delta = max(1e-10, tempo_atual - self.tempo_inicial) # nunca zerar
        
        tela.blit(self.fonte.render('fps ' + str(round(self.contador_frames / delta)), True, (255, 000, 000)), (largura * 0.8, altura * 0.05))
        tela.blit(self.fonte.render(f"geração {estrategia_evolutiva.gerenciador.contador_geracoes}", True, (255, 000, 000)), (largura * 0.8, altura * 0.1))
        tela.blit(self.fonte.render(f"partida {estrategia_evolutiva.gerenciador.contador_partidas}", True, (255, 000, 000)), (largura * 0.8, altura * 0.15))
        tela.blit(self.fonte.render(f"Velocidade {round(Obstaculos.velocidade_cenario, 2)}", True, (255, 000, 000)), (largura * 0.8, altura * 0.20))

        if (delta) > 0.6: # a cada x segundos, atualiza a taxa de frames
            self.contador_frames = 0
            self.tempo_inicial = tempo_atual

        