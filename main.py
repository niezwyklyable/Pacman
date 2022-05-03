import pygame
from pm.constants import WIDTH, HEIGHT, FPS
from pm.game import Game

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pacman by AW')

def main():
    clock = pygame.time.Clock()
    run = True
    game = Game(WIN)
    pygame.init()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

            if event.type == pygame.KEYDOWN:
                if not game.gameover:
                    if event.key == pygame.K_LEFT:
                        game.pacman.set_future_dir('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        game.pacman.set_future_dir('RIGHT')
                    elif event.key == pygame.K_UP:
                        game.pacman.set_future_dir('UP')
                    elif event.key == pygame.K_DOWN:
                        game.pacman.set_future_dir('DOWN')
                else:
                    if event.key == pygame.K_RETURN:
                        game.restart()

        game.update()
        game.render()
        
    pygame.quit()

main()
