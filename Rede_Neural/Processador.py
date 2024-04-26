from Configurações.Config import *
import Configurações.Variaveis_globais as Variaveis_globais

# classe que gerencia o player
class Processador:
    def __init__(self, indice, camadas):

        self.indice = indice
        self.camadas = camadas
    
        # variavel que vai armazenar todos os pesos daquela rede (gerados na criação de rede)
        self.tensores = [torch.tensor(camada, dtype=torch.float64) for camada in camadas] ##############################

    # seleciona a função de ativação de acordo com a configuração
    def aplicar_ativacao(self, tensor, tipo):

        if tipo == 1:
            return F.sigmoid(tensor)
            
        elif tipo == 2:
            return F.relu(tensor)
        
        elif tipo == 3:
            return F.tanh(tensor)
    
        if tipo == 4:
            return F.leaky_relu(tensor)

    # função para retornar as entradas para a rede neural
    def obter_entradas(self):
       
        # variavel que vai ser retornada após passar pelas funções
        entradas = []

        def obter_distancias():
            for projetil in Variaveis_globais.grupo_obstaculos:
              
                dados = projetil.buscar_informacoes()

                # calcul o quão distante o projetil está do player (1 = o projetil mais distante à direita, -1 à esquerda)
                distancia_x = (dados[3] - Variaveis_globais.grupo_players[self.indice].rect.right)

                # retorna junto algumas outras informações (largura, altura, altura do chão, distancia do player)
                entradas.append([dados[0], dados[1], dados[2], distancia_x])

        # função que ordena cada coordenada (dos inimigos) de acordo com os que estão mais próximos
        def ordenar_cada_inimigo():
            entradas.sort(key=lambda x: x[3])

        # função que apaga as coordenadas exedentes e apaga a distancia absoluta dos resultados (usada para "ordenar cada inimigo")
        def normatizar_o_resultado():
        
            while len(entradas) > 1:

                # remove a entrada do inicio caso o player já tenha passado completamente por ela
                if entradas[0][3] < -(entradas[0][0] + 40):
                    entradas.pop(0)
                else:
                    entradas.pop(-1)

        # chama todas essas funções
        obter_distancias()
        ordenar_cada_inimigo()
        normatizar_o_resultado()

        # retorna as coordenadas mais próximas
        return entradas

    # atualiza o estado da rede a cada iteração
    def update(self):
    
        # obtem as informações dos projeteis mais próximos
        resultados = self.obter_entradas()

        # variavel que vai conter os dados de entrada da rede
        entrada_da_rede = [Variaveis_globais.velocidade_cenario, Variaveis_globais.grupo_players[self.indice].rect.bottom]

        # junta todos os dados que vão para a entrada da rede em uma única lista
        for projetil in resultados:
            entrada_da_rede.extend(projetil)
        
        # armazena o resultado das entradas ou de alguma fase intermediária
        self.estado_atual_da_rede = torch.tensor(entrada_da_rede, dtype=torch.float64)  ###########################################

        # Faz todos os calculos de cada camada e armazena na variavel acima
        for camada in range(1, len(configuracao_de_camadas)):

            saida_camada_tensor = torch.matmul(self.estado_atual_da_rede, self.tensores[camada - 1].t()) + bias ###########################################
            saida_camada_tensor_ativada = self.aplicar_ativacao(saida_camada_tensor, Variaveis_globais.funcoes_de_camadas[camada - 1])
            self.estado_atual_da_rede = saida_camada_tensor_ativada ######################################

        # variavel que contem o valor de saída da rede neural
        self.comandos = self.estado_atual_da_rede.tolist()
