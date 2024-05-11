from config.configuracoes import *
from config import Global
from src.Jogo import player, obstaculos, Colisões
from src.Rede_Neural.selecao_neural import SelecaoNeural

# função para criar os objetos
def criar_objetos(quantidade_playes):
    
    # cria o primeiro obstáculo 
    Global.grupo_obstaculos.append(obstaculos.Obstaculos())
    
    # cria os players a partir do valor definido em Config
    for indice_player in range(quantidade_playes):

        # se for o início de uma nova geração ele cria a nova geração normalmente
        if selecao.contador_partidas == 0:
            
            agente = player.Player(False, indice_player) # cria o player, que vai aparecer na tela

        # se não, copia as redes daquela geração
        else:
            agente = Global.grupo_players_desativados[indice_player]
            del Global.grupo_players_desativados[indice_player]

        # adiciona do grupo de redes e players novamente
        Global.grupo_players[indice_player] = agente
    
    # condição para adicionar um player para o jogador
    if quantidade_jogadores > 0:

        # cria um ou dois players
        for i in range(1, quantidade_jogadores + 1):
    
            agente = player.Player(True, f'p{str(i)}')  # o index nesse caso registra quem é o primeiro e o segundo player
            Global.grupo_players[f'p{str(i)}'] = agente
  
# lógica para contar o fps
def exibir_fps():
    global mensagem_fps_para_tela

    Global.contador_frames += 1
    tempo_atual = time.time()

    delta = tempo_atual - Global.tempo_inicio
    # a cada x segundos, printa a quantidade de loops feitos
    if (delta) > 0.5:

        mensagem_fps = "fps " + str(round(Global.contador_frames / delta))
        mensagem_fps_para_tela = fonte.render(mensagem_fps, True, (255, 000, 000))


        Global.contador_frames = 0
        Global.tempo_inicio = tempo_atual
    
    # exibe a taxa de fps no display
    tela.blit(mensagem_fps_para_tela, (largura * 0.8, altura * 0.05))
    tela.blit(fonte.render(f"geração {selecao.contador_geracoes}", True, (255, 000, 000)), (largura * 0.8, altura * 0.1))
    tela.blit(fonte.render(f"partida {selecao.contador_partidas}", True, (255, 000, 000)), (largura * 0.8, altura * 0.15))

# atualiza todos os objetos
def atualizar_objetos():

    # função para exibir o fps
    exibir_fps()

    for obstaculo in Global.grupo_obstaculos:
        obstaculo.update()
    
    for player in Global.grupo_players.values():
        player.update()

    # confere as colisões
    colisoes.update()

    if largura - Global.grupo_obstaculos[-1].rect.x > 400:

        obstaculo = obstaculos.Obstaculos()
        Global.grupo_obstaculos.append(obstaculo)

    Global.velocidade_cenario += 0.001
    if Global.velocidade_cenario > 15:
        Global.velocidade_cenario = 15


def nova_geracao_ou_nova_partida(): ##############################################################

    # registra a conclusão de uma partida
    selecao.contador_partidas += 1    

    # zera os inimigos e recria todos depois
    Global.grupo_obstaculos = []
    Global.velocidade_cenario = 5

    # confere se a quantidade escolhida de partidas por geração foi completa, se sim, cria a nova geração normalmente
    if selecao.contador_partidas >= selecao.partidas_por_geracao:
        selecao.update()

    criar_objetos(numero_players)  


# função para verificar se o jogador movimentou o player e responder (melhorar depois)
def movimentacao_jogador(): 

    # se a configuração for de um jogador, confere se ele está ativo
    if quantidade_jogadores == 1:
        if 'p1' in Global.grupo_players:
            if pygame.key.get_pressed()[K_SPACE]:
                if Global.grupo_players['p1'].no_chao:
                    Global.grupo_players['p1'].velocidade_y -= 18

            if pygame.key.get_pressed()[K_s]:
                Global.grupo_players['p1'].velocidade_y += 0.4
                Global.grupo_players['p1'].rect = pygame.Rect(Global.grupo_players['p1'].rect.x, Global.grupo_players['p1'].rect.y + 20, 40, 25)
            else:
                Global.grupo_players['p1'].rect = pygame.Rect(Global.grupo_players['p1'].rect.x, Global.grupo_players['p1'].rect.y, 40, 45)


selecao = SelecaoNeural(500, 1)

selecao.verificar_arquivos()

if selecao.contador_geracoes > 0:
    selecao.carregar_redes()
    
# cria os objetos iniciais
criar_objetos(numero_players)

# cria classe de colisões
colisoes = Colisões.Colisoes()





