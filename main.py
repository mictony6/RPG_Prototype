import pygame
import sys
from world import World

from config import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
world = World(screen, world_data)


def main():
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    world.run()
    pygame.display.update()


if __name__ == '__main__':
    while True:
        main()
