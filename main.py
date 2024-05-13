from funcoes_main import *

# loop principal
while True:

    # preenche a tela de preto (para ser redesenhada)
    tela.fill((000, 000, 000))

    # se todos os players foram eliminados, cria uma nova geração ou partida
    if len(estrategia_evolutiva.gerenciador.agentes) == 0 and player.jogador == None:
        finalizar_partida()

    # função para dar update em todos os objetos
    atualizar_objetos()

    # confere o clique para sair
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            sys.exit()

    # para contralar o jogador no teclado ou joystick
    movimentacao_jogador()

    # define um limite de fps
    pygame.time.Clock().tick(fps)

    # atualiza o display
    pygame.display.update() 