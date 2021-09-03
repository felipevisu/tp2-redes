import pygame

from network import Network
from game import *

pygame.init()

width = 878
height = 610
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Freeway")

status = 0

def redraw_window(screen, player1, player2, game):

    global status

    # Aguardando segundo jogador se conectar
    if status == 0:
        game.waiting(screen)

    # Contagem regressiva para início do jogo
    if player1 and player2 and status == 0:
        game.countdown(screen)
        status = 2

    # Partida em andamento
    if player1 and player2 and status == 2 and game.winner is None:
        game.render(screen)

    # Algum jogador venceu
    if game.winner is not None:
        game.finalize(screen)

    pygame.display.update()


def main():
    run = True
    network = Network()
    player1 = network.get_player()
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        player2, game = network.send(player1)
        
        cars = game.get_cars()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move(cars)
        redraw_window(screen, player1, player2, game)

        if game.winner is not None:
            break


main()