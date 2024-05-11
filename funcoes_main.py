from config.configuracoes import *
from config import Global
from src.Jogo import player, obstaculos, Colisões

# função para criar os objetos
def criar_objetos(quantidade_playes):
    
    # cria o primeiro obstáculo 
    Global.grupo_obstaculos.append(obstaculos.Obstaculos())
    
    # cria os players a partir do valor definido em Config
    for indice_do_player_na_geracao in range(quantidade_playes):

        # se for o início de uma nova geração ele cria a nova geração normalmente
        if Global.partida_atual_da_geracao == 0:
            
            # cria o player, que vai aparecer na tela
            agente = player.Player(False, indice_do_player_na_geracao)

        # se não, copia as redes daquela geração
        else:
            agente = Global.grupo_players_desativados[indice_do_player_na_geracao]
            del Global.grupo_players_desativados[indice_do_player_na_geracao]

        # adiciona do grupo de redes e players novamente
        Global.grupo_players[indice_do_player_na_geracao] = agente
    
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
    tela.blit(fonte.render(f"geração {Global.contador_geracoes}", True, (255, 000, 000)), (largura * 0.8, altura * 0.1))
    tela.blit(fonte.render(f"partida {Global.partida_atual_da_geracao}", True, (255, 000, 000)), (largura * 0.8, altura * 0.15))

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

# função para criar uma nova geração
def nova_geracao():
    
    # zera algumas variaveis que serão usadas depois
    Global.individuos_elite = 0
    Global.juncao_de_geracoes = []     

     # salva algumas informações
    with open("dados/saves/informacoes.json", 'w') as arquivo:
        json.dump([Global.contador_geracoes], arquivo)

    melhor_tempo_da_geracao = 0
    # divide a recompensa pela quantidade de partidas para fazer a media de recompensa 
    for individuo in range(numero_players):
        Global.geracao_atual[individuo][0][0] /= partidas_por_geracao

        # marca o melhor tempo da geração
        if Global.geracao_atual[individuo][0][0] > melhor_tempo_da_geracao:
            melhor_tempo_da_geracao = Global.geracao_atual[individuo][0][0]      

            # confere se existe um novo melhor individuo
            if Global.geracao_atual[individuo][0][0] > Global.maior_ditancia:
                Global.maior_ditancia = Global.geracao_atual[individuo][0][0]
                Global.melhor_individuo = Global.geracao_atual[individuo]

                # tranforma os dados ndrray em listas normais 
                pesos_normalizados = [
                                        [neuronio.tolist() if isinstance(neuronio, numpy.ndarray) else neuronio for neuronio in camada]
                                        for camada in Global.melhor_individuo
                                        ]

                # se sim, adiciona ele em um arquivo csv
                with open("dados/saves/melhor_individuo.json", 'w') as arquivo:
                    json.dump(pesos_normalizados, arquivo)

    # printa o melhor tempo geral e o melhor tempo dessa geração
    print(f'melhor tempo global: {Global.maior_ditancia}')
    print(f"melhor tempo da geração; {melhor_tempo_da_geracao}")

    # pega a geração atual e passa ela para as gerações passadas
    Global.geracao_avo = Global.geracao_anterior
    Global.geracao_anterior = Global.geracao_atual

    # salva a geração em um arquivo
    def salvar_geracao(geracao, nome_do_arquivo):
        
        with open(nome_do_arquivo, "w") as arquivo:
            # tranforma os dados ndrray em listas normais 
            lista_geracao = [   
                                [
                                [neuronio.tolist() if isinstance(neuronio, numpy.ndarray) else neuronio for neuronio in camada]
                                for camada in individuo 
                                ]
                                for individuo in geracao
                            ]
            json.dump(lista_geracao, arquivo)
    
    salvar_geracao(Global.geracao_anterior, "dados/saves/geracao_anterior.json")
    salvar_geracao(Global.geracao_avo, "dados/saves/geracao_avo.json")

    carregar_redes()

    # cria ou recria os objetos
    criar_objetos(numero_players)

def nova_geracao_ou_nova_partida():

    # registra a conclusão de uma partida
    Global.partida_atual_da_geracao += 1    

    # zera os inimigos e recria todos depois
    Global.grupo_obstaculos = []
    Global.velocidade_cenario = 5

    # confere se a quantidade escolhida de partidas por geração foi completa, se sim, cria a nova geração normalmente
    if Global.partida_atual_da_geracao >= partidas_por_geracao:

        # registra que uma geração foi completa
        Global.contador_geracoes += 1
        Global.partida_atual_da_geracao = 0

        # chama a função de criar uma nova geração
        nova_geracao()

    else:  
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

def carregar_redes():

    # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um  
    Global.juncao_de_geracoes = Global.geracao_avo + Global.geracao_anterior
    Global.juncao_de_geracoes.sort(key=lambda x: x[0])

    # soma todas as recompensas dos individuos
    total_de_recompesa = sum(individuo[0][0] for individuo in Global.juncao_de_geracoes)
   
    Global.valores_proporcionais = [Global.juncao_de_geracoes[0][0][0] / total_de_recompesa]
    # adiciona proporcionalmente um valor de acordo com a recompensa de cada individuo (para a roleta)
    for individuo in range(1, len(Global.juncao_de_geracoes) - 1):

        # soma o valor anterior com o do individuo (para manter os valores "progredindo")
        Global.valores_proporcionais.append(Global.valores_proporcionais[-1] + Global.juncao_de_geracoes[individuo][0][0] / total_de_recompesa)
                    
    # zera a geração atual para ser preenchida novamente
    Global.geracao_atual = []

    # recria a estrutura da geração atual (vazia)
    for individuo in range(numero_players):
        Global.geracao_atual.append([])

if Global.contador_geracoes > 0:
    carregar_redes()
    
# cria os objetos iniciais
criar_objetos(numero_players)

# cria classe de colisões
colisoes = Colisões.Colisoes()

