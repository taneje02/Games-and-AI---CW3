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
    "1111111111111111111111111111",
    "1000000000110000000000000001",
    "1011111110110111111111100001",
    "1000000000000000000000111101",
    "1111110111111111111011111101",
    "1000000110000000110000000001",
    "1011111110111111111111111101",
    "1000000000000000000000000001",
    "1111111111111111111111111111",
    "1000000000110000000000000001",
    "1011111110110111111111100001",
    "1000000000000000000000111101",
    "1111111111111111111111111111",
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

# Draw the maze
def draw_maze():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if MAZE[y][x] == 1:
                pygame.draw.rect(SCREEN, BLUE, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

# A* Pathfinding
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(start, goal):
    queue = []
    heapq.heappush(queue, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while queue:
        _, current = heapq.heappop(queue)
        if current == goal:
            break

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = current[0] + dx, current[1] + dy
            next_node = (nx, ny)
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and MAZE[ny][nx] == 0:
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(queue, (priority, next_node))
                    came_from[next_node] = current

    # Reconstruct path
    path = []
    curr = goal
    while curr in came_from:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()
    return path

# Entities
class Player:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.color = color
        self.controls = controls
        self.direction = (0, 0)

    def handle_input(self, keys):
        for key, dir in self.controls.items():
            if keys[key]:
                dx, dy = dir
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and MAZE[ny][nx] == 0:
                    self.direction = (dx, dy)

    def move(self):
        dx, dy = self.direction
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and MAZE[ny][nx] == 0:
            self.x, self.y = nx, ny

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, players):
        # Target the closest player using A*
        distances = [(heuristic((self.x, self.y), (p.x, p.y)), p) for p in players]
        target = min(distances, key=lambda x: x[0])[1]
        path = astar((self.x, self.y), (target.x, target.y))
        if path:
            next_pos = path[0]
            if next_pos != (self.x, self.y):
                self.x, self.y = next_pos

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

# Get a valid spawn position
def get_valid_spawn():
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if MAZE[y][x] == 0:
            return x, y

# Controls
player1_controls = {
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1)
}

player2_controls = {
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0),
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1)
}

# Create players
player1 = Player(*get_valid_spawn(), YELLOW, player1_controls)
player2 = Player(*get_valid_spawn(), GREEN, player2_controls)
players = [player1, player2]

# Create ghosts, avoiding overlap
ghosts = []
for _ in range(2):
    while True:
        gx, gy = get_valid_spawn()
        if all(p.x != gx or p.y != gy for p in players):
            ghosts.append(Ghost(gx, gy, RED))
            break

# Game state
clock = pygame.time.Clock()
running = True
frame_count = 0
font = pygame.font.SysFont(None, 48)

def check_collision():
    for ghost in ghosts:
        for player in players:
            if ghost.x == player.x and ghost.y == player.y:
                return True
    return False

# Show start screen briefly
SCREEN.fill(BLACK)
draw_maze()
for player in players:
    player.draw()
for ghost in ghosts:
    ghost.draw()
pygame.display.flip()
pygame.time.delay(2000)

# Game loop
while running:
    SCREEN.fill(BLACK)
    draw_maze()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    for player in players:
        player.handle_input(keys)

    if frame_count % 2 == 0:
        for player in players:
            player.move()

    if frame_count % 3 == 0:  # Slower ghost movement
        for ghost in ghosts:
            ghost.move(players)

    if check_collision():
        game_over_text = font.render("Game Over!", True, WHITE)
        SCREEN.blit(game_over_text, (SCREEN.get_width()//2 - 100, SCREEN.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
        continue

    for player in players:
        player.draw()
    for ghost in ghosts:
        ghost.draw()

    pygame.display.flip()
    frame_count += 1
    clock.tick(10)

pygame.quit()





