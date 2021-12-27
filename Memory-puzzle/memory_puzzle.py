# Memory puzzle

import random, pygame, time, sys

#Initialising the modules
pygame.init()
pygame.font.init()

# the colors
GREEN = pygame.Color(0, 255, 0)
NAVYBLUE = pygame.Color(60,  60, 100)
YELLOW = pygame.Color(255, 255, 0)
bg = NAVYBLUE
color_list = [YELLOW, GREEN]

class game:
    def text_display(self):
        font = pygame.font.SysFont('freesansbold.ttf', 40, True)
        F1 = font.render('Clicks :  ' + str(self.clickCount), 1, GREEN)
        F2 = font.render('Score :  ' + str(self.score), 1, GREEN)
        self.surface.blit(F1, (self.initialPosX, 20))
        self.surface.blit(F2, (self.initialPosX + self.boxwidth * 8 + self.gap * 7 - 155, 20))

    def draw_surface(self, width, height, bg_color):
        self.width = width
        self.height = height
        self.color = pygame.Color(bg_color[0], bg_color[1], bg_color[2])
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.surface.fill(self.color)
        pygame.display.set_caption('Memory Puzzle')
        pygame.display.update()
        return

    def check_for_collision(self, rect):
        if rect.box.collidepoint(self.clickX, self.clickY):
            self.clickCount += 1
            if not(self.isSecond(rect)):
                self.isOnBox[0], self.isOnBox[1] = True, rect
                self.open_close_anim([rect])

    def isSecond(self, rect):
        if self.isOnBox[0]:
            if (self.isOnBox[1] is rect):
                self.open_close_anim([rect], False)
            else:
                self.open_close_anim([rect])
                time.sleep(0.5)
                if not(self.isSame(rect)):
                    self.open_close_anim([rect, self.isOnBox[1]], False)
            self.isOnBox = [False, None]
            return True
        return False

    def isSame(self, rect):
        if (self.isOnBox[1].color == rect.color and self.isOnBox[1].shape == rect.shape):
            self.shape_list.remove(rect)
            self.shape_list.remove(self.isOnBox[1])
            self.score += 2
            return True
        return False

    def open_close_anim(self, rectList, open = True, timeSpan = 0.01):
        if open: factor = -1
        else: factor = 1
        for slide in range(10):
            for rect in rectList:
                self.surface.fill(bg, rect.box)
                rect.rectSpan += 0.1 * factor
                rect.check_for_shape()
            pygame.display.update()
            time.sleep(timeSpan)

    def show_hover_effect(self):
        for item in self.shape_list:
            if item.box.collidepoint(self.hoverX, self.hoverY):
                mouseBox = (item.box[0] - 3, item.box[1] - 3, item.box[2] + 6, item.box[3] + 6)
                pygame.draw.rect(self.surface, (0, 0, 255), mouseBox, 4)

    def play(self):
        isRunning = True
        self.initialPosY = 70
        self.initialPosX = 25
        self.gap = 8
        self.boxwidth = 50
        self.clicked = False
        self.isOnBox = [False, None]
        self.clickX = self.clickY = None
        self.hoverX = self.hoverY = 0
        self.clickCount = self.score = 0

        self.define_the_shapes()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])

        # taking record of time
        self.clock = pygame.time.Clock()

        # Let the player see something :)
        self.first_look()

        # The main running loop
        while isRunning:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    isRunning = False
                    break
                elif event.type == pygame.MOUSEMOTION:
                    self.hoverX, self.hoverY = event.pos[0], event.pos[1]
                elif event.type == pygame.MOUSEBUTTONUP:
                    if (event.button == 1):
                        self.clicked = True
                        self.clickX = event.pos[0]
                        self.clickY = event.pos[1]
            self.update_surface()
        return

    def checkForWin(self):
        if self.score == 48:
            self.winMessage()
        return

    def winMessage(self):
        self.surface.fill((0, 0, 0))
        FONT = pygame.font.SysFont('freesansbold.ttf', 150)
        mycolor = pygame.Color(200, 200, 200)
        surf1 = FONT.render('YOU', 1, mycolor)
        surf2 = FONT.render('WIN', 1, mycolor)
        self.surface.blit(surf1, (150, 75))
        self.surface.blit(surf2, (150, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    def first_look(self):
        self.open_close_anim(self.shape_list, True, 0.01)
        time.sleep(2)
        self.open_close_anim(self.shape_list, False, 0.01)
        return

    def define_the_shapes(self):
        self.shape_list = [0 for i in range (48)]
        pool_of_values = [i for i in range (48)]
        skeletal_list = ['donut', 'ellipse', 'square', 'diamond', 'rect_border', 'lines'] # Other choices are oval and circle
        for iter in skeletal_list:
            for round in range(2):
                color = color_list[random.randint(0, len(color_list) - 1)]
                for turn in range(4):
                    place = pool_of_values[random.randint(0, len(pool_of_values)-1)]
                    _shape = shapes(self, iter, color, place)
                    self.shape_list[place] = _shape
                    pool_of_values.remove(place)
        return

    def update_surface(self):
        self.checkForWin()
        if self.clicked:
            for rect in self.shape_list:
                self.check_for_collision(rect)
            self.clickX = self.clickY = None
            self.clicked = False
        self.surface.fill(bg)
        for iter in self.shape_list:
            iter.check_for_shape()
        self.show_hover_effect()
        self.text_display()
        pygame.display.update()
        return

# The shapes class
class shapes:
    def __init__(self, game, str, color, place):
        self.game = game
        self.width = self.game.boxwidth
        self.shape = str
        self.color = color
        self.row = place // 8
        self.column = place % 8
        posX = self.game.initialPosX + (self.game.gap + self.width) * self.column
        posY = self.game.initialPosY + (self.game.gap + self.width) * self.row
        self.box = pygame.Rect(posX, posY, self.width, self.width)
        self.rectSpan = 1

    def check_for_shape(self):
        if self.shape == 'circle':
            pass #self.draw_circle()
        elif self.shape == 'donut':
            self.draw_donut()
        elif self.shape == 'square':
            self.draw_square()
        elif self.shape == 'diamond':
            self.draw_diamond()
        elif self.shape == 'ellipse':
            self.draw_ellipse()
        elif self.shape == 'rect_border':
            self.draw_rect_border()
        else:
            self.draw_lines()
        coverBox = (self.box[0], self.box[1], self.box[2] * self.rectSpan, self.box[3])
        pygame.draw.rect(self.game.surface, (228, 228, 228), coverBox)

    def draw_circle(self):
        pygame.draw.circle(self.game.surface, self.color, self.box.center, self.width // 4)

    def draw_donut(self):
        pygame.draw.circle(self.game.surface, self.color, self.box.center, self.width // 4, 3)

    def draw_lines(self):
        Left, Top= self.box[0], self.box[1]
        Right, Bottom = self.box[0] + self.box[2], self.box[1] + self.box[3]
        for i in range(0, self.box[2], 4):
            pygame.draw.aaline(self.game.surface, self.color, (Left+i, Top), (Left, Top+i))
            pygame.draw.aaline(self.game.surface, self.color, (Right, Top+i), (Left+i, Bottom))

    def draw_ellipse(self):
        myRectbox = (self.box[0] + 5, self.box[1] + 15, self.box[2] - 10, self.box[2] - 30)
        pygame.draw.ellipse(self.game.surface, self.color, myRectbox)

    def draw_diamond(self):
        tempRectbox = (self.box[0] + 10, self.box[1] + 10, self.box[2] - 20, self.box[3] - 20)
        myRectbox = ((tempRectbox[0] + tempRectbox[2]//2, tempRectbox[1]),
            (tempRectbox[0], tempRectbox[2]//2 + tempRectbox[1]),
            (tempRectbox[0] + tempRectbox[2]//2, tempRectbox[1] + tempRectbox[2]),
            (tempRectbox[0] + tempRectbox[2], tempRectbox[1] + tempRectbox[2]//2))
        pygame.draw.polygon(self.game.surface, self.color, myRectbox)

    def draw_square(self):
        myRectbox = (self.box[0] + 15, self.box[1] + 15, self.box[2] - 30, self.box[3] - 30)
        pygame.draw.rect(self.game.surface, self.color, myRectbox)

    def draw_rect_border(self):
        myRectbox = (self.box[0] + 15, self.box[1] + 15, self.box[2] - 30, self.box[2] - 30)
        pygame.draw.rect(self.game.surface, self.color, myRectbox, 3)


# The main program
if (__name__ == "__main__"):
    surf = game()
    surf.draw_surface(510, 435, bg)
    surf.play()
    pygame.quit()