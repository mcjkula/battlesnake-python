# Battlesnake Bots/AI in Python

This repository contains algorithms and bots developed for [Battlesnake](https://play.battlesnake.com/).

## Technologies Used

- Libraries: `dataset`, `fastapi`

## Features

- **A* Algorithm (Pathfinding)**: Efficiently finds the shortest path to food/objectives.
- **Collision Detection**: Ensures the snake avoids collisions with other snakes or itself.
- **Head-to-Head Prevention**: Logic to prevent head-to-head collisions.
- **Out-of-Bounds Detection**: Keeps the snake within the game board boundaries.

## Motivation/Reason

Driven by an interest in competitive programming and game strategies, Battlesnake caught my attention. This project started as a hobby, with the goal of continuously refining the algorithm and bot to climb the Battlesnake rankings.

## Usage
1. Clone this repository.
2. Install necessary libraries.
3. Modify the code to remove database logic:
    - Navigate to the "start" and "end" methods in the main script.
    - Remove the lines involving the DATABASE object.
4. Run the main script.

```bash
python main.py
```

## Future Plans

- Refine the current strategies for better performance. (Cap being 500ms)
- Integrate reinforcement learning for adaptive gameplay.
- Experiment with other popular game algorithms and see their impact on performance.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.