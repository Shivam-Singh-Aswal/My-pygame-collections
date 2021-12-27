# The snake game

import pygame, random, sys, time

pygame.init()
pygame.font.init()

WIDTH = 1000
HEIGHT = 600
BGCOLOR = (0, 0, 0)
CELLSIZE = 20
FPS = 15

assert (WIDTH%CELLSIZE == 0 and HEIGHT% CELLSIZE == 0), 'non integral boxes'

pygame.mixer.music.load('bgsound.mp3')
pygame.mixer.music.play()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
SCREEN.fill(BGCOLOR)
pygame.display.update()


class mainGame:
    def __init__(self):
        self.DULLWHITE = pygame.Color(40, 40, 40)
        self.WHITE = pygame.Color(255, 255, 255)
        self.RED = pygame.Color(200, 0, 0)
        self.GREEN = pygame.Color(0, 255, 0)
        self.DARKG = pygame.Color(0, 125, 0)
        self.clock = pygame.time.Clock()


    def reset(self):
        self.dirList = [0, 0, 1, 0]
        self.snakeList = [(0, 0)]
        self.allowed = True
        self.isRunning = True
        self.score = 0


    def play(self):
        self.setAppleLocation()

        while self.isRunning:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                elif (event.type == pygame.KEYDOWN):
                    if self.allowed:
                        if (event.key == pygame.K_ESCAPE):
                            pygame.quit()
                            sys.exit()
                        elif (event.key == pygame.K_p):
                            self.pause()
                        elif (event.key == pygame.K_UP and not self.dirList[1]):
                            self.dirList = [-1, 0, 0, 0]
                        elif (event.key == pygame.K_DOWN and not self.dirList[0]):
                            self.dirList = [0, 1, 0, 0]
                        elif (event.key == pygame.K_LEFT and not self.dirList[3]):
                            self.dirList = [0, 0, -1, 0]
                        elif (event.key == pygame.K_RIGHT and not self.dirList[2]):
                            self.dirList = [0, 0, 0, 1]
                        self.allowed = False

            self.updateScreen()


    def pause(self):
        pause = True
        pygame.mixer.music.stop()
        while pause:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                elif (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    if (event.key == pygame.K_p):
                        pause = False
        pygame.mixer.music.play()


    def prepareGround(self):
        for i in range(0, WIDTH, CELLSIZE):
            pygame.draw.line(SCREEN, self.DULLWHITE, (i, 0), (i, HEIGHT))
            if (i < HEIGHT):
                pygame.draw.line(SCREEN, self.DULLWHITE, (0, i), (WIDTH, i))


    def setAppleLocation(self):
        while True:
            self.appleRow = random.randint(0, HEIGHT // CELLSIZE - 1)
            self.appleCol = random.randint(0, WIDTH // CELLSIZE - 1)
            for rect in self.snakeList:
                snakeRow, snakeCol = rect[0] // CELLSIZE, rect[1] // CELLSIZE
                if (snakeRow == self.appleRow and snakeCol == self.appleCol):
                    continue
            else:
                break

        self.appleBox = pygame.Rect(self.appleCol * CELLSIZE,
                                    self.appleRow * CELLSIZE,
                                    CELLSIZE,
                                    CELLSIZE)


    def drawApple(self):
        pygame.draw.rect(SCREEN, self.RED, self.appleBox)


    def drawSnake(self):
        for pos in self.snakeList:
            pygame.draw.rect(SCREEN, self.DARKG, (pos[0], pos[1], CELLSIZE, CELLSIZE))
            pygame.draw.rect(SCREEN, self.GREEN, (pos[0]+4, pos[1]+4, CELLSIZE-8, CELLSIZE-8))


    def showScore(self):
        FONT = pygame.font.SysFont('Consolas', 26, True)
        surf = FONT.render('Score :  ' + str(self.score), 1, self.WHITE)
        SCREEN.blit(surf, ( WIDTH - CELLSIZE * 9, CELLSIZE * 2))


    def moveSnake(self):
        self.allowed = True

        # The new box for snake
        end = self.snakeList[len(self.snakeList) - 1]
        newRect = (end[0] + (self.dirList[2] + self.dirList[3]) * CELLSIZE, 
                   end[1] + (self.dirList[0] + self.dirList[1]) * CELLSIZE)
        if (newRect in self.snakeList):
            self.isRunning = False
        elif (newRect[0]<0 or newRect[0]>WIDTH-CELLSIZE):
            self.isRunning = False
        elif (newRect[1]<0 or newRect[1]>HEIGHT-CELLSIZE):
            self.isRunning = False
        else:
            # Check if the apple has been eaten or not
            if (newRect == (self.appleCol * CELLSIZE, self.appleRow * CELLSIZE)):
                soundObj = pygame.mixer.Sound('eaten.wav')
                soundObj.play()
                self.score += 5
                self.setAppleLocation()
            else:
                self.snakeList.pop(0)

            self.snakeList.append(newRect)


    def startAnim(self):
        SCREEN.fill(BGCOLOR)
        self.prepareGround()
        FONT1 = pygame.font.SysFont('Consolas', 125, True, True)
        surf1 = FONT1.render('START GAME', 1, (0, 150, 0))
        FONT2 = pygame.font.SysFont('Comic Sans Ms', 40, True)
        surf2 = FONT2.render('Press any key to start', 1, (150, 150, 150))
        SCREEN.blit(surf1, (140, 135))
        SCREEN.blit(surf2, (275, 325))
        pygame.display.update()
        reset = pygame.event.get()
        
        done = False
        while not done:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                elif (event.type == pygame.KEYDOWN):
                    if (event.key != pygame.K_ESCAPE):
                        done = True
                        break
                    else:
                        pygame.quit()
                        sys.exit()

        self.reset()
        self.play()


    def endMessage(self):
        endSound = pygame.mixer.Sound('badswap.wav')
        endSound.play()
        time.sleep(1)
        FONT = pygame.font.SysFont('Consolas', 135, True)
        surf1 = FONT.render('GAME', 1, self.WHITE)
        surf2 = FONT.render('OVER', 1, self.WHITE)
        SCREEN.blit(surf1, (WIDTH - 650, 125))
        SCREEN.blit(surf2, (WIDTH - 650, 325))
        pygame.display.update()
        time.sleep(2)
        self.startAnim()


    def updateScreen(self):
        SCREEN.fill(BGCOLOR)
        self.moveSnake()
        self.drawApple()
        self.drawSnake()
        self.prepareGround()
        self.showScore()
        pygame.display.update()
        if not(self.isRunning):
            self.endMessage()


if __name__ == '__main__':
    game = mainGame()
    game.startAnim()
    pygame.quit()