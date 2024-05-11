from config import Global
from config.configuracoes import *

class SelecaoNeural:
    def __init__(self, numero_players, partidas_por_geracao):
        
        self.numero_players = numero_players
        self.partidas_por_geracao = partidas_por_geracao
        
        self.contador_geracoes = 0
        self.contador_partidas = 0
        self.agentes_elite = 0
        self.melhor_record = 0
        self.melhor_agente = 0

        self.total_redes = []
        self.geracao_atual = []
        self.geracao_anterior = []
        self.geracao_avo = []
    
    def update(self):

        # registra que uma geração foi completa
        self.contador_geracoes += 1
        self.contador_partidas = 0

        # chama a função de criar uma nova geração
        self.nova_geracao()    

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
            if self.geracao_atual[agente][0][0] > self.melhor_record:
                self.melhor_record_geracao = self.geracao_atual[agente][0][0]      

                # confere se existe um novo melhor individuo
                if self.geracao_atual[agente][0][0] > self.melhor_record:
                    self.melhor_record = self.geracao_atual[agente][0][0]
                    self.melhor_agente = self.geracao_atual[agente]

                    # tranforma os dados ndrray em listas normais 
                    pesos_normalizados = [
                                            [neuronio.tolist() if isinstance(neuronio, numpy.ndarray) else neuronio for neuronio in camada]
                                            for camada in self.melhor_agente
                                            ]

                    # se sim, adiciona ele em um arquivo csv
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
    def salvar_geracao(self, geracao, nome_do_arquivo): ###################################################################
        
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

    def carregar_redes(self): ###########################################################

        # junta as duas gerações mais recentes e organiza os individuos pela recompensa obtida por cada um  
        self.total_redes = self.geracao_avo + self.geracao_anterior
        self.total_redes.sort(key=lambda x: x[0])

        # soma todas as recompensas dos individuos
        total_de_recompesa = sum(individuo[0][0] for individuo in self.total_redes)
        print(len(self.total_redes))
    
        Global.valores_proporcionais = [self.total_redes[0][0][0] / total_de_recompesa]
        # adiciona proporcionalmente um valor de acordo com a recompensa de cada individuo (para a roleta)
        for individuo in range(1, len(self.total_redes) - 1):

            # soma o valor anterior com o do individuo (para manter os valores "progredindo")
            Global.valores_proporcionais.append(Global.valores_proporcionais[-1] + self.total_redes[individuo][0][0] / total_de_recompesa)
                        
        # zera a geração atual para ser preenchida novamente
        
        self.geracao_atual = []
    
    def verificar_arquivos(self):
        
        # se o arquivo da geração anterior existir
        if os.path.exists("dados/saves/geracao_anterior.json"):

            # carrega os dados da ultima geração salva
            with open("dados/saves/geracao_anterior.json", 'r') as arquivo:
                geracao = json.load(arquivo)
                self.geracao_anterior = geracao
                
            if os.path.exists("dados/saves/informacoes.json"):

                with open("dados/saves/informacoes.json", 'r') as arquivo:
                    informacoes = json.load(arquivo)

                    self.contador_geracoes = informacoes[0]

        # se o arquivo da geração anterior existir
        if os.path.exists("dados/saves/geracao_avo.json"):

            #carrega os dados da ultima geração salva
            with open("dados/saves/geracao_avo.json", 'r') as arquivo:
                geracao = json.load(arquivo)
                self.geracao_avo = geracao


        # se o arquivo de melhor individuo existir
        if os.path.exists("dados/saves/melhor_individuo.json"):

            # lê o arquivo e armazena os pesos
            with open("dados/saves/melhor_individuo.json", 'r') as arquivo:
                camadas = json.load(arquivo)
            self.melhor_agente = camadas
            self.melhor_record = camadas[0][0]
