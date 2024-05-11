import pygame
from pygame import *

import sys, os, time, copy
from functools import cache
from random import *

import json
from cProfile import run
import torch
import torch.nn.functional as F
import numpy

# largura e altura da tela
largura = 1200
altura = 800

# inicia o pygame e define um limite de fps
pygame.init()
fps = 60

# define dimensões e cor da tela
tela = pygame.display.set_mode((largura, altura))
tela.fill((000, 000, 000))

# difine a fonte e um texto inicial para a tela
fonte = pygame.font.Font(None, 32)
mensagem_fps_para_tela = fonte.render('fps 0', True, (255, 000, 000))

###########################################################################################

# define o número de player (até dois)
quantidade_jogadores = 1

bias = 0

quantidade_entradas = 6

configuracao_de_camadas = (quantidade_entradas, quantidade_entradas * 2, quantidade_entradas, 2)
funcoes_de_camadas = ('relu', 'relu', 'relu', True) # [1-sigmoid, 2-relu, 3-tanh, 4-leark_relu] [softmax]

# quantas partidas vão ter por geração (quanto mais partidas, mais confiavel o resultado, porém, mais lento)
partidas_por_geracao = 4

numero_players = 500
distancia_obtaculos = 400

numero_de_elitismo = numero_players * 0.3

taxa_de_mutacao_base = 0.06
# definição da taxa de mutação (para o elitismo)
taxa_de_mutacao_elite = 0.02

recompensa_objetivo = 50000 * (1 / taxa_de_mutacao_base)





