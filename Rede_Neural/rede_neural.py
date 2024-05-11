from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais

class RedeNeural:
    def __init__(self, camadas=[]):

        self.camadas = copy.deepcopy(camadas) # variavel onde vão ser colocados os pesos 

        self.taxa_de_mutacao = taxa_de_mutacao_base # definição da taxa de mutação
        
        # cria a estrutura de camadas com base nas configurações definidas
        for camada in range(1, len(configuracao_de_camadas)):  # 1 porque a primeira camada é  de entrada inicial
            self.camadas.append([numpy.array([0] * configuracao_de_camadas[camada - 1], dtype=float) for neuronio in range(configuracao_de_camadas[camada])])

        # se for a primeira geração, chama uma função que randomiza todos os pesos, senão, faz uma nova a partir da(s) anterior(es)
        self.iniciar_geracao() if Variaveis_globais.contador_geracoes == 0 else self.nova_geracao()

        # variavel que vai armazenar todos os pesos daquela rede (gerados na criação de rede)
        self.tensores = [torch.tensor(camada, dtype=torch.float64) for camada in self.camadas]
  
    # função utilizada para criar a primeira geração
    def iniciar_geracao(self):
        self.camadas = [ [ [uniform(-1, 1) for peso in range(len(neuronio))] for neuronio in camada] for camada in self.camadas]

    # função utilizada para criar um anova geração
    def nova_geracao(self):

        if Variaveis_globais.individuos_elite < numero_de_elitismo: # quantidade de cópias da melhor rede depende do valor definido
            
            self.camadas = copy.deepcopy(Variaveis_globais.melhor_individuo[1:]) # obtem os pesos do melhor indivíduo
            Variaveis_globais.individuos_elite += 1 # registra que foi feita mais uma cópia
   
        else: # faz um sorteio dos individuos com preferencia dos melhores
     
            def roleta(): # sorteia um valor e busca seu indice

                roleta = uniform(0, 1)
                indice = numpy.searchsorted(Variaveis_globais.valores_proporcionais, roleta)
                return indice
                
            # sorteia dois individuos
            roleta_1 = roleta()
            roleta_2 = roleta()

            # calcula a média do desempenho dos dois individuos sorteados
            media_de_recompensa = ((Variaveis_globais.juncao_de_geracoes[roleta_1][0][0] + Variaveis_globais.juncao_de_geracoes[roleta_2][0][0]) / 2) 

            # reduz a taxa de mutação base de acordo com a aproximação do objetivo
            self.taxa_de_mutacao = taxa_de_mutacao_base - (media_de_recompensa / recompensa_objetivo)

            # junta caracteristicas dos dois individuos para formar o novo individuo, sorteando o ponto que vai ser unido
            camada_insercao_escolhida = randint(0, len(self.camadas) - 1) 
            neuronio_insercao_escolhido = randint(0, len(self.camadas[camada_insercao_escolhida]) - 1)

            # combina os dois individuos
            for camada in range(len(self.camadas)):
                for neuronio in range(len(self.camadas[camada])):

                    if camada < camada_insercao_escolhida or (camada == camada_insercao_escolhida and neuronio < neuronio_insercao_escolhido):                                         
                        self.camadas[camada][neuronio] = Variaveis_globais.juncao_de_geracoes[roleta_1][camada + 1][neuronio]# camada +1 porque a primeira camada = fitness
                  
                    elif camada > camada_insercao_escolhida or (camada == camada_insercao_escolhida and neuronio >= neuronio_insercao_escolhido):
                        self.camadas[camada][neuronio] = Variaveis_globais.juncao_de_geracoes[roleta_2][camada + 1][neuronio]
       
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
        if funcoes_de_camadas[-2] in ['relu', 'tanh', 'leaky_relu']:
            return 0
    
        # se for sigmoid, o valor mínimo é 0.5
        elif funcoes_de_camadas[-2] == 'sigmoid':
            return 0.5
    
    def definir_entrada(self, entradas):
        self.entrada = entradas

    # atualiza o estado da rede a cada iteração
    def obter_saida(self):
        
        # armazena o resultado temporario de cada camada
        self.estado_atual_da_rede = torch.tensor(self.entrada, dtype=torch.float64)
        
        # Faz todos os calculos de cada camada e armazena em estado_atual_da_rede
        for camada in range(1, len(configuracao_de_camadas)):

            saida_camada_tensor = torch.matmul(self.estado_atual_da_rede, self.tensores[camada - 1].t()) + bias # executa as operações entre camadas
            saida_camada_tensor_ativada = self.aplicar_ativacao(saida_camada_tensor, Variaveis_globais.funcoes_de_camadas[camada - 1]) # aplica a função de ativação
            self.estado_atual_da_rede = saida_camada_tensor_ativada # passa para a próxima camada, armazenando os dados da anterior

        # retorna True ou False para cada saída (a partir do critério da função de ativação)
        return [True if comando > self.valor_de_ativacao() else False for comando in self.estado_atual_da_rede.tolist()]


    
                