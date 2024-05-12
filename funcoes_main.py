from config.configuracoes import *
from config import Global
from src.Jogo import player, obstaculos, Colisões
from src.Rede_Neural import estrategia_evolutiva

# função para criar os objetos
def criar_objetos():
    
    # cria o primeiro obstáculo 
    Global.grupo_obstaculos.append(obstaculos.Obstaculos())

    estrategia_evolutiva.gerenciador.ativar_agentes(player.Player, False)
    
    # condição para adicionar um player para o jogador
    if quantidade_jogadores > 0:
        pass

# atualiza todos os objetos
def atualizar_objetos():

    # função para exibir o fps
    estrategia_evolutiva.gerenciador.fps(tela, largura, altura)

    for obstaculo in Global.grupo_obstaculos:
        obstaculo.update()
    
    for player in estrategia_evolutiva.gerenciador.agentes:
        player.update()

    # confere as colisões
    colisoes.update()

    if largura - Global.grupo_obstaculos[-1].rect.x > 400:

        obstaculo = obstaculos.Obstaculos()
        Global.grupo_obstaculos.append(obstaculo)

    for obstaculo in Global.grupo_obstaculos:
        obstaculo.acelerar(0.001)

def nova_geracao_ou_nova_partida():

    # zera os inimigos e recria todos depois
    Global.grupo_obstaculos = []
    Global.velocidade_cenario = 5

    estrategia_evolutiva.gerenciador.update()
    criar_objetos()  


# função para verificar se o jogador movimentou o player e responder (melhorar depois)
def movimentacao_jogador():  ############################################################## REFAZER
    pass


estrategia_evolutiva.gerenciador = estrategia_evolutiva.GerenciadorNeural(500, 2, 0.3) # cria a classe que vai gerenciar as redes
criar_objetos() # cria os objetos iniciais
colisoes = Colisões.Colisoes() # cria classe de colisões





