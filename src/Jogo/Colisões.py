from config.configuracoes import *
import config.Global as Global
from ..Rede_Neural import estrategia_evolutiva

#classe para conferir conliões
class Colisoes:
    def __init__(self):
        pass

    # função para conferir as colisões com o player
    def verificar_colisao(self):
    
        # confere se cada player colidiu com cada obstaculo
        for player in estrategia_evolutiva.gerenciador.agentes[:]:
            if player.rect.collidelist([projetil.rect for projetil in Global.grupo_obstaculos]) != -1:
                estrategia_evolutiva.gerenciador.desativar_agente() 
            
    # função para chamar as funções de colisão a cada iteração
    def update(self):
        self.verificar_colisao()

