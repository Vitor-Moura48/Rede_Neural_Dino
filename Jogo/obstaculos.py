from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais

class Obstaculos:  # classe que gerencia os projeteis
    def __init__(self):
 
        self.spawn()
    
    # função para tornar aleatorio a direção e ponto de partida dos projeteis
    def spawn(self):
        
        # largura, altura, altura para o fim da tela
        dimensoes = [[15, 33, 15], [23, 46, 15], [32, 33, 15], [55, 50, 110], [42, 36, 44], [49, 33, 15], [65, 47, 15]] 
        escolha = choice(dimensoes)#[45, 100, 55]

        self.altura = escolha[0]
        self.largura = escolha[1]
        self.altura_chao = escolha[2]
        
        self.rect = pygame.Rect(largura, altura - self.altura_chao, self.altura, self.largura)
        self.rect.bottom = altura - self.altura_chao


    # função que retorna algumas informações do projetil (usado no processamento da rede)
    def buscar_informacoes(self):
        return self.largura, self.altura, self.altura_chao, self.rect.left
    
    # atualiza estado a cada iteração
    def update(self):

        self.rect.x -= Variaveis_globais.velocidade_cenario

        if self.rect.right < 0:
            Variaveis_globais.grupo_obstaculos.remove(self)

        # cria um retandulo de colisão e mostra na tela 
        pygame.draw.rect(tela, (255, 000, 000), self.rect)

        

        

        

