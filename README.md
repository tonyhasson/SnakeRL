# SnakeRL

I built a Reinforcement Learning model that teaches an agent through game exprience how to play snake (and play it quite well).

## Information about the files

* SnakeGame.py - contains the snake game logic and environment.
* agent.py - contains the structure of the agent.
* model.py - contains the Q-net logic.
* main.py - the main program which connects all of these programs together.

## Information about the model

### Model :
DQN.

### Layers :
13 -> 255 -> 3 .

### The input:
13 parameters describing the state of the game-
* danger: danger_straight,danger_left,danger_right.
* current direction of snake: up,left,down,right.
* apple position: up,left,down,right.
* apple-snake manhattan distance.
* timeout- 200 turns without eating apple == GameOver.

### The output :
3 options of an action -
* turn left.
* turn right. 
* continue straight.

### Learning rate : 
0.0083

### Discount rate :
0.9

## Learning Process 

* The agent might make random actions until game 30,afterwards it plays only by knowledge of previous games.(Exploration/Explotation Trade Off)

* Exprience replay is used after every agents move,feeding to the network a batch consisting of 6 random states saved in memory.

* After the agent dies,the network is fed a batch of 1000 random states saved in memory.



https://user-images.githubusercontent.com/63504193/176749058-644da21c-9063-44d3-8174-c32e6669abe0.mp4
