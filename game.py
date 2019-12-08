import pygame
import random
import math
from constants import *
from os import path
from objects import *
from animation import *

# Game Class has in game functions
class Game :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
        pygame.display.set_caption("Arcus")
        self.clock = pygame.time.Clock()
        self.last_arrow_time = pygame.time.get_ticks()
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.draw = Draw(self)
        self.misses = 0
        self.highscore = 0
        self.score = 0
        self.PAUSE = False
        self.highscore = 0
        self.arrow_img = pygame.image.load(
                path.join(path.dirname(__file__), ARROW_IMAGE)).convert()
        self.background = pygame.image.load(
                path.join(path.dirname(__file__), BACKGROUND_IMAGE)).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_rect = self.background.get_rect()
        self.baloon_color = ["fire","meteor"]

        self.all_sprites = None
        self.baloons = None
        self.arrows = None
        self.new_baloon = None
        self.new_arrow = None
        self.last_arrow = None
        self.last_baloon_time = 0
        self.last_arrow_time = 0

        self.explosion = []
        for i in range(9):
            filename = "assets/regularExplosion0{}.png".format(i)
            temp = pygame.image.load(
                path.join(path.dirname(__file__), filename)).convert()
            self.explosion.append(temp)

        self.explosion_sound = pygame.mixer.Sound(
            path.join(path.dirname(__file__), EXPLOSION_SOUND))
        self.select_sound = pygame.mixer.Sound(
            path.join(path.dirname(__file__), CLICK_SOUND))

    def readHighScore(self) :
        try :
            with open(HIGHSCORE_FILE, "r") as file:
                self.highscore = int(file.readline())
        except :
            self.highscore = 0
    
    def writeHighScore(self) :
        with open(HIGHSCORE_FILE, "w") as file:
                file.write("%d" % (self.score))

    def loadMusic(self):
        pygame.mixer.music.load(
            (path.join(path.dirname(__file__), "assets/tgfcoder-FrozenJam-SeamlessLoop.ogg")))
        pygame.mixer.music.set_volume(VOLUME)

    def unpause_function(self):
        self.PAUSE = False


    def pause_function(self):
        self.PAUSE = True
        while self.PAUSE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.draw.Button(200, 2*HEIGHT/3, "CONTINUE", BRIGHT_GREEN,
               GREEN, self.unpause_function, 150, 100)
            self.draw.Button(WIDTH-450, 2*HEIGHT/3, "QUIT", BRIGHT_RED, RED, quit, 150, 100)
            self.draw.draw_text("PAUSE", WIDTH/2, HEIGHT/3, 200, BLUE)
            pygame.display.flip()
            self.clock.tick(FPS)


    def replay(self):
        if self.score == self.highscore:
            self.writeHighScore()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                self.screen.fill(SKY_BLUE)
                self.screen.blit(self.background, self.background_rect)
                self.draw.Button(200, 2*HEIGHT/3, "PLAY AGAIN",
                    BRIGHT_GREEN, GREEN, self.gameloop, 150, 100)
                self.draw.Button(WIDTH-450, 2*HEIGHT/3, "QUIT", BRIGHT_RED, RED, quit, 150, 100)
                self.draw.draw_text("Your Score : %d" % (self.score), WIDTH/2, HEIGHT/3, 100, BLUE)
                self.draw.draw_text("HIGH SCORE:%d" % (self.highscore), WIDTH-400, 50, 30, BLACK)
                if self.score == self.highscore:
                    self.draw.draw_text("Congratulations you have a new high score",
                        WIDTH/2, HEIGHT-200, 60, BRIGHT_GREEN)
                pygame.display.flip()
                self.clock.tick(FPS)

    def reload(self) :
        self.misses = 0
        self.highscore = 0
        self.score = 0
        self.last_arrow_time = 0

        self.all_sprites = None
        self.baloons = None
        self.arrows = None
        self.new_baloon = None
        self.new_arrow = None
        self.last_arrow = None
        self.last_baloon_time = 0
        self.last_arrow_time = 0

    def gameloop(self):
        self.reload()
        self.readHighScore()        

        self.all_sprites = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()
        self.baloons = pygame.sprite.Group()

        self.new_arrow = Arrow(self)
        self.all_sprites.add(self.new_arrow)
        self.arrows.add(self.new_arrow)
        self.last_arrow = self.new_arrow

        self.new_baloon = Baloon(self)
        self.all_sprites.add(self.new_baloon)
        self.baloons.add(self.new_baloon)

        # last_arrow_time = pygame.time.get_ticks()
        self.last_baloon_time = pygame.time.get_ticks()
        running = True
        while running:

            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            now = pygame.time.get_ticks()
            if self.last_arrow.Released and now-self.last_arrow_time > 1000:
                self.new_arrow = Arrow(self)
                self.all_sprites.add(self.new_arrow)
                self.arrows.add(self.new_arrow)
                self.last_arrow = self.new_arrow
                # last_arrow_time=now

            if now - self.last_baloon_time > 20000:
                self.new_baloon = Baloon(self)
                self.all_sprites.add(self.new_baloon)
                self.baloons.add(self.new_baloon)
                self.last_baloon_time = now

            for baloon in self.baloons:
                hits = pygame.sprite.spritecollide(
                    baloon, self.arrows, False, pygame.sprite.collide_circle)
                threshold = self.new_baloon.rect.top
                ##print(threshold)
                # adding treshold makes ballons or meteors explode at impact
                if hits or threshold<2:
                    baloon.kill()
                    explode = Explosion(baloon.rect.center, 100,self)
                    self.all_sprites.add(explode)
                    self.score += 1

                if (self.score > self.highscore):
                    self.highscore = self.score

            self.all_sprites.update()

            if self.misses > MISSES:
                self.replay()
            self.end_screen()
            pygame.display.flip()

    def end_screen(self) :
        self.screen.fill(SKY_BLUE)
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        self.draw.Button(WIDTH-120, 20, "PAUSE", BRIGHT_GREEN,
                GREEN, self.pause_function, 100, 100)
        self.draw.Button(WIDTH-120, 140, "QUIT", BRIGHT_RED, RED, quit, 100, 100)
        self.draw.Button(WIDTH-120, 280, "RESTART", BLUE, SKY_BLUE, self.gameloop, 100, 100)
        self.draw.draw_text("MISSES : %d" % (self.misses), WIDTH -
                200, HEIGHT-150, 50, BRIGHT_RED)
        self.draw.draw_text("SCORE : %d" % (self.score), WIDTH-200, HEIGHT-100, 40, BLUE)
        self.draw.draw_text("HIGH SCORE : %d" % (self.highscore),
                WIDTH-200, HEIGHT-50, 40, BLUE)


#Class to draw text and surfaces on screen
class Draw() :
    def __init__(self,game) :
        self.game = game

    def drawimage(self,x,y,w,h,address):
        image = self.insertimage = pygame.image.load(
                path.join(path.dirname(__file__),address)).convert_alpha()
        image=pygame.transform.scale(image,(int(w),int(h)))
        self.game.screen.blit(image, (x, y))

    def DrawRect(self,x, y, w, h, c):
        pygame.draw.rect(self.game.screen, c, [x, y, w, h])

    def text_objects(self,text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()


    def draw_text(self,text, x, y, s, color):
        font_name = pygame.font.match_font('comicsansms.ttf')
        s = int(s)
        largeText = pygame.font.Font(font_name, s)
        TextSurf, TextRect = self.text_objects(text, largeText, color)
        TextRect.center = ((x, y))
        self.game.screen.blit(TextSurf, TextRect)


    def Button(self,x,y , string, color2, color1, function, w, h):
        y = int(y) 
        self.game.mouse = pygame.mouse.get_pos()
        self.game.click = pygame.mouse.get_pressed()
        self.DrawRect(x, y, w, h, color1)
        if x <= self.game.mouse[0] <= x+w and y <= self.game.mouse[1] <= y+h:
            self.DrawRect(x, y, w, int(h), color2)
            if (self.game.click[0] == 1):
                self.game.select_sound.play()
                function()
        self.draw_text(string, x+w/2, y+h/2, (w+h)/8, BLACK)
