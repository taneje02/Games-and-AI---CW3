**Pac-Man with A* Pathfinding AI**
This project implements a simplified version of Pac-Man with autonomous players and ghost enemies powered by the A (A-Star) pathfinding algorithm*. Ghosts dynamically chase the nearest player using real-time AI, navigating the maze using the shortest possible path. Players move randomly with goal-seeking behavior. A collision results in a game-over state.
**AI Technique: A* Pathfinding**
Implemented from scratch using heapq for priority queue.
Uses Manhattan distance as a heuristic.
Recalculates paths each frame to follow the nearest player.
Supports multiple ghosts and players.
