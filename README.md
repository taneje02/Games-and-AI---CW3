# **Pac-Man with A* Pathfinding AI**
This project implements a simplified version of Pac-Man with autonomous players and ghost enemies powered by the A (A-Star) pathfinding algorithm*. Ghosts dynamically chase the nearest player using real-time AI, navigating the maze using the shortest possible path. Players move randomly with goal-seeking behavior. A collision results in a game-over state.
# **AI Technique: A* Pathfinding**
Implemented from scratch using heapq for priority queue.
Uses Manhattan distance as a heuristic.
Recalculates paths each frame to follow the nearest player.
Supports multiple ghosts and players.

# Testing & Evaluation
Ghosts correctly track and catch players.

Game ends when any ghost reaches a player.

Tested on multiple maze layouts.

Responsive performance at 10 FPS.

# Network Considerations (If Multiplayer)
AI logic must be server-authoritative.

Players send input; server syncs ghost paths.

Latency affects fairness in collision detection.


