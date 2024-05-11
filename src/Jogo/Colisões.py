from config.configuracoes import *
import config.Global as Global

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
                
                    # obtem o tempo de vida do individuo
                    ditancia_percorrida = player.distancia_percorrida

                    # se for a primeira partida de geração, preenche a a lista de geração_atual
                    if Global.partida_atual_da_geracao == 0:
                    
                        # junta o tempo de vida e os pesos da rede em uma lista e coloca os pesos do individuo no indice escolhido no inicio da geração
                        Global.geracao_atual[player.indice] = [[ditancia_percorrida]] + Global.grupo_players[player.indice].rede_neural.camadas

                    # se não for a primeira partida, apenas incrementa o valor (para tirar a média no futuro)
                    else:
                        Global.geracao_atual[player.indice][0][0] += ditancia_percorrida
                
                player.desativar() 
                chaves_para_eliminar.append(player.indice)

        # apaga o player da lista de players
        for chave in chaves_para_eliminar:
            del Global.grupo_players[chave]
                
    # função para chamar as funções de colisão a cada iteração
    def update(self):
        self.verificar_colisao()

