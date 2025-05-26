# Main file for the Mutorere game

import pygame
from board import Board


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Mutorere")
    board = Board(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.handle_click(event.pos)
        board.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
