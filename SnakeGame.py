import pygame
import sys
import random
import numpy as np
import time



clock=pygame.time.Clock()
BLOCK_SIZE=20

##Grid to x,y converter
def GridXYConverter(Grid_num):
    return Grid_num*BLOCK_SIZE

##x,y to Grid converter
def XYGridConverter(X):
    return X/BLOCK_SIZE


class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y


class Snake():
    # def __init__(self,start_x,start_y,color_body,color_head,PosList,PreviousPos):
    #     self.color_body=color_body
    #     self.color_head = color_head
    #     self.PosList=[]
    #     self.PosList.append(Point(start_x,start_y))
    #     self.action_pattern=0  ## 0->up , 1>left  , 2->down  , 3->right
    #     self.action_vector=[]  ## [1,0,0]->continue straight,[0,1,0]->left turn , [0,0,1]-> right turn
    #     self.PreviousPos=Point(-1,-1)
    def __init__(self,color_body, color_head, PosList, PreviousPos,action_vector,action_pattern=0):
        self.color_body = color_body
        self.color_head = color_head
        self.PosList = PosList
        self.action_pattern = action_pattern  ## 0->up , 1>left  , 2->down  , 3->right
        self.action_vector = action_vector  ## [1,0,0]->continue straight,[0,1,0]->left turn , [0,0,1]-> right turn
        self.PreviousPos = PreviousPos

    ##default constructor for new snake
    @classmethod
    def new(cls,start_x,start_y,color_body,color_head):
        return cls(color_body,color_head,[Point(start_x, start_y)],Point(-1,-1),[])

    ##copy constructor
    @classmethod
    def copy(cls,snake_source):
        PosList=[]
        for pos in snake_source.PosList:
            PosList.append(Point(pos.x,pos.y))

        ActionVec=[]
        for ap in snake_source.action_vector:
            ActionVec.append(ap)

        return cls(snake_source.color_body,snake_source.color_head,PosList,Point(snake_source.PreviousPos.x,snake_source.PreviousPos.y),ActionVec,snake_source.action_pattern)


    def get_action(self,state,agent):

        ##create random list of action(later will be a ML model_saver)
        #self.action_vector.append(build_action_vector(drawSnake))

        ##with model_saver using agent
        self.action_vector.append(agent.build_action_vector(state))

    def move(self):
        ##move snake body according to first Pos

        ##get previous position of last part for adding new part after eating apple
        self.PreviousPos.x = self.PosList[-1].x
        self.PreviousPos.y = self.PosList[-1].y

        temp_pos=Point(self.PosList[0].x,self.PosList[0].y)

        ##set action_pattern according to action_vector (not changing anything if moving straight)

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
            return True
        return False




class Apple:
    def __init__(self,x,y,color):
        self.Pos=Point(x,y)
        self.view=False
        self.color=color

    def NewPos(self,snake_list):
        ##set random values
        # x,y=random.randint(0,19),random.randint(0,19)
        # while (x,y) in snake_list:
        #     x, y = random.randint(0, 19), random.randint(0, 19)
        # self.Pos.x=GridXYConverter(x)
        # self.Pos.y=GridXYConverter(y)

        x=y=0
        try_again=True
        while try_again:
            try_again = False
            ##set random values
            x, y = GridXYConverter(random.randint(0, 19)), GridXYConverter(random.randint(0, 19))
            for snake in snake_list:
                ##if apple is in snake position, try again
                if x ==snake.x and y==snake.y:
                    try_again = True
                    break
        self.Pos.x = x
        self.Pos.y = y

class Colors:
    def __init__(self):
        self.BLACK=(0, 0, 0)
        self.WHITE = (200, 200, 200)
        self.RED=(255,0,0)
        self.GREEN=(0,255,0)
        self.BLUE=(0,0,255)

##class with regular states
class Game:
    def __init__(self):
        self.colors=Colors()
        self.WINDOW_HEIGHT = 400
        self.WINDOW_WIDTH = 400
        self.SCREEN = pygame.display.set_mode(( self.WINDOW_HEIGHT,  self.WINDOW_WIDTH))
        self.CLOCK=pygame.time.Clock()
        self.blockSize = BLOCK_SIZE #Set the size of the grid block (top of page)
        self.timeout_size=200

        ##if you add/edit anything don't forget the add to it to reset func as well
        #self.snake=Snake(GridXYConverter(10),GridXYConverter(10),self.colors.GREEN,self.colors.BLUE)
        self.snake = Snake.new(GridXYConverter(10),GridXYConverter(10),self.colors.GREEN,self.colors.BLUE)
        self.apple=Apple(GridXYConverter(5),GridXYConverter(5),self.colors.RED)
        self.apple.NewPos(self.snake.PosList)
        self.pause=False
        self.game_over=False
        self.score=0
        self.snake_apple_dist_pre=self.__snake_apple_dist_calc()
        self.snake_apple_dist=self.__snake_apple_dist_calc()
        self.timeout= self.timeout_size
        self.timeout_counter=0

        ##visualization testing
        self.fake_snake_list=[]



    ##main loop of the game
    def main(self,agent):
        pygame.init()
        self.SCREEN.fill(self.colors.BLACK)


        ##loop as long as you didn't collide with wall/yourself
        while not self.game_over:

            ##check for clicking events
            self.clicking_events()

            if not self.pause:

                ##get current state of game
                current_state = self.evaluate_game_state()

                ##decide action for snake
                self.snake.get_action(current_state,agent)

                ##move snake
                self.snake.move()

                self.evaluate_reward(agent)

                ##update previous distance between apple and snake
                self.snake_apple_dist_pre = self.snake_apple_dist

                ##draw game
                self.draw()

                ##get new state of game
                new_state=self.evaluate_game_state()

                ##train short memory
                agent.train_short_memory(current_state, self.snake.action_vector[-1], agent.reward, new_state, done=self.game_over)

                # remember
                agent.remember(current_state, self.snake.action_vector[-1], agent.reward, new_state, done=self.game_over)





    def reset(self):
        #self.snake = Snake(GridXYConverter(10), GridXYConverter(10), self.colors.GREEN,self.colors.BLUE)
        self.snake = Snake.new(GridXYConverter(10), GridXYConverter(10), self.colors.GREEN, self.colors.BLUE)
        self.apple = Apple(GridXYConverter(5), GridXYConverter(5), self.colors.RED)
        self.apple.NewPos(self.snake.PosList)
        self.pause = False
        self.game_over = False
        self.score = 0
        self.snake_apple_dist_pre = self.__snake_apple_dist_calc()
        self.snake_apple_dist = self.__snake_apple_dist_calc()
        self.timeout =self.timeout_size
        self.timeout_counter = 0

    def clicking_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:

                if pygame.key.name(event.key) == 'p':
                    if not self.pause:
                        self.pause = True
                    else:
                        self.pause = False


    ##draw grid,snake and apple positions
    def draw(self):
        self.drawGrid()
        self.drawSnake()
        self.drawApple()
        pygame.display.update()
        #time.sleep(0.000001)



    def drawGrid(self):
        for x in range(0, self.WINDOW_WIDTH, self.blockSize):
            for y in range(0, self.WINDOW_HEIGHT,self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.SCREEN, self.colors.BLACK, rect, 0)


    def drawSnake(self):
        for i,Pos in enumerate(self.snake.PosList):
            rect = pygame.Rect(Pos.x, Pos.y, self.blockSize, self.blockSize)
            ##if looking at head of snake
            if i==0:
                pygame.draw.rect(self.SCREEN, self.snake.color_head, rect, 0)
            ##if looking at body of snake
            else:
                pygame.draw.rect(self.SCREEN, self.snake.color_body, rect, 0)
            ##visulzation testing

        ##draw fake snake parts (for visualization only)
        # rect = pygame.Rect(self.fake_snake_list[0].PosList[0].x, self.fake_snake_list[0].PosList[0].y,
        #                    self.blockSize, self.blockSize)
        # pygame.draw.rect(self.SCREEN, self.fake_snake_list[0].color, rect, 0)
        #
        # rect = pygame.Rect(self.fake_snake_list[1].PosList[0].x, self.fake_snake_list[1].PosList[0].y,
        #                    self.blockSize, self.blockSize)
        # pygame.draw.rect(self.SCREEN, self.fake_snake_list[1].color, rect, 0)
        #
        # rect = pygame.Rect(self.fake_snake_list[2].PosList[0].x, self.fake_snake_list[2].PosList[0].y,
        #                    self.blockSize, self.blockSize)
        # pygame.draw.rect(self.SCREEN, self.fake_snake_list[2].color, rect, 0)

    def drawApple(self):
        rect = pygame.Rect(self.apple.Pos.x, self.apple.Pos.y, self.blockSize, self.blockSize)
        pygame.draw.rect(self.SCREEN, self.apple.color, rect, 0)

    def collision(self,snake_head):
        ##check if snake is not colliding with walls
        if snake_head.x<0 or snake_head.x>self.WINDOW_WIDTH-self.blockSize or snake_head.y<0 or snake_head.y>self.WINDOW_HEIGHT-self.blockSize:
            return True
        ##check if snake is not colliding with himself
        for i in range(1,len(self.snake.PosList)):
             if snake_head.x==self.snake.PosList[i].x and snake_head.y==self.snake.PosList[i].y:
                  return True
        else:
            return False

    def evaluate_reward(self,agent):
        ##reset agent reward
        agent.reward = 0

        ##try to eat apple
        if self.snake.eat(self.apple):
            agent.reward += 100
            self.score += 1
            self.timeout=self.timeout_size ##reset timeout

        ##didn't eat apple
        else:
            self.timeout-=1

        ##check if going toward apple
        if self.snake_apple_dist < self.snake_apple_dist_pre:
            agent.reward += max(0, 10 - self.snake_apple_dist)
            # agent.reward +=1

        ##check if going away from apple
        elif self.snake_apple_dist > self.snake_apple_dist_pre:
            agent.reward += max(-10, -1 * (self.snake_apple_dist))
            # agent.reward += -1

        ##check for collision with wall/snake body or timeout
        if self.collision(self.snake.PosList[0]) or self.timeout==0:
            if self.timeout==0:
                self.timeout_counter+=1
                print("TIMEOUT")
            self.game_over = True
            agent.reward = -100


    ##evaluate game state for ML model_saver
    def evaluate_game_state(self):
        ##13 states overall which will be fed as an input to the NN
        ## danger: danger_straight,danger_left,danger_right
        ## current direction of snake: up,left,down,right
        ## apple position: up,left,down,right
        ## apple-snake manhattan distance
        ## timeout- 200 turns without eating apple == GameOver


        ##first part:

        ##calc danger
        danger=[0,0,0]
        ##create 3 fake snake parts according to previous position and 3 possible directions

        danger_straight = Snake.copy(self.snake)
        danger_left = Snake.copy(self.snake)
        danger_right = Snake.copy(self.snake)

        ##move fake snake parts

        danger_straight.action_vector.append([1,0,0])
        danger_left.action_vector.append([0,1,0])
        danger_right.action_vector.append([0,0,1])

        danger_straight.move()
        danger_left.move()
        danger_right.move()

        ##send the fake part collision
        if self.collision(danger_straight.PosList[0]):
            danger[0]=1

        if self.collision(danger_left.PosList[0]):
            danger[1]=1

        if self.collision(danger_right.PosList[0]):
            danger[2]=1


        ##appending for test visualization only
        #self.fake_snake_list=[danger_straight,danger_left,danger_right]



        ##second part:

        ##calc current direction
        snake_dir = [0, 0, 0, 0]
        ##move up
        if self.snake.action_pattern == 0:
            snake_dir[0]=1

        ##move left
        elif self.snake.action_pattern == 1:
            snake_dir[1] = 1

        ##move down
        elif self.snake.action_pattern == 2:
            snake_dir[2] = 1

        ##move right
        elif self.snake.action_pattern == 3:
            snake_dir[3] = 1


        ##third part:

        ##calc apple position
        apple_pos=[0,0,0,0]
        if self.apple.Pos.y>self.snake.PosList[0].y: ##apple is below snake
            apple_pos[2]=1

        elif self.apple.Pos.y<self.snake.PosList[0].y: ##apple is above snake
            apple_pos[0]=1

        if self.apple.Pos.x > self.snake.PosList[0].x:  ##apple is right to snake
            apple_pos[3] = 1

        elif self.apple.Pos.x < self.snake.PosList[0].x:  ##apple is left to snake
            apple_pos[1] = 1


        ##fourth part:
        self.snake_apple_dist=self.__snake_apple_dist_calc()


        #return danger+snake_dir+apple_pos+[1/(1+self.snake_apple_dist)]
        return danger + snake_dir + apple_pos + [self.snake_apple_dist*(0.0125)]+[self.timeout/self.timeout_size]


    def __snake_apple_dist_calc(self):
        return XYGridConverter(abs(self.snake.PosList[0].x-self.apple.Pos.x)+abs(self.snake.PosList[0].y-self.apple.Pos.y))


##class with state as the whole grid (used for CNN)
class GameGridAsState:

    def __init__(self):
        self.colors = Colors()
        self.WINDOW_HEIGHT = 400
        self.WINDOW_WIDTH = 400
        self.SCREEN = pygame.display.set_mode((self.WINDOW_HEIGHT, self.WINDOW_WIDTH))
        self.CLOCK = pygame.time.Clock()
        self.blockSize = BLOCK_SIZE  # Set the size of the grid block (top of page)
        self.timeout_size = 200

        ##if you add/edit anything don't forget the add to it to reset func as well
        self.snake = Snake.new(GridXYConverter(10), GridXYConverter(10), self.colors.GREEN, self.colors.BLUE)
        self.apple = Apple(GridXYConverter(5), GridXYConverter(5), self.colors.RED)
        self.apple.NewPos(self.snake.PosList)
        self.pause = False
        self.game_over = False
        self.score = 0
        self.Grid_State_Real=np.zeros(shape=(3,3,20,20),dtype='f')

        self.snake_apple_dist_pre = self.__snake_apple_dist_calc()
        self.snake_apple_dist = self.__snake_apple_dist_calc()
        self.timeout = self.timeout_size
        self.timeout_counter = 0

        ##visualization testing
        self.fake_snake_list = []

    ##main loop of the game
    def main(self, agent):
        pygame.init()
        self.SCREEN.fill(self.colors.BLACK)

        ##loop as long as you didn't collide with wall/yourself
        while not self.game_over:

            ##check for clicking events
            self.clicking_events()

            if not self.pause:



                ##get current state of game
                current_state = self.evaluate_game_state()

                ##decide action for snake
                self.snake.get_action(current_state, agent)

                ##move snake
                self.snake.move()

                ##evaluate reward
                self.evaluate_reward(agent)

                ##update previous distance between apple and snake
                self.snake_apple_dist_pre = self.snake_apple_dist

                ##draw game
                self.draw()


                ##get new state of game
                new_state = self.evaluate_game_state()

                ##train short memory
                agent.train_short_memory(current_state, self.snake.action_vector[-1], agent.reward, new_state,
                                         done=self.game_over)

                # remember
                agent.remember(current_state, self.snake.action_vector[-1], agent.reward, new_state,
                               done=self.game_over)

    def reset(self):
        self.snake = Snake.new(GridXYConverter(10), GridXYConverter(10), self.colors.GREEN, self.colors.BLUE)
        self.apple = Apple(GridXYConverter(5), GridXYConverter(5), self.colors.RED)
        self.apple.NewPos(self.snake.PosList)
        self.pause = False
        self.game_over = False
        self.score = 0
        self.Grid_State_Real = np.zeros(shape=(3, 3, 20, 20), dtype='f')

        self.snake_apple_dist_pre = self.__snake_apple_dist_calc()
        self.snake_apple_dist = self.__snake_apple_dist_calc()
        self.timeout = self.timeout_size
        self.timeout_counter = 0

    def clicking_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:

                if pygame.key.name(event.key) == 'p':
                    if not self.pause:
                        self.pause = True
                    else:
                        self.pause = False

    ##draw grid,snake and apple positions
    def draw(self):
        self.drawGrid()
        self.drawSnake()
        self.drawApple()
        pygame.display.update()
        # GR=np.reshape(self.Grid_State,(1,400))
        # x,y,z=zip(*(GR[0]))

        #time.sleep(0.3)

    def drawGrid(self):
        for x in range(0, self.WINDOW_WIDTH, self.blockSize):
            for y in range(0, self.WINDOW_HEIGHT, self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.SCREEN, self.colors.BLACK, rect, 0)

    def drawSnake(self):
        for i, Pos in enumerate(self.snake.PosList):
            rect = pygame.Rect(Pos.x, Pos.y, self.blockSize, self.blockSize)

            ##if looking at head of snake
            if i == 0:
                pygame.draw.rect(self.SCREEN, self.snake.color_head, rect, 0)

            ##if looking at body of snake
            else:
                pygame.draw.rect(self.SCREEN, self.snake.color_body, rect, 0)


    ##visulzation testing

    ##draw fake snake parts (for visualization only)
    # rect = pygame.Rect(self.fake_snake_list[0].PosList[0].x, self.fake_snake_list[0].PosList[0].y,
    #                    self.blockSize, self.blockSize)
    # pygame.draw.rect(self.SCREEN, self.fake_snake_list[0].color, rect, 0)
    #
    # rect = pygame.Rect(self.fake_snake_list[1].PosList[0].x, self.fake_snake_list[1].PosList[0].y,
    #                    self.blockSize, self.blockSize)
    # pygame.draw.rect(self.SCREEN, self.fake_snake_list[1].color, rect, 0)
    #
    # rect = pygame.Rect(self.fake_snake_list[2].PosList[0].x, self.fake_snake_list[2].PosList[0].y,
    #                    self.blockSize, self.blockSize)
    # pygame.draw.rect(self.SCREEN, self.fake_snake_list[2].color, rect, 0)

    def drawApple(self):
        rect = pygame.Rect(self.apple.Pos.x, self.apple.Pos.y, self.blockSize, self.blockSize)
        pygame.draw.rect(self.SCREEN, self.apple.color, rect, 0)


    # def drawGridStateMEM(self):
    #     print(len(self.Grid_State_MEM))
    #     for i in range(len(self.Grid_State_MEM)):
    #         for x in range(0, self.WINDOW_WIDTH, self.blockSize):
    #             for y in range(0, self.WINDOW_HEIGHT, self.blockSize):
    #                 rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
    #                 pygame.draw.rect(self.SCREEN,
    #                                  self.Grid_State_MEM[i][int(XYGridConverter(y))][int(XYGridConverter(x))], rect,
    #                                  0)
    #         pygame.display.update()
    #         time.sleep(0.3)

    def collision(self, snake_head):
        ##check if snake is not colliding with walls
        if snake_head.x < 0 or snake_head.x > self.WINDOW_WIDTH - self.blockSize or snake_head.y < 0 or snake_head.y > self.WINDOW_HEIGHT - self.blockSize:
            return True
        ##check if snake is not colliding with himself
        for i in range(1, len(self.snake.PosList)):
            if snake_head.x == self.snake.PosList[i].x and snake_head.y == self.snake.PosList[i].y:
                return True
        else:
            return False

    def evaluate_reward(self, agent):
        # ##reset agent reward
        # agent.reward = 0
        #
        # ##try to eat apple
        # if self.snake.eat(self.apple):
        #     agent.reward += 100
        #     self.score += 1
        #
        #
        # ##check for collision with wall/snake body
        # if self.collision(self.snake.PosList[0]):
        #     self.game_over = True
        #     agent.reward = -100

        ##reset agent reward
        agent.reward = 0

        ##try to eat apple
        if self.snake.eat(self.apple):
            agent.reward += 100
            self.score += 1
            self.timeout = self.timeout_size  ##reset timeout

        ##didn't eat apple
        else:
            self.timeout -= 1

        ##get distance between snake and apple
        self.snake_apple_dist = self.__snake_apple_dist_calc()


        ##check if going toward apple
        if self.snake_apple_dist < self.snake_apple_dist_pre:
            agent.reward += max(0, 10 - self.snake_apple_dist)
            # agent.reward +=1

        ##check if going away from apple
        elif self.snake_apple_dist > self.snake_apple_dist_pre:
            agent.reward += max(-10, -1 * (self.snake_apple_dist))
            # agent.reward += -1

        ##check for collision with wall/snake body or timeout
        if self.collision(self.snake.PosList[0]) or self.timeout == 0:
            if self.timeout == 0:
                self.timeout_counter += 1
                print("TIMEOUT")
            self.game_over = True
            agent.reward = -100

    ##evaluate game state for ML model
    def evaluate_game_state(self):
        ##todo https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
        # 3 different photos, each has 3 different colors, each made of 20x20 pixels
        ##the grid is filled with zeros so all is left is to add the snake and apple
        ##first step will be taking the pixels for the snake
        ##second step will be taking the pixels of the apple


        ##get snake possible movements pixels


        ##create 3 fake snake parts according to previous position and 3 possible directions

        danger_straight = Snake.copy(self.snake)
        danger_left = Snake.copy(self.snake)
        danger_right = Snake.copy(self.snake)

        ##move fake snake parts

        danger_straight.action_vector.append([1, 0, 0])
        danger_left.action_vector.append([0, 1, 0])
        danger_right.action_vector.append([0, 0, 1])

        danger_straight.move()
        danger_left.move()
        danger_right.move()


        ##getting the pixel value for each photo
        self.PathSpecificSnake(self.Grid_State_Real[0],danger_straight)
        self.PathSpecificSnake(self.Grid_State_Real[1], danger_left)
        self.PathSpecificSnake(self.Grid_State_Real[2], danger_right)


        ##get apple position
        for p in range(3):
            for c in range(3):
                self.Grid_State_Real[p][c][int(XYGridConverter(self.apple.Pos.y))][int(XYGridConverter(self.apple.Pos.x))]=self.apple.color[c]

        return self.Grid_State_Real


    def PathSpecificSnake(self,Grid_State,snake):
        for i, Pos in enumerate(snake.PosList):

            ##if looking at head of snake
            if i == 0:
                try:
                    ##for each color channel

                    Grid_State[0][int(XYGridConverter(Pos.y))][int(XYGridConverter(Pos.x))]=snake.color_head[0]
                    Grid_State[1][int(XYGridConverter(Pos.y))][int(XYGridConverter(Pos.x))] = snake.color_head[1]
                    Grid_State[2][int(XYGridConverter(Pos.y))][int(XYGridConverter(Pos.x))] = snake.color_head[2]
                except:
                    pass
            ##if looking at body of snake
            else:
                try:
                    ##for each color channel

                    Grid_State[0][int(XYGridConverter(Pos.y))][int(XYGridConverter(Pos.x))] = snake.color_head[0]
                    Grid_State[1][int(XYGridConverter(Pos.y))][int(XYGridConverter(Pos.x))] = snake.color_head[1]
                    Grid_State[2][int(XYGridConverter(Pos.y))][int(XYGridConverter(Pos.x))] = snake.color_head[2]
                except:
                    pass

    def __snake_apple_dist_calc(self):
        return XYGridConverter(
            abs(self.snake.PosList[0].x - self.apple.Pos.x) + abs(self.snake.PosList[0].y - self.apple.Pos.y))

