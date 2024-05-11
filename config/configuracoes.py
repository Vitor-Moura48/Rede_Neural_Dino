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
fps = 600

# define dimensões e cor da tela
tela = pygame.display.set_mode((largura, altura))
tela.fill((000, 000, 000))

# difine a fonte e um texto inicial para a tela
fonte = pygame.font.Font(None, 32)
mensagem_fps_para_tela = fonte.render('fps 0', True, (255, 000, 000))

###########################################################################################

# define o número de players
quantidade_jogadores = 1

numero_players = 500
distancia_obtaculos = 400
numero_de_elitismo = numero_players * 0.3