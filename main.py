# "ArcuS"
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

import pygame
from game import *


#Function for opening screen
def main() :
    intro = True
    game = Game()
    game.loadMusic()
    game.readHighScore()
    pygame.mixer.music.play(loops=-1)
    while intro:
        pygame.mixer.music.play(loops=-1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
        game.screen.fill(SKY_BLUE)
        game.screen.blit(game.background, game.background_rect)
        game.draw.Button(4*WIDTH/5-75, 2*HEIGHT/3, "PLAY", BRIGHT_GREEN, GREEN, game.gameloop, WIDTH/8, HEIGHT/9)
        game.draw.Button(WIDTH/5-75, 2*HEIGHT/3, "QUIT", BRIGHT_RED, RED, quit, WIDTH/8, HEIGHT/9)
        game.draw.drawimage(WIDTH/2-WIDTH/4,HEIGHT/5,WIDTH/2,HEIGHT/4,TITLE_SCREEN)
        game.draw.drawimage(4*WIDTH/5 - WIDTH/10 , 2*HEIGHT / 3-WIDTH/20, WIDTH/5, WIDTH/5,"assets/playbutton.png")
        game.draw.drawimage(WIDTH / 5 -WIDTH/10, 2*HEIGHT / 3-WIDTH/20, WIDTH/5, WIDTH/5,"assets/quitbutton.png")
        game.draw.draw_text("HIGH SCORE:%d" % (game.highscore), WIDTH-WIDTH/5, 50, 30, BLACK)
        pygame.display.flip()
        game.clock.tick(FPS)

main()
