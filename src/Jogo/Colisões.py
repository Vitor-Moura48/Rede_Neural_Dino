from config.configuracoes import *
from ..Rede_Neural import estrategia_evolutiva
from . import player, obstaculos

#classe para conferir conliões
class Colisoes:

    # função para conferir as colisões com o player
    def verificar_colisao(self, objeto):
        if objeto.rect.collidelist([projetil.rect for projetil in obstaculos.grupo_obstaculos]) != -1:
            estrategia_evolutiva.gerenciador.desativar_agente(objeto)
            
    # função para chamar as funções de colisão a cada iteração
    def update(self):
        for agente in estrategia_evolutiva.gerenciador.agentes[:]:
            self.verificar_colisao(agente)
        
        try: 
            if player.jogador.rect.collidelist([projetil.rect for projetil in obstaculos.grupo_obstaculos]) != -1:
                player.jogador = None
        except: pass

