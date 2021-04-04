import torch
import random
import numpy as np
from collections import deque
from game_env import SnakeGameEnv, Direction, Point
from model import QNet, Trainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.num_games = 0
        self.epsilon = 0  # to control the randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # pop left
        self.model = QNet(11, 256, 3)
        self.trainer = Trainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, env):
        head = env.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y + 20)
        point_d = Point(head.x, head.y - 20)

        dir_l = env.snake_direction == Direction.LEFT
        dir_r = env.snake_direction == Direction.RIGHT
        dir_u = env.snake_direction == Direction.UP
        dir_d = env.snake_direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_l and env.is_collision(point_l))
            or (dir_r and env.is_collision(point_r))
            or (dir_u and env.is_collision(point_u))
            or (dir_d and env.is_collision(point_d)),
            # Danger right
            (dir_l and env.is_collision(point_u))
            or (dir_r and env.is_collision(point_d))
            or (dir_u and env.is_collision(point_r))
            or (dir_d and env.is_collision(point_l)),
            # Danger left
            (dir_l and env.is_collision(point_d))
            or (dir_r and env.is_collision(point_u))
            or (dir_u and env.is_collision(point_l))
            or (dir_d and env.is_collision(point_r)),
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            # Food location
            env.food.x < env.head_position.x,  # food left
            env.food.x > env.head_position.x,  # food right
            env.food.y < env.head_position.y,  # food down
            env.food.y > env.head_position.y,  # food up
        ]

        return np.array(state, dtype=int)

    def store_data(self, state, action, reward, next_state, done):
        self.memory.append(
            (state, action, reward, next_state, done)
        )  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        # grab one thousand samples from the memory
        if len(self.memory) > BATCH_SIZE:
            batch_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            batch_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*batch_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: trade-off between exploration and exploitation
        self.epsilon = 80 - self.num_games
        move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move_idx = random.randint(0, 2)
            move[move_idx] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move_idx = torch.argmax(prediction).item()
            move[move_idx] = 1

        return move


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
                agent.model.save_model()

            print("Game", agent.num_games, "Score", score, "Record", record_score)
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.num_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    train()
