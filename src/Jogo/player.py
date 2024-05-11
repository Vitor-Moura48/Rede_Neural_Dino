from config.configuracoes import *
import config.Global as Global
from src.Rede_Neural.rede_neural import RedeNeural

class Player:
    def __init__(self, real, indice):

        self.rede_neural = RedeNeural()
        self.indice = indice # indice que o player vai ser colocado na variavel geração atual
        self.real = real # define se o player é ou não um jogador
        self.distancia_percorrida = 0 # variavel para contar a quantidade de loops que o player conseguiu passar
        self.cor = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.no_chao = False
        self.velocidade_y = 0
        
        # define o ponto de spaw do player
        self.posicao_x = int(largura * 0.2  + randint(-60, 60))
        self.posicao_y = int(altura * 0.8 + randint(-10, 10))

        # cria um retandulo de colisão e mostra na tela
        self.rect = pygame.Rect(self.posicao_x, self.posicao_y, 40, 45)

        if self.real:
            self.rect.x = 50
    
    # função para retornar as entradas para a rede neural
    def obter_entradas(self):
       
        # variavel que vai ser retornada após passar pelas funções
        projeteis = []

        def obter_distancias():
            for projetil in Global.grupo_obstaculos:
              
                dados = projetil.buscar_informacoes()

                # calcul o quão distante o projetil está do player (1 = o projetil mais distante à direita, -1 à esquerda)
                distancia_x = (dados[3] - self.rect.right)

                # retorna junto algumas outras informações (largura, altura, altura do chão, distancia do player)
                projeteis.append([dados[0], dados[1], dados[2], distancia_x])

        # função que ordena cada coordenada (dos inimigos) de acordo com os que estão mais próximos
        def ordenar_cada_inimigo():
            projeteis.sort(key=lambda x: x[3])

        # função que apaga as coordenadas exedentes e apaga a distancia absoluta dos resultados (usada para "ordenar cada inimigo")
        def normatizar_o_resultado():
        
            while len(projeteis) > 1:

                # remove a entrada do inicio caso o player já tenha passado completamente por ela
                if projeteis[0][3] < -(projeteis[0][0] + 40):
                    projeteis.pop(0)
                else:
                    projeteis.pop(-1)
        
        # chama todas essas funções
        obter_distancias()
        ordenar_cada_inimigo()
        normatizar_o_resultado()
        
        # variavel que vai conter os dados de entrada da rede
        entradas = [Global.velocidade_cenario, self.rect.bottom]

        # junta todos os dados que vão para a entrada da rede em uma única lista
        for projetil in projeteis:
            entradas.extend(projetil)

        # retorna as coordenadas mais próximas
        return entradas

    def desativar(self):
        Global.grupo_players_desativados[self.indice] = self
    
    # atualiza o estado do player a cada geração
    def update(self):
        
        if self.real == False:
            # conta os loops
            self.distancia_percorrida += 1 * Global.velocidade_cenario

            self.rede_neural.definir_entrada(self.obter_entradas())
            output = self.rede_neural.obter_saida()

            if output[0]:
                if self.no_chao:
                    self.velocidade_y -= 18

            if output[1]:
                self.velocidade_y += 0.4
                self.rect = pygame.Rect(self.rect.x, self.rect.y + 20, 40, 25)
            else:
                self.rect = pygame.Rect(self.rect.x, self.rect.y, 40, 45)
                
        # move o retangulo
        self.rect.y += int(self.velocidade_y)

        # Gravidade
        if self.rect.bottom >= altura - 15:
            self.no_chao = True
            self.rect.bottom = altura - 15
            self.velocidade_y = 0
        else:
            self.no_chao = False
            self.velocidade_y += 1.1

        
        # cria um retandulo de colisão e mostra na tela
        draw.rect(tela, self.cor, self.rect)
