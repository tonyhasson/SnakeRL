import time

import pygame
import sys
import random

clock=pygame.time.Clock()

##Grid to x,y converter
def GridXYConverter(Grid_num):
    return Grid_num*20


class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Snake:
    def __init__(self,start_x,start_y,color):
        self.color=color
        self.PosList=[]
        self.PosList.append(Point(start_x,start_y))
        self.action_pattern=0  ## 0->up , 1>left  , 2->down  , 3->right
        self.action_vector=[]  ## [1,0,0]->continue straight,[0,1,0]->left turn , [0,0,1]-> right turn
        self.PreviousPos=Point(-1,-1)

    def get_action(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ##create random list of action(later will be a ML model)
        num=random.randint(1,3)
        if num==1:
            self.action_vector.append([1,0,0])
        elif num==2:
            self.action_vector.append([0,1,0])
        elif num==3:
            self.action_vector.append([0, 0, 1])




    def move(self):
        ##move snake body according to first Pos

        ##get previous position of last part for adding new part after eating apple
        self.PreviousPos.x = self.PosList[-1].x
        self.PreviousPos.y = self.PosList[-1].y

        temp_pos=Point(self.PosList[0].x,self.PosList[0].y)

        ##set action_pattern according to action_vector

        ##move right
        if self.action_vector[-1]==[0,0,1]:
            self.action_pattern=(self.action_pattern+1)%4

        ##move left
        if self.action_vector[-1] == [0, 1, 0]:
            self.action_pattern = (self.action_pattern - 1) % 4



        ##move first part

        ##move up
        if self.action_pattern == 0:
            self.PosList[0].y-=GridXYConverter(1)

        ##move left
        elif self.action_pattern == 1:
            self.PosList[0].x -= GridXYConverter(1)

        ##move down
        elif self.action_pattern == 2:
            self.PosList[0].y += GridXYConverter(1)

        ##move right
        elif self.action_pattern == 3:
            self.PosList[0].x += GridXYConverter(1)

        ##move the rest
        for i in range(1,len(self.PosList)):
            temp_pos2 = Point( self.PosList[i].x,self.PosList[i].y)
            self.PosList[i].y =temp_pos.y
            self.PosList[i].x = temp_pos.x
            temp_pos=temp_pos2



    def eat(self,apple):
        ##check if ate apple
        if self.PosList[0].x==apple.Pos.x and self.PosList[0].y==apple.Pos.y:
            self.PosList.append(Point(self.PreviousPos.x,self.PreviousPos.y))
            apple.NewPos(self.PosList)




class Apple:
    def __init__(self,x,y,color):
        self.Pos=Point(x,y)
        self.view=False
        self.color=color

    def NewPos(self,snake_list):
        ##set random values
        x,y=random.randint(0,19),random.randint(0,19)
        while (x,y) in snake_list:
            x, y = random.randint(0, 19), random.randint(0, 19)
        self.Pos.x=GridXYConverter(x)
        self.Pos.y=GridXYConverter(y)
class Colors:
    def __init__(self):
        self.BLACK=(0, 0, 0)
        self.WHITE = (200, 200, 200)
        self.RED=(255,0,0)
        self.GREEN=(0,255,0)
        self.BLUE=(0,0,255)

class Game:
    def __init__(self):
        self.colors=Colors()
        self.WINDOW_HEIGHT = 400
        self.WINDOW_WIDTH = 400
        self.SCREEN = pygame.display.set_mode(( self.WINDOW_HEIGHT,  self.WINDOW_WIDTH))
        self.CLOCK=pygame.time.Clock()
        self.blockSize = 20 #Set the size of the grid block
        self.snake=Snake(GridXYConverter(10),GridXYConverter(10),self.colors.GREEN)
        self.apple=Apple(GridXYConverter(5),GridXYConverter(5),self.colors.RED)



    ##main loop of the game
    def main(self):
        pygame.init()
        self.SCREEN.fill(self.colors.BLACK)

        ##loop as long as you didn't collide with wall/yourself
        while self.collision():
            self.snake.get_action()
            self.snake.move()
            self.snake.eat(self.apple)
            self.draw()
            pygame.display.update()
            time.sleep(0.5)


    ##draw grid,snake and apple positions
    def draw(self):
        self.drawGrid()
        self.drawSnake()
        self.drawApple()


    def drawGrid(self):
        for x in range(0, self.WINDOW_WIDTH, self.blockSize):
            for y in range(0, self.WINDOW_HEIGHT,self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.SCREEN, self.colors.BLACK, rect, 0)

    def drawSnake(self):
        for Pos in self.snake.PosList:
            rect = pygame.Rect(Pos.x, Pos.y, self.blockSize, self.blockSize)
            pygame.draw.rect(self.SCREEN, self.snake.color, rect, 0)

    def drawApple(self):
        rect = pygame.Rect(self.apple.Pos.x, self.apple.Pos.y, self.blockSize, self.blockSize)
        pygame.draw.rect(self.SCREEN, self.apple.color, rect, 0)

    def collision(self):
        ##check if snake is not colliding with walls
        if self.snake.PosList[0].x<0 or self.snake.PosList[0].x>self.WINDOW_WIDTH or self.snake.PosList[0].y<0 or self.snake.PosList[0].y>=self.WINDOW_HEIGHT-GridXYConverter(1):
            return False
        ##check if snake is not colliding with himself
        for i in range(1,len(self.snake.PosList)):
             if self.snake.PosList[0].x==self.snake.PosList[i].x and self.snake.PosList[0].y==self.snake.PosList[i].y:
                  return False
        else:
            return True


if __name__ == '__main__':
    gm=Game()
    gm.main()



