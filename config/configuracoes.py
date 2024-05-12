import pygame
from pygame import *

import sys, time, copy
from functools import cache
from random import *

# largura e altura da tela
largura = 1200
altura = 800

# inicia o pygame e define um limite de fps
pygame.init()
fps = 600

# define dimensões e cor da tela
tela = pygame.display.set_mode((largura, altura))
tela.fill((000, 000, 000))

# define o número de players
quantidade_jogadores = 1

distancia_obtaculos = 400