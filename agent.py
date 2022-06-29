import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
SMALL_BATCH_SIZE=6


class Agent:

    def __init__(self,LR,):
        self.LR=LR
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.90  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(13,255, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.reward=0


    def reset(self):
        self.memory = deque(maxlen=MAX_MEMORY)

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

        self.epsilon = 30 - self.n_games

        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


