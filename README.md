# 3D Car Racing Game
A 3D racing game built with OpenGL and Python featuring dynamic track generation and stadium lighting.

## Quick Start

Run the game from `main.py`:
```bash
python main.py
```

Edit game settings directly in main.py:

- Track Options: Set track_number to 0, 1, 2, or 3
-- 0: Auto-generates random track using DFS recursion algorithm
-- 1, 2, 3: Pre-made tracks

- Auto-Generation Settings: Adjust min_len and max_len for random track length

## Track Generation Notes

- Map generation typically completes in 5-6 seconds
- If the algorithm gets gridlocked, restart the program or reduce min/max lengths

## Requirements
Install dependencies:

pip install pygame PyOpenGL PyOpenGL_accelerate

## Controls
- WASD: Vehicle movement
- Arrow Keys: Camera control
