from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais
from Jogo.obstaculos import *
from Rede_Neural.Criação_de_Rede import *
from Rede_Neural.Processador import *
from Jogo.Player import *
from Jogo.Colisões import *

# função para criar os objetos
def criar_objetos(quantidade_playes):

    # cria o primeiro obstáculo
    obstaculo = Obstaculos()  
    Variaveis_globais.grupo_obstaculos.append(obstaculo)

    # cria os players a partir do valor definido em Config
    for indice_do_player_na_geracao in range(quantidade_playes):

        # cria o player, que vai aparecer na tela
        player = Player(False, indice_do_player_na_geracao)

        # se for o início de uma nova geração ele cria a nova geração normalmente
        if Variaveis_globais.partida_atual_da_geracao == 0:

            # cria a rede para processar as entradas
            nova_rede = CriarRedeNeural()
            resultado = nova_rede.randomizar_resultados()
            processador = Processador(indice_do_player_na_geracao, resultado) 
         
        # se não, copia as redes daquela geração
        else:
            processador = Processador(indice_do_player_na_geracao, Variaveis_globais.geracao_atual[indice_do_player_na_geracao][1:])

        # adiciona do grupo de redes e players novamente
        Variaveis_globais.grupo_processadores[indice_do_player_na_geracao] = processador
        Variaveis_globais.grupo_players[indice_do_player_na_geracao] = player
    
    # condição para adicionar um player para o jogador
    if quantidade_jogadores > 0:

        # cria um ou dois players
        for i in range(1, quantidade_jogadores + 1):
    
            player = Player(True, f'p{str(i)}')  # o index nesse caso registra quem é o primeiro e o segundo player
            Variaveis_globais.grupo_players[f'p{str(i)}'] = player
  
# lógica para contar o fps
def exibir_fps():
    global mensagem_fps_para_tela

    Variaveis_globais.contador_distancia += 1
    tempo_atual = time.time()

    delta = tempo_atual - Variaveis_globais.tempo_inicio
    # a cada x segundos, printa a quantidade de loops feitos
    if (delta) > 0.5:

        mensagem_fps = "fps " + str(round(Variaveis_globais.contador_distancia / delta))
        mensagem_fps_para_tela = fonte.render(mensagem_fps, True, (255, 000, 000))


        Variaveis_globais.contador_distancia = 0
        Variaveis_globais.tempo_inicio = tempo_atual
    
    # exibe a taxa de fps no display
    tela.blit(mensagem_fps_para_tela, (largura * 0.8, altura * 0.05))
    tela.blit(fonte.render(f"geração {Variaveis_globais.contador_geracoes}", True, (255, 000, 000)), (largura * 0.8, altura * 0.1))
    tela.blit(fonte.render(f"partida {Variaveis_globais.partida_atual_da_geracao}", True, (255, 000, 000)), (largura * 0.8, altura * 0.15))

# atualiza todos os objetos
def atualizar_objetos():

    # função para exibir o fps
    exibir_fps()

    for obstaculo in Variaveis_globais.grupo_obstaculos:
        obstaculo.update()
     
    for processador in Variaveis_globais.grupo_processadores.values():
        processador.update()
    
    for player in Variaveis_globais.grupo_players.values():
        player.update()

    # confere as colisões
    colisoes.update()

    if largura - Variaveis_globais.grupo_obstaculos[-1].rect.x > 400:

        obstaculo = Obstaculos()
        Variaveis_globais.grupo_obstaculos.append(obstaculo)

    Variaveis_globais.velocidade_cenario += 0.001
    if Variaveis_globais.velocidade_cenario > 15:
        Variaveis_globais.velocidade_cenario = 15

# função para criar uma nova geração
def nova_geracao():
    
    # zera algumas variaveis que serão usadas depois
    Variaveis_globais.individuos_elite = 0
    Variaveis_globais.juncao_de_geracoes = []     

     # salva algumas informações
    with open("Rede_neural/informacoes.json", 'w') as arquivo:
        json.dump([Variaveis_globais.contador_geracoes], arquivo)

    melhor_tempo_da_geracao = 0
    # divide a recompensa pela quantidade de partidas para fazer a media de recompensa 
    for individuo in range(numero_players):
        Variaveis_globais.geracao_atual[individuo][0][0] /= partidas_por_geracao

        # marca o melhor tempo da geração
        if Variaveis_globais.geracao_atual[individuo][0][0] > melhor_tempo_da_geracao:
            melhor_tempo_da_geracao = Variaveis_globais.geracao_atual[individuo][0][0]      

            # confere se existe um novo melhor individuo
            if Variaveis_globais.geracao_atual[individuo][0][0] > Variaveis_globais.maior_ditancia:
                Variaveis_globais.maior_ditancia = Variaveis_globais.geracao_atual[individuo][0][0]
                Variaveis_globais.melhor_individuo = Variaveis_globais.geracao_atual[individuo]

                # tranforma os dados ndrray em listas normais 
                pesos_normalizados = [
                                        [neuronio.tolist() if isinstance(neuronio, numpy.ndarray) else neuronio for neuronio in camada]
                                        for camada in Variaveis_globais.melhor_individuo
                                        ]

                # se sim, adiciona ele em um arquivo csv
                with open("Rede_neural/melhor_individuo.json", 'w') as arquivo:
                    json.dump(pesos_normalizados, arquivo)

    # printa o melhor tempo geral e o melhor tempo dessa geração
    print(f'melhor tempo global: {Variaveis_globais.maior_ditancia}')
    print(f"melhor tempo da geração; {melhor_tempo_da_geracao}")

    # pega a geração atual e passa ela para as gerações passadas
    Variaveis_globais.geracao_avo = Variaveis_globais.geracao_anterior
    Variaveis_globais.geracao_anterior = Variaveis_globais.geracao_atual

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
    
    salvar_geracao(Variaveis_globais.geracao_anterior, "Rede_Neural/geracao_anterior.json")
    salvar_geracao(Variaveis_globais.geracao_avo, "Rede_Neural/geracao_avo.json")

    # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um  
    Variaveis_globais.juncao_de_geracoes = Variaveis_globais.geracao_avo + Variaveis_globais.geracao_anterior
    Variaveis_globais.juncao_de_geracoes.sort(key=lambda x: x[0])

    # soma todas as recompensas dos individuos
    total_de_recompesa = sum(individuo[0][0] for individuo in Variaveis_globais.juncao_de_geracoes)

    # adiciona a proporção de recompensa do primeiro individuo
    Variaveis_globais.valores_proporcionais = [Variaveis_globais.juncao_de_geracoes[0][0][0] / total_de_recompesa]
    # adiciona proporcionalmente um valor de acordo com a recompensa de cada individuo (para a roleta)
    for individuo in range(1, len(Variaveis_globais.juncao_de_geracoes)):
        
        # soma o valor anterior com o do individuo (para manter os valores "progredindo")
        Variaveis_globais.valores_proporcionais.append(Variaveis_globais.valores_proporcionais[-1] + Variaveis_globais.juncao_de_geracoes[individuo][0][0] / total_de_recompesa)

    # zera a geração atual para ser preenchida novamente
    Variaveis_globais.geracao_atual = []

    # recria a estrutura da geração atual (vazia)
    for individuo in range(numero_players):
        Variaveis_globais.geracao_atual.append([])

    # cria ou recria os objetos
    criar_objetos(numero_players)

def nova_geracao_ou_nova_partida():

    # registra a conclusão de uma partida
    Variaveis_globais.partida_atual_da_geracao += 1    

    # zera os inimigos e recria todos depois
    Variaveis_globais.grupo_obstaculos = []
    Variaveis_globais.velocidade_cenario = 5

    # confere se a quantidade escolhida de partidas por geração foi completa, se sim, cria a nova geração normalmente
    if Variaveis_globais.partida_atual_da_geracao >= partidas_por_geracao:

        # registra que uma geração foi completa
        Variaveis_globais.contador_geracoes += 1
        Variaveis_globais.partida_atual_da_geracao = 0

        # chama a função de criar uma nova geração
        nova_geracao()

    else:  
        criar_objetos(numero_players)  

    

# função para verificar se o jogador movimentou o player e responder (melhorar depois)
def movimentacao_jogador(): #################################################################################################### REFAZER #####################################
   
    # se a configuração for de um jogador, confere se ele está ativo
    if quantidade_jogadores == 1:
        if 'p1' in Variaveis_globais.grupo_players:
            if pygame.key.get_pressed()[K_SPACE]:
                if Variaveis_globais.grupo_players['p1'].no_chao:
                    Variaveis_globais.grupo_players['p1'].velocidade_y -= 18

            if pygame.key.get_pressed()[K_s]:
                Variaveis_globais.grupo_players['p1'].velocidade_y += 0.4
                Variaveis_globais.grupo_players['p1'].rect = pygame.Rect(Variaveis_globais.grupo_players['p1'].rect.x, Variaveis_globais.grupo_players['p1'].rect.y + 20, 40, 25)
            else:
                Variaveis_globais.grupo_players['p1'].rect = pygame.Rect(Variaveis_globais.grupo_players['p1'].rect.x, Variaveis_globais.grupo_players['p1'].rect.y, 40, 45)
                


def iniciar_save():

    # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um  
    Variaveis_globais.juncao_de_geracoes = Variaveis_globais.geracao_avo + Variaveis_globais.geracao_anterior
    Variaveis_globais.juncao_de_geracoes.sort(key=lambda x: x[0])

    # soma todas as recompensas dos individuos
    total_de_recompesa = sum(individuo[0][0] for individuo in Variaveis_globais.juncao_de_geracoes)
   
    Variaveis_globais.valores_proporcionais = [Variaveis_globais.juncao_de_geracoes[0][0][0] / total_de_recompesa]
    # adiciona proporcionalmente um valor de acordo com a recompensa de cada individuo (para a roleta)
    for individuo in range(1, len(Variaveis_globais.juncao_de_geracoes) - 1):

        # soma o valor anterior com o do individuo (para manter os valores "progredindo")
        Variaveis_globais.valores_proporcionais.append(Variaveis_globais.valores_proporcionais[-1] + Variaveis_globais.juncao_de_geracoes[individuo][0][0] / total_de_recompesa)
                    
    # zera a geração atual para ser preenchida novamente
    Variaveis_globais.geracao_atual = []
    # recria a estrutura da geração atual (vazia)
    for individuo in range(numero_players):
        Variaveis_globais.geracao_atual.append([])

if Variaveis_globais.contador_geracoes > 0:
    iniciar_save()
    
# cria os objetos iniciais
criar_objetos(numero_players)

# cria classe de colisões
colisoes = Colisoes()

