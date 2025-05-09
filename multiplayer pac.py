import pygame
import random
import heapq

# Initialize Pygame
pygame.init()
TILE_SIZE = 20
GRID_WIDTH = 28

# Full-size Pac-Man style maze
raw_maze = [
    "1111111111111111111111111111",
    "1000000000110000000000000001",
    "1011111110110111111111100001",
    "1000000000000000000000111101",
    "1111110111111111111011111101",
    "1000000110000000110000000001",
    "1011111110111111111111111101",
    "1000000000000000000000000001",
    "1011111111111111111111111101",
    "1000000000000000000000000001",
    "1111111111111111111111111111",
    "1000000000110000000000000001",
    "1011111110110111111111100001",
    "1000000000000000000000111101",
    "1111110111111111111011111101",
    "1000000110000000110000000001",
    "1011111110111111111111111101",
    "1000000000000000000000000001",
    "1111111111111111111111111111"
]

MAZE = [[int(cell) for cell in row] for row in raw_maze]
GRID_HEIGHT = len(MAZE)
SCREEN = pygame.display.set_mode((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE))
pygame.display.set_caption("Multiplayer Pac-Man with A* Ghosts")

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# A* Pathfinding

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal):
    queue = []
    heapq.heappush(queue, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while queue:
        _, current = heapq.heappop(queue)
        if current == goal:
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            next_node = (nx, ny)
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and MAZE[ny][nx] == 0:
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(queue, (priority, next_node))
                    came_from[next_node] = current

    path = []
    curr = goal
    while curr in came_from:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()
    return path

# Game Entities
class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move_randomly(self):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and MAZE[ny][nx] == 0:
                self.x, self.y = nx, ny
                break

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x*TILE_SIZE+TILE_SIZE//2, self.y*TILE_SIZE+TILE_SIZE//2), TILE_SIZE//2)

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, players):
        # Target the nearest player
        target = min(players, key=lambda p: heuristic((self.x, self.y), (p.x, p.y)))
        path = astar((self.x, self.y), (target.x, target.y))
        if path:
            self.x, self.y = path[0]

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x*TILE_SIZE+TILE_SIZE//2, self.y*TILE_SIZE+TILE_SIZE//2), TILE_SIZE//2)

# Utility

def draw_maze():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if MAZE[y][x] == 1:
                pygame.draw.rect(SCREEN, BLUE, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def get_valid_spawn():
    while True:
        x, y = random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)
        if MAZE[y][x] == 0:
            return x, y

# Setup
players = [Player(*get_valid_spawn(), YELLOW), Player(*get_valid_spawn(), GREEN)]
ghosts = [Ghost(*get_valid_spawn(), RED) for _ in range(2)]

# Game Loop
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 48)
while running:
    SCREEN.fill(BLACK)
    draw_maze()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move players randomly
    for player in players:
        player.move_randomly()

    # Move ghosts toward players
    for ghost in ghosts:
        ghost.move(players)

    # Draw everything
    for player in players:
        player.draw()
    for ghost in ghosts:
        ghost.draw()

    # Check for collisions
    for ghost in ghosts:
        for player in players:
            if ghost.x == player.x and ghost.y == player.y:
                text = font.render("Game Over", True, WHITE)
                SCREEN.blit(text, (SCREEN.get_width()//2 - 100, SCREEN.get_height()//2))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False

    pygame.display.flip()
    clock.tick(5)
<<<<<<< HEAD
=======

pygame.quit()




>>>>>>> 8cfc602ed285c646326fdd0ddab7b2296f5620b3

pygame.quit()
