from config.configuracoes import *
import config.Global as Global
import funcoes_main

#classe para conferir conliões
class Colisoes:
    def __init__(self):
        pass

    # função para conferir as colisões com o player
    def verificar_colisao(self):
        
        chaves_para_eliminar = []
        # confere se cada player colidiu com cada obstaculo
        for player in Global.grupo_players.values():
            if player.rect.collidelist([projetil.rect for projetil in Global.grupo_obstaculos]) != -1:
        
                # se colidiu e não for o jogador:
                if player.real == False:   
                  
                    # se for a primeira partida de geração, preenche a a lista de geração_atual
                    if funcoes_main.selecao.contador_partidas == funcoes_main.selecao.partidas_por_geracao-1:

                        # junta o tempo de vida e os pesos da rede em uma lista e coloca os pesos do individuo no indice escolhido no inicio da geração
                        funcoes_main.selecao.geracao_atual.append([[player.distancia_percorrida]] + player.rede_neural.camadas)
                    
                player.desativar() 
                chaves_para_eliminar.append(player.indice)

        # apaga o player da lista de players
        for chave in chaves_para_eliminar:
            del Global.grupo_players[chave]
                
    # função para chamar as funções de colisão a cada iteração
    def update(self):
        self.verificar_colisao()

