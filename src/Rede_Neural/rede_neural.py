import torch, copy, numpy
import torch.nn.functional as F
from. import estrategia_evolutiva
from random import uniform, randint

class RedeNeural:
    def __init__(self, configuracao_camadas, funcoes_camadas, bias, taxa_mutacao):

        self.configuracao_camadas = configuracao_camadas
        self.funcoes_camadas = funcoes_camadas
        self.bias = bias
        self.taxa_de_mutacao = taxa_mutacao
        self.camadas = [] # variavel onde vão ser colocados os pesos 
        
        # cria a estrutura de camadas com base nas configurações definidas
        for camada in range(1, len(self.configuracao_camadas)):  # 1 porque a primeira camada é  de entrada inicial
            self.camadas.append([numpy.array([0] * self.configuracao_camadas[camada - 1], dtype=float) for neuronio in range(self.configuracao_camadas[camada])])

        # se for a primeira geração, chama uma função que randomiza todos os pesos, senão, faz uma nova a partir da(s) anterior(es)
        self.iniciar_geracao() if estrategia_evolutiva.gerenciador.contador_geracoes == 0 else self.nova_geracao()

        # variavel que vai armazenar todos os pesos daquela rede (gerados na criação de rede)
        self.tensores = [torch.tensor(camada, dtype=torch.float64) for camada in self.camadas]
  
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

    # seleciona a função de ativação de acordo com a configuração
    def aplicar_ativacao(self, tensor, tipo):

        if tipo == 'sigmoid':
            return F.sigmoid(tensor)
            
        elif tipo == 'relu':
            return F.relu(tensor)
        
        elif tipo == 'tanh':
            return F.tanh(tensor)
    
        elif tipo == 'leaky_relu':
            return F.leaky_relu(tensor)
    
    # retorna o valor mínimo para ativar o neuronio
    def valor_de_ativacao(self):
        
        # se for Relu, leaky relu ou tangente hiperbólica, o valor de ativação é 0
        if self.funcoes_camadas[-1] in ['relu', 'tanh', 'leaky_relu']:
            return 0
    
        # se for sigmoid, o valor mínimo é 0.5
        elif self.funcoes_camadas[-1] == 'sigmoid':
            return 0.5
    
    def definir_entrada(self, entradas):
        self.entrada = entradas

    # atualiza o estado da rede a cada iteração
    def obter_saida(self):
        
        # armazena o resultado temporario de cada camada
        self.estado_atual_da_rede = torch.tensor(self.entrada, dtype=torch.float64)
        
        # Faz todos os calculos de cada camada e armazena em estado_atual_da_rede
        for camada in range(1, len(self.configuracao_camadas)):

            saida_camada_tensor = torch.matmul(self.estado_atual_da_rede, self.tensores[camada - 1].t()) + self.bias # executa as operações entre camadas
            saida_camada_tensor_ativada = self.aplicar_ativacao(saida_camada_tensor, self.funcoes_camadas[camada - 1]) # aplica a função de ativação
            self.estado_atual_da_rede = saida_camada_tensor_ativada # passa para a próxima camada, armazenando os dados da anterior

        # retorna True ou False para cada saída (a partir do critério da função de ativação)
        return [True if comando > self.valor_de_ativacao() else False for comando in self.estado_atual_da_rede.tolist()]


    
                