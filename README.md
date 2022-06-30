# SnakeRL

I built a Reinforcement Learning model that teaches an agent through game exprience how to play snake (and play it quite well).

Information about the files:

* SnakeGame.py - contains the snake game logic and environment.
* agent.py - contains the structure of the agent.
* model.py - contains the Q-net logic.
* main.py - the main program which connects all of these programs together.

Information about the model:

* Model - DQN.
* Layers :   13 -> 255 -> 3 .
* Learning rate : 0.0083
* Discount rate : 0.9
* The agent might make random actions until game 30,afterwards it plays only by knowledge of previous games.
* Exprience replay is used after every agents move,feeding to the network a batch consisting of 6 random states saved in memory.
* After the agent dies,the network is fed a batch of 1000 random states saved in memory.


