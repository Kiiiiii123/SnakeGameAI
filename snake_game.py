import pygame
import random
from enum import Enum
from collections import namedtuple

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
GAME_SPEED = 5

# RGB Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # initialize the display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("SnakeGame")

        # to set the speed of the game
        self.clock = pygame.time.Clock()

        # initialize the game state
        self.game_over = False
        self.snake_direction = Direction.RIGHT
        self.head_position = Point(self.width / 2, self.height / 2)
        self.snake = [
            self.head_position,
            Point(self.head_position.x - BLOCK_SIZE, self.head_position.y),
            Point(self.head_position.x - (2 * BLOCK_SIZE), self.head_position.y),
        ]
        self.score = 0
        self.food = None
        self._place_food()

    # helper function: randomly place the food
    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        # recursive
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.snake_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.snake_direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.snake_direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.snake_direction = Direction.DOWN

        # 2. move the snake
        self._move(self.snake_direction)  # update the snake head
        self.snake.insert(0, self.head_position)

        # 3. check if the game is over
        self.game_over = False
        if self._is_collision():
            self.game_over = True
            return self.game_over, self.score

        # 4. place new food or just move
        if self.head_position == self.food:
            self._place_food()
            self.score += 1
        else:
            self.snake.pop()

        # 5. update the pygame ui and clock
        self._update_ui()
        self.clock.tick(GAME_SPEED)

        # 6. return if the game is over and the score
        return self.game_over, self.score

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

    def _move(self, direction):
        x = self.head_position.x
        y = self.head_position.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head_position = Point(x, y)

    def _is_collision(self):
        # the snake hits the boundary
        if (
            self.head_position.x > self.width - BLOCK_SIZE
            or self.head_position.x < 0
            or self.head_position.y > self.height - BLOCK_SIZE
            or self.head_position.y < 0
        ):
            return True

        # the snake hits itself
        if self.head_position in self.snake[1:]:
            return True

        return False


if __name__ == "__main__":
    game = SnakeGame()

    # Game Loop
    while True:
        game_over, score = game.play_step()

        # break if game over
        if game_over:
            break

    print("Final Score: " + str(score))
    pygame.quit()
