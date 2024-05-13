import json, numpy, os, time, copy

class GerenciadorNeural:
    def __init__(self, numero_players, partidas_por_geracao, elitismo, classe, *arg):
        
        self.numero_players = numero_players
        self.partidas_por_geracao = partidas_por_geracao
        self.elitismo = numero_players * elitismo
        self.classe = classe
        self.arg = arg
        
        self.contador_geracoes = 0
        self.contador_partidas = 0
        self.agentes_elite = 0
        self.melhor_record = 0
        self.melhor_agente = None 
        self.contador_frames = 0
        self.tempo_inicial = time.time()

        self.total_redes = []
        self.geracao_atual = []
        self.geracao_anterior = []
        self.geracao_avo = []
        self.agentes = []
        self.agentes_inativos = []

        self.verificar_arquivos()
        if self.contador_geracoes > 0:
            self.carregar_redes()
    
    def nova_partida(self):

        self.contador_partidas += 1 # registra a conclusão de uma partida
        if self.contador_partidas > self.partidas_por_geracao:# se as partidas da geração acabaram, cria a nova geração

            # registra que uma geração foi completa
            self.contador_geracoes += 1
            self.contador_partidas = 1

            self.nova_geracao() # chama a função responsável por criar uma nova geração
        
        self.ativar_agentes(self.classe, *self.arg)
    
    # função para criar uma nova geração
    def nova_geracao(self):

        # zera algumas variaveis que serão usadas depois
        self.agentes_elite = 0
        self.total_redes = []

        # salva algumas informações
        with open("dados/saves/informacoes.json", 'w') as arquivo:
            json.dump([self.contador_geracoes], arquivo)
       
        # divide a recompensa pela quantidade de partidas para fazer a media de recompensa
        self.melhor_record_geracao = 0
        for agente in range(self.numero_players):
            self.geracao_atual[agente][0][0] /= self.partidas_por_geracao

            # marca o melhor tempo da geração
            if self.geracao_atual[agente][0][0] > self.melhor_record_geracao:
                self.melhor_record_geracao = self.geracao_atual[agente][0][0]      

                # confere se existe um novo melhor agente
                if self.geracao_atual[agente][0][0] > self.melhor_record:
                    self.melhor_record = self.geracao_atual[agente][0][0]
                    self.melhor_agente = self.geracao_atual[agente]

                    # tranforma os dados ndrray em listas normais 
                    pesos_normalizados = [
                                            [neuronio.tolist() if isinstance(neuronio, numpy.ndarray) else neuronio for neuronio in camada]
                                            for camada in self.melhor_agente
                                            ]

                    # se sim, adiciona o agente em um arquivo csv
                    with open("dados/saves/melhor_individuo.json", 'w') as arquivo:
                        json.dump(pesos_normalizados, arquivo)

        # printa o melhor tempo geral e o melhor tempo dessa geração
        print(f'melhor tempo global: {self.melhor_record}')
        print(f"melhor tempo da geração; {self.melhor_record_geracao}")

        # pega a geração atual e passa ela para as gerações passadas
        self.geracao_avo = self.geracao_anterior
        self.geracao_anterior = self.geracao_atual
        
        self.salvar_geracao(self.geracao_anterior, "dados/saves/geracao_anterior.json")
        self.salvar_geracao(self.geracao_avo, "dados/saves/geracao_avo.json")

        self.carregar_redes()
    
    # salva a geração em um arquivo
    def salvar_geracao(self, geracao, nome_do_arquivo):
        
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

    def carregar_redes(self):

        # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um  
        self.total_redes = self.geracao_avo + self.geracao_anterior
        self.total_redes.sort(key=lambda x: x[0])

        recompensas = numpy.array([individuo[0][0] for individuo in self.total_redes]) # obtem o array de recompensas ordenada
        total_de_recompesa = sum(individuo[0][0] for individuo in self.total_redes) # soma todas as recompensas dos individuos
        self.valores_proporcionais = numpy.cumsum(recompensas / total_de_recompesa) # obtem cada parcela de recompensa e mantem a acumulação
                        
        self.geracao_atual = [] # zera a geração atual para ser preenchida novamente
    
    def carregar_arquivos(self, caminho, retorno):
        if os.path.exists(caminho):
            with open(caminho, 'r') as arquivo:
                return json.load(arquivo)
        else:
            return retorno
    
    def verificar_arquivos(self):
            
        self.geracao_anterior = self.carregar_arquivos("dados/saves/geracao_anterior.json", [])
        self.contador_geracoes = self.carregar_arquivos("dados/saves/informacoes.json", [0])[0] 
        self.geracao_avo = self.carregar_arquivos("dados/saves/geracao_avo.json", [])
        self.melhor_agente = self.carregar_arquivos("dados/saves/melhor_individuo.json", None)
        self.melhor_record = self.carregar_arquivos("dados/saves/melhor_individuo.json", [[0]])[0][0]
    
    def ativar_agentes(self, classe, *arg): # preenche a lista de agentes novos ou reativa os agentes
        self.agentes = [classe(*arg) for _ in range(self.numero_players)] if self.contador_partidas == 1 else copy.deepcopy(self.agentes_inativos)
        self.agentes_inativos = []
    
    def desativar_agente(self, agente):
        self.agentes_inativos.append(agente)
        self.agentes.remove(agente)

        if self.contador_partidas == self.partidas_por_geracao:
            self.geracao_atual.append([[agente.distancia_percorrida]] + agente.rede_neural.camadas)