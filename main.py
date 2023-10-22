from objects import Snake, Board
from objects.additionals import Direction, DetectionAreas
import random
from typing import Dict, Tuple, List
from enum import Enum

ACTUAL_DIRECTIONS = [d for d in Direction if d.is_actual_direction]

class Algorithm:
    def is_out_of_bounds(self, move, board) -> bool:
        return (move[0] < 0 or move[1] < 0) or (move[0] > board.size or move[1] > board.size)

    def is_colliding(self, move, snakes) -> bool:
        for s in snakes:
            for p in s["body"]:
                if (move[0] == p["x"]) and (move[1] == p["y"]):
                    return True
        return False

    def is_head_to_head(self, snake, heads, detection_area, direction, board) -> bool:
        print(f"The Detection-Area is: {detection_area}")

        for coordinate in detection_area[direction]:
            for h in heads:
                opponent = Snake(board.get_snake_by_head(h))

                if (h["x"] == (snake.head[0] + coordinate[0]) and h["y"] == (snake.head[1] + coordinate[1])) and (
                    opponent.length >= snake.length
                ):
                    return True
        return False

    def is_towards_food(self, snake, foods, move) -> bool:
        nearest_food = snake.nearest_food(foods)

        return ((abs((move[0]) - nearest_food[0])) < (abs((snake.head[0]) - nearest_food[0]))) or (
            (abs((move[1]) - nearest_food[1])) < (abs((snake.head[1]) - nearest_food[1]))
        )

    def get_safe_moves(self, snake, board) -> List[str]:
        snakes = board.snakes

        snake_heads = [snake["head"] for snake in snakes]
        safe_moves = []
        removed_directions = []

        for d in ACTUAL_DIRECTIONS:
            new_position = snake.move_position(d.coords)
            if not self.is_out_of_bounds(new_position, board) and not self.is_colliding(new_position, snakes):
                if not self.is_head_to_head(snake, snake_heads, snake.detection_area, d.name.lower(), board):
                    safe_moves.append(d.name.lower())
                else:
                    removed_directions.append(d.name.lower())

        if not safe_moves and removed_directions:
            for d in removed_directions:
                safe_moves.append(d)
        return safe_moves

    def get_good_moves(self, snake, board) -> List[str]:
        foods = board.foods

        good_moves = []

        for d in ACTUAL_DIRECTIONS:
            new_position = snake.move_position(d.coords)
            if self.is_towards_food(snake, foods, new_position):
                good_moves.append(d.name.lower())
        return good_moves

    def execute_move(self, game_state: Dict) -> Dict:
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
    print("INFO")

    return {
        "apiversion": "1",
        "author": "dessher",
        "color": "#a566d1",
        "head": "do-sammy",
        "tail": "mlh-gene",
    }


# start is called when your Battlesnake begins a game
def start(game_state: Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: Dict):
    print("GAME OVER!")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: Dict) -> Dict:
    algo = Algorithm()
    return algo.execute_move(game_state)


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
