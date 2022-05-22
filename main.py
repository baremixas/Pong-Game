import pygame

from game import Game
from ai import AI

pygame.init()

screen_res = (800, 600)
screen = pygame.display.set_mode(screen_res)

if __name__ == '__main__':
    test = AI(screen, screen_res)
    test.train()

    # game = Game(screen, screen_res)
    # game.play(True)
