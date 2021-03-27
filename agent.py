import torch
import random
import numpy as np
from collections import deque
from game_env import SnakeGameEnv, Direction, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.num_games = 0
        self.epsilon = 0  # to control the randomness
        self.gamma = 0  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # pop left
        # TODO: model, trainer

    def get_state(self, env):
        pass

    def store_data(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record_score = 0

    agent = Agent()
    env = SnakeGameEnv()

    # training loop
    while True:
        # get old state
        old_state = agent.get_state(env)

        # get action
        move = agent.get_action(old_state)

        # perform the move and get new state
        reward, done, score = env.play_step(move)
        new_state = agent.get_state(env)

        # train short memory
        agent.train_short_memory(old_state, move, reward, new_state, done)

        # store data
        agent.store_data(old_state, move, reward, new_state, done)

        if done:
            # train long memory and plot the results
            env.reset()
            agent.num_games += 1
            agent.train_long_memory()

            if score > record_score:
                record_score = score
                # TODO agent.model.save()

            print("Game", agent.num_games, "Score", score, "REcord", record_score)

            # TODO: plot


if __name__ == "__main__":
    train()
