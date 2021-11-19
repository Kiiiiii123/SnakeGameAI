import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

font = pygame.font.Font("arial.ttf", 25)


# font = pygame.font.SysFont("arial", 25)


# A set of symbolic names that are bounded to unique values
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


# just like a light-weighted class
Point = namedtuple("Point", "x, y")

BLOCK_SIZE = 20
GAME_SPEED = 40  # set 20 when human play the game.

# RGB Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


class SnakeGameEnv:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # initialize the display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("SnakeGame")

        # to set the speed of the game
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        # initialize the game state
        self.snake_direction = Direction.RIGHT
        self.head_position = Point(self.width / 2, self.height / 2)
        self.snake = [
            self.head_position,
            Point(self.head_position.x - BLOCK_SIZE, self.head_position.y),
            Point(self.head_position.x - (2 * BLOCK_SIZE), self.head_position.y)]
        self.score = 0
        self.food = None
        self._place_food()
        # keep the track of frame iteration
        self.frame_iteration = 0

    # randomly place the food
    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        # recursive
        if self.food in self.snake:
            self._place_food()

    # given an action and return the reward
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            # we can get rid of the user input
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move the snake
        self._move(action)  # update the snake head
        self.snake.insert(0, self.head_position)

        # 3. check if the game is over
        reward = 0
        self.game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            self.game_over = True
            reward = -10
            return reward, self.game_over, self.score

        # 4. place new food or just move
        if self.head_position == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update the pygame ui and clock
        self._update_ui()
        self.clock.tick(GAME_SPEED)

        # 6. return if the game is over and the score
        return reward, self.game_over, self.score

    def _update_ui(self):
        # background
        self.display.fill(BLACK)

        # draw the snake
        for point in self.snake:
            pygame.draw.rect(
                self.display,
                BLUE1,
                pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE),
            )
            pygame.draw.rect(
                self.display, BLUE2, pygame.Rect(point.x + 4, point.y + 4, 12, 12)
            )

        # draw the food
        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )

        # draw the score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])

        # update the full display service to the screen
        pygame.display.flip()

    # the action can be straight, left turn and right turn
    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.snake_direction)

        if np.array_equal(action, [1, 0, 0]):
            next_direction = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            next_direction = clock_wise[next_idx]  # right turn: r -> d -> l -> u
        else:
            next_idx = (idx - 1) % 4  # turn left
            next_direction = clock_wise[next_idx]  # left turn: r -> u -> l -> d

        self.snake_direction = next_direction

        x = self.head_position.x
        y = self.head_position.y

        if self.snake_direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.snake_direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.snake_direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.snake_direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head_position = Point(x, y)

    # this function should be public because the agent will use it
    def is_collision(self, point=None):
        if point is None:
            point = self.head_position

        # the snake hits the boundary
        if (point.x > self.width - BLOCK_SIZE
                or point.x < 0
                or point.y > self.height - BLOCK_SIZE
                or point.y < 0):
            return True

        # the snake hits itself
        if point in self.snake[1:]:
            return True

        return False
