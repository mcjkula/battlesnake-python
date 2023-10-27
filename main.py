from objects import Snake, Board, Game
from objects.additionals import Direction, DetectionAreas
from models import Database
import random
import dataset
import os
from typing import Dict, Tuple, List
from enum import Enum
from dotenv import load_dotenv
from queue import PriorityQueue

load_dotenv()

ACTUAL_DIRECTIONS = [d for d in Direction if d.is_actual_direction]
GAME = None
DATABASE = Database()

class Algorithm:
    def is_out_of_bounds(self, move, board) -> bool:
        """
        TODO: Docstring
        """
        return (move[0] < 0 or move[1] < 0) or (move[0] > board.size or move[1] > board.size)

    def is_colliding(self, move, snakes) -> bool:
        """
        TODO: Docstring
        """
        for s in snakes:
            for p in s["body"]:
                if (move[0] == p["x"]) and (move[1] == p["y"]):
                    return True
        return False

    def is_head_to_head(self, snake, heads, detection_area, direction, board) -> bool:
        """
        TODO: Docstring
        """
        for coordinate in detection_area[direction]:
            for h in heads:
                opponent = Snake(board.get_snake_by_head(h))

                if (h["x"] == (snake.head[0] + coordinate[0]) and h["y"] == (snake.head[1] + coordinate[1])) and (
                    opponent.length >= snake.length
                ):
                    return True
        return False

    def get_manhattan_distance(self, pos1, pos2):
        """
        TODO: Docstring
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def valid_neighbours(self, location, board):
        """
        TODO: Docstring
        """
        neighbours = []
        for d in ACTUAL_DIRECTIONS:
            coords = (location[0] + d.coords[0], location[1] + d.coords[1])
            if not (self.is_colliding(coords, board.snakes) or self.is_out_of_bounds(coords, board)):
                neighbours.append(coords)
        return neighbours

    def is_towards_food(self, snake, foods, move) -> bool:
        """
        -- Depraceted Function --
        Checks if the Manhattan Distance with the passed Move is less than the current Distance.
        Returns a Bool based on the Condition-Check.
        """
        nearest_food = snake.nearest_food(foods)
        return self.get_manhattan_distance(move, nearest_food) < self.get_manhattan_distance(snake.head, nearest_food)

    def a_star_search(self, snake, board):
        """
        TODO: Docstring
        """
        nearest_food = snake.nearest_food(board.foods)

        queue = PriorityQueue()
        queue.put((0, snake.head))

        came_from = {}
        cost_so_far = {}
        came_from[snake.head] = None
        cost_so_far[snake.head] = 0

        while not queue.empty():
            _, current = queue.get()

            if current == nearest_food:
                break

            for next in self.valid_neighbours(current, board):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.get_manhattan_distance(next, nearest_food)
                    queue.put((priority, next))
                    came_from[next] = current
        return came_from, nearest_food

    def reconstruct_path(self, came_from, start, goal):
        """
        TODO: Docstring
        """
        current = goal
        path = [current]
        while current in came_from and came_from[current] is not None:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def get_safe_moves(self, snake, board) -> List[str]:
        """
        TODO: Docstring
        """
        snakes = board.snakes
        snake_heads = [snake["head"] for snake in snakes]
        safe_moves = []
        removed_directions = []

        for d in ACTUAL_DIRECTIONS:
            new_position = snake.move_position(d.coords)
            if new_position in self.valid_neighbours(snake.head, board):
                if not self.is_head_to_head(snake, snake_heads, snake.detection_area, d.name.lower(), board):
                    safe_moves.append(d.name.lower())
                else:
                    removed_directions.append(d.name.lower())

        if not safe_moves and removed_directions:
            for d in removed_directions:
                safe_moves.append(d)
        return safe_moves

    def get_good_moves(self, snake, board):
        """
        TODO: Docstring
        """
        came_from, nearest_food = self.a_star_search(snake, board)
        path = self.reconstruct_path(came_from, snake.head, nearest_food)

        if len(path) < 2:
            return []

        dx = path[1][0] - snake.head[0]
        dy = path[1][1] - snake.head[1]
        next_move_direction = Direction.get_name_by_direction((dx, dy)).lower()

        return [next_move_direction]

    def execute_move(self, game_state: Dict) -> Dict:
        """
        TODO: Docstring
        """
        snake = Snake(game_state["you"])
        board = Board(game_state["board"])

        safe_moves = self.get_safe_moves(snake, board)
        good_moves = self.get_good_moves(snake, board)
        final_moves = []

        print(f"The safe moves are: {safe_moves}")
        print(f"The good moves are: {good_moves}")

        if safe_moves and good_moves:
            final_moves = [move for move in safe_moves if move in good_moves]

        if final_moves:
            next_move = random.choice(final_moves)
        elif safe_moves:
            next_move = random.choice(safe_moves)
            print(f"No good moves detected...moving {next_move} 'safely'!")
        else:
            next_move = "down"
            print(f"No safe moves detected...moving down!")

        print(f"MOVE {game_state['turn']}: {next_move}")
        return {"move": next_move}


def info() -> Dict:
    """
    TODO: Docstring
    """
    print("INFO")

    return {
        "apiversion": "1",
        "author": "dessher",
        "color": "#a566d1",
        "head": "default",
        "tail": "block-bum",
    }


# "start" is called when your Battlesnake begins a Game
def start(game_state: Dict):
    """
    TODO: Docstring
    """
    GAME = Game(game_state["game"], game_state["turn"])

    if DATABASE.table("games") == None:
        DATABASE.create()

    DATABASE.table("games").insert(
        dict(
            game_id=GAME.game_id,
            replay_link="https://play.battlesnake.com/game/{game_id}".format(game_id=GAME.game_id),
            source=GAME.source,
            game_map=GAME.game_map,
            timeout=GAME.timeout,
        )
    )

    print("GAME START")


# "end" is called when your Battlesnake finishes a Game
def end(game_state: Dict):
    """
    TODO: Docstring
    """
    GAME = Game(game_state["game"], game_state["turn"])

    try:
        winner = game_state["board"]["snakes"][0]["name"] == "PythonicViperidaeUnik"
    except (IndexError, KeyError, TypeError):
        winner = False

    DATABASE.table("games").update(dict(game_id=GAME.game_id, last_turn=GAME.turn, outcome=winner), ['game_id'])
    print("GAME OVER!")


# "move" is called on every Turn and returns your next Move
def move(game_state: Dict) -> Dict:
    """
    TODO: Docstring
    """
    algo = Algorithm()
    return algo.execute_move(game_state)


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
