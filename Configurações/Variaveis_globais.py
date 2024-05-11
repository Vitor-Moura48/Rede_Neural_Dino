from Configurações.Config import *

# se o arquivo da geração anterior existir
if os.path.exists("dados/saves/geracao_anterior.json"):

    # carrega os dados da ultima geração salva
    with open("dados/saves/geracao_anterior.json", 'r') as arquivo:
        geracao = json.load(arquivo)
        geracao_anterior = geracao
        
    if os.path.exists("dados/saves/informacoes.json"):

        with open("dados/saves/informacoes.json", 'r') as arquivo:
            informacoes = json.load(arquivo)

            contador_geracoes = informacoes[0]

else:

    # cria a estrutura da geração, para ser preenchida depois
    geracao_atual = []
    for individuo in range(numero_players):
        geracao_atual.append([])
    
    contador_geracoes = 0

    # listas das gerações anteriores
    geracao_avo = []
    geracao_anterior = []


# se o arquivo da geração anterior existir
if os.path.exists("dados/saves/geracao_avo.json"):

    #carrega os dados da ultima geração salva
    with open("dados/saves/geracao_avo.json", 'r') as arquivo:
        geracao = json.load(arquivo)
        geracao_avo = geracao


# se o arquivo de melhor individuo existir
if os.path.exists("dados/saves/melhor_individuo.json"):

    # lê o arquivo e armazena os pesos
    with open("dados/saves/melhor_individuo.json", 'r') as arquivo:
        camadas = json.load(arquivo)
    melhor_individuo = camadas
    maior_ditancia = camadas[0][0]

else:

    melhor_individuo = []

    # ajuda a selecionar o melhor individuo de cada geração
    maior_ditancia = 0

partida_atual_da_geracao = 0

velocidade_cenario = 11

# listas usadas na criação de uma nova geração
juncao_de_geracoes = []
valores_proporcionais = []

# variavel para ajudar a manter sempre o melhor player
individuos_elite = 0

# variavel para controle do player do jogador
comandos = [[False], [False]] # (melhorar depois)

# lista para juntar os objetos das classes
grupo_obstaculos = []
grupo_processadores = {}
grupo_players = {}
grupo_players_desativados = {}

clock = pygame.time.Clock()

# variaveis para contar o fps
contador_frames = 0
tempo_inicio = time.time()