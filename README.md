### Introduction

------

#### In this tiny project, we will first re-engrave the game Snake with pygame, then turn the game into a reinforcement learning environment with a few minor code changes. In the core section, we will train an RL agent with Pytorch to play the game well — the snake can eat quite a bit of food while the game speed is very fast 😉. 

```
SnakeGameAI
├─ README.md
├─ agent.py
├─ arial.ttf
├─ game_env.py
├─ helper.py
├─ model
│    └─ model.pth
├─ model.py
└─ snake_game.py
```

### Environment

------

- #### Observation Space

```shell
[danger straight, danger right, danger left,

 direction left, direction right,
 direction up, direction down,

 food left, food right,
 food up, food down
 ]
```

#### Take the following figure for example:

<p align="center">
<img src="/images/960.png"><br/>
</p>

- #### Action Space

```tex
[1, 0, 0] -> go straight
[0, 1, 0] -> turn right
[0, 0, 1] -> turn left
```

- #### Reward Function

```tex
eat food:  +10
game over: -10
else:        0
```

### Agent

------

- #### Deep Q Learning

<p align="center">
<img src="/images/962.png"><br/>
</p>

- #### Model

<p align="center">
<img src="/images/961.png"><br/>
</p>

- #### Bellman Equation

<p align="center">
<img src="/images/963.png"><br/>
</p>

- #### Q Update Rule Simplified

<p align="center">
<img src="/images/964.png"><br/>
</p>

- #### Loss Function

<p align="center">
<img src="/images/965.png"><br/>
</p>

### Experiments

------

#### After training for about 100 games, we can get a pretty good agent：

<p align="center">
<img src="/images/967.png"><br/>
</p>
<p align="center">
<img src="/images/966.png"><br/>
</p>
