from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais

class Player:
    def __init__(self, real, indice):

        # indice que o player vai ser colocado na variavel geração atual
        self.indice = indice

        # define se o player é ou não um jogador
        self.real = real

        # variavel para contar a quantidade de loops que o player conseguiu passar
        self.distancia_percorrida = 0

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
    
    # atualiza o estado do player a cada geração
    def update(self):
        
        if self.real == False:
            # conta os loops
            self.distancia_percorrida += 1 * Variaveis_globais.velocidade_cenario

            output = Variaveis_globais.grupo_processadores[self.indice].output

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
