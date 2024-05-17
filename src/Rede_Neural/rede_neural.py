import torch, copy, numpy
import torch.nn.functional as F
import torch.nn as nn
from. import estrategia_evolutiva
from random import uniform, randint

class RedeNeural(nn.Module):
    def __init__(self, configuracao_camadas, funcoes_camadas, bias, taxa_mutacao):
        super(RedeNeural, self).__init__() # garante que o nn.Module sejá inicializado antes de tudo ##########################################################################

        self.configuracao_camadas = configuracao_camadas
        self.funcoes_camadas = funcoes_camadas
        self.bias = bias
        self.taxa_de_mutacao = taxa_mutacao
        self.camadas = [] # variavel onde vão ser colocados os pesos 

        funcoes = {'relu': nn.ReLU(), 'leak_relu': nn.LeakyReLU(), 'sigmoid': nn. Sigmoid(), 'tanh': nn.Tanh()}
        self.funcoes_camadas = [funcoes[funcao] for funcao in funcoes_camadas]

        camadas = []
        for camada in range(len(configuracao_camadas) - 1): # -1 porque a ultima camada não tem uma próxima apra ligar (linha de baixo)
            camadas.append(nn.Linear(self.configuracao_camadas[camada], (self.configuracao_camadas[camada+1]))) # faz a ligação completa da camada com a proxima
            camadas.append(self.funcoes_camadas[camada])

        self.rede = nn.Sequential(*camadas) # junta todas as ligações, cria a rede em si

    # função utilizada para criar a primeira geração
    def iniciar_geracao(self):
        self.camadas = [ [ [uniform(-1, 1) for peso in range(len(neuronio))] for neuronio in camada] for camada in self.camadas]

    # função utilizada para criar um anova geração
    def nova_geracao(self):

        if estrategia_evolutiva.gerenciador.agentes_elite < estrategia_evolutiva.gerenciador.elitismo: # quantidade de cópias da melhor rede depende do valor definido
            
            self.camadas = copy.deepcopy(estrategia_evolutiva.gerenciador.melhor_agente[1:]) # obtem os pesos do melhor indivíduo
            estrategia_evolutiva.gerenciador.agentes_elite += 1 # registra que foi feita mais uma cópia
   
        else: # faz um sorteio dos individuos com preferencia dos melhores
     
            def roleta(): # sorteia um valor e busca seu indice

                roleta = uniform(0, 1)
                indice = numpy.searchsorted(estrategia_evolutiva.gerenciador.valores_proporcionais, roleta)
                return indice
                
            # sorteia dois individuos
            roleta_1 = roleta()
            roleta_2 = roleta()

            # junta caracteristicas dos dois individuos para formar o novo individuo, sorteando o ponto que vai ser unido
            camada_insercao_escolhida = randint(0, len(self.camadas) - 1) 
            neuronio_insercao_escolhido = randint(0, len(self.camadas[camada_insercao_escolhida]) - 1)

            # combina os dois individuos
            for camada in range(len(self.camadas)):
                for neuronio in range(len(self.camadas[camada])):

                    if camada < camada_insercao_escolhida or (camada == camada_insercao_escolhida and neuronio < neuronio_insercao_escolhido):                                         
                        self.camadas[camada][neuronio] = estrategia_evolutiva.gerenciador.total_redes[roleta_1][camada + 1][neuronio]# camada +1 porque a primeira camada = fitness
                  
                    elif camada > camada_insercao_escolhida or (camada == camada_insercao_escolhida and neuronio >= neuronio_insercao_escolhido):
                        self.camadas[camada][neuronio] = estrategia_evolutiva.gerenciador.total_redes[roleta_2][camada + 1][neuronio]
       
    # função utilizada para simular a mutação
    def mutacao(self):

        # randomizando cada peso de acordo com a taxa de mutação
        for camada in range(len(self.camadas)):
            for neuronio in range(len(self.camadas[camada])):
                for peso in range(len(self.camadas[camada][neuronio])):
        
                    # quanto maior a taxa de mutação, mais provavel é a alteração
                    if uniform(0, 1) <= self.taxa_de_mutacao:
                        self.camadas[camada][neuronio][peso] = round(uniform(-1, 1), 16) 

        # retorna todos os pesos do individuo deposi da mutação
        return (self.camadas)
    
    def definir_entrada(self, entradas):
        self.entrada = torch.tensor(entradas, dtype=torch.float32)

    # atualiza o estado da rede a cada iteração
    def obter_saida(self):

        # retorna True ou False para cada saída (a partir do critério da função de ativação)
        return self.rede(self.entrada).bool()


    
                