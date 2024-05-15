from config.configuracoes import *
from src.Jogo import player, obstaculos, Colisões, visualizador
from src.Rede_Neural import estrategia_evolutiva

# função para criar os objetos
def criar_objetos():

    estrategia_evolutiva.gerenciador.nova_partida()
    
    # cria o primeiro obstáculo 
    obstaculos.Obstaculos.velocidade_cenario = 11
    obstaculos.grupo_obstaculos.append(obstaculos.Obstaculos())

    player.jogador = player.Player(real=True)
    
# atualiza todos os objetos=
def atualizar_objetos():

    # função para exibir o fps
    visualizador.dados.update()

    for obstaculo in obstaculos.grupo_obstaculos:
        obstaculo.update()
    
    for agente in estrategia_evolutiva.gerenciador.agentes:
        agente.update()
    
    try: 
        player.jogador.update()
    except: pass

    # confere as colisões
    colisoes.update()

    if largura - obstaculos.grupo_obstaculos[-1].rect.x > 400:

        obstaculo = obstaculos.Obstaculos()
        obstaculos.grupo_obstaculos.append(obstaculo)

    obstaculos.Obstaculos.velocidade_cenario += 0.005
    if obstaculos.Obstaculos.velocidade_cenario > 18:
        obstaculos.Obstaculos.velocidade_cenario = 18

def finalizar_partida():

    # zera os inimigos e recria todos depois
    obstaculos.grupo_obstaculos = []
    criar_objetos()  

# função para verificar se o jogador movimentou o player (melhorar depois)
def movimentacao_jogador():
    try:
        if pygame.key.get_pressed()[K_SPACE]:
            player.jogador.pular()
        if pygame.key.get_pressed()[K_s]:
            player.jogador.abaixar()
        else:
            player.jogador.levantar()
    except: pass

estrategia_evolutiva.gerenciador = estrategia_evolutiva.GerenciadorNeural(500, 2, 0.3, player.Player) # cria a classe que vai gerenciar as redes
criar_objetos() # cria os objetos iniciais
colisoes = Colisões.Colisoes() # cria classe de colisões
visualizador.dados = visualizador.Visualizador()





