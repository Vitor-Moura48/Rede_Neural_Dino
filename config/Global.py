from config.configuracoes import *

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
grupo_players = {}
grupo_players_desativados = {}

# variaveis para contar o fps
contador_frames = 0
tempo_inicio = time.time()

clock = pygame.time.Clock()




