import torch
import random
from collections import deque
from model import Linear_QNet, QTrainer,convnet1,QTrainer_CNN


if torch.cuda.is_available():
  dev = "cuda:0"
else:
  dev = "cpu"
device = torch.device(dev)

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
SMALL_BATCH_SIZE=6


class Agent_CNN:

    def __init__(self,LR,ell,total_epochs):
        self.LR=LR
        self.total_epochs=total_epochs
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.90  # discount rate
        self.epsilon_lvl_limit=ell
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = convnet1()
        self.trainer = QTrainer_CNN(self.model, lr=LR, gamma=self.gamma)
        self.reward=0

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached
        #self.memory.append((state[0], action, reward, next_state[0], done))  # popleft if MAX_MEMORY is reached
        #self.memory.append((state[1], action, reward, next_state[1], done))  # popleft if MAX_MEMORY is reached
        #self.memory.append((state[2], action, reward, next_state[2], done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, next_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
            if len(self.memory)>SMALL_BATCH_SIZE:
                mini_sample = random.sample(self.memory, SMALL_BATCH_SIZE)  # list of tuples
                state, action, reward, next_state, done = zip(*mini_sample)
                self.trainer.train_step(state, action, reward, next_state, done)
            else:
                self.trainer.train_step(state, action, reward, next_state, done)
                #self.trainer.train_step(state[0], action, reward, next_state[0], done)
                #self.trainer.train_step(state[1], action, reward, next_state[1], done)
                #self.trainer.train_step(state[2], action, reward, next_state[2], done)





    def build_action_vector(self, state):
        # random moves: tradeoff exploration / exploitation

        self.epsilon = self.epsilon_lvl_limit - self.n_games

        final_move = [0, 0, 0]
        if random.randint(0,  self.total_epochs) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            state0=state0.to(device)
            prediction = self.model(state0)

            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


##class with classic DQN
class Agent:

    def __init__(self,LR,ell):
        self.LR=LR
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.90  # discount rate
        self.epsilon_lvl_limit=ell
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(13,255, 3).to(device)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.reward=0

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, next_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
            if len(self.memory)>SMALL_BATCH_SIZE:
                mini_sample = random.sample(self.memory, SMALL_BATCH_SIZE)  # list of tuples
                state, action, reward, next_state, done = zip(*mini_sample)
            self.trainer.train_step(state, action, reward, next_state, done)




    def build_action_vector(self, state):
        # random moves: tradeoff exploration / exploitation

        self.epsilon = self.epsilon_lvl_limit - self.n_games

        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            state0 = state0.to(device)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


