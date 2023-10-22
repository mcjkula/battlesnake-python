import random
import typing


def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "dessher",
        "color": "#a566d1",
        "head": "do-sammy",
        "tail": "mlh-gene",
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER!")

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]
    my_neck = game_state["you"]["body"][1]
    body_length = game_state["you"]["length"]

    body_direction = {"x": (my_head["x"] - my_neck["x"]), "y": (my_head["y"] - my_neck["y"])}

    if body_length > 1:
        head_detect_left = None
        head_detect_top = None
        head_detect_right = None

        match body_direction:
            case {"x": 1, "y": 0}:
                head_detect_left = {
                    "0": {"x": (my_head["x"] - 1), "y": my_head["y"] + 1},
                    "1": {"x": my_head["x"], "y": (my_head["y"] + 2)},
                    "2": {"x": (my_head["x"] + 1), "y": (my_head["y"] + 1)},
                }
                head_detect_top = {
                    "0": {"x": (my_head["x"] + 2), "y": my_head["y"]},
                    "1": {"x": (my_head["x"] + 1), "y": (my_head["y"] + 1)},
                    "2": {"x": (my_head["x"] + 1), "y": (my_head["y"] - 1)},
                }
                head_detect_right = {
                    "0": {"x": (my_head["x"] - 1), "y": my_head["y"] - 1},
                    "1": {"x": my_head["x"], "y": (my_head["y"] - 2)},
                    "2": {"x": (my_head["x"] + 1), "y": (my_head["y"] - 1)},
                }
            case {"x": -1, "y": 0}:
                head_detect_left = {
                    "0": {"x": (my_head["x"] + 1), "y": my_head["y"] - 1},
                    "1": {"x": my_head["x"], "y": (my_head["y"] - 2)},
                    "2": {"x": (my_head["x"] - 1), "y": (my_head["y"] - 1)},
                }
                head_detect_top = {
                    "0": {"x": (my_head["x"] - 2), "y": my_head["y"]},
                    "1": {"x": (my_head["x"] - 1), "y": (my_head["y"] - 1)},
                    "2": {"x": (my_head["x"] - 1), "y": (my_head["y"] + 1)},
                }
                head_detect_right = {
                    "0": {"x": (my_head["x"] + 1), "y": my_head["y"] + 1},
                    "1": {"x": my_head["x"], "y": (my_head["y"] - 2)},
                    "2": {"x": (my_head["x"] - 1), "y": (my_head["y"] + 1)},
                }
            case {"x": 0, "y": 1}:
                head_detect_left = {
                    "0": {"x": (my_head["x"] - 1), "y": my_head["y"] - 1},
                    "1": {"x": (my_head["x"] - 2), "y": my_head["y"]},
                    "2": {"x": (my_head["x"] - 1), "y": (my_head["y"] + 1)},
                }
                head_detect_top = {
                    "0": {"x": my_head["x"], "y": (my_head["y"] + 2)},
                    "1": {"x": (my_head["x"] - 1), "y": (my_head["y"] + 1)},
                    "2": {"x": (my_head["x"] + 1), "y": (my_head["y"] + 1)},
                }
                head_detect_right = {
                    "0": {"x": (my_head["x"] + 1), "y": my_head["y"] - 1},
                    "1": {"x": (my_head["x"] + 2), "y": my_head["y"]},
                    "2": {"x": (my_head["x"] + 1), "y": (my_head["y"] + 1)},
                }
            case {"x": 0, "y": -1}:
                head_detect_left = {
                    "0": {"x": (my_head["x"] + 1), "y": my_head["y"] + 1},
                    "1": {"x": (my_head["x"] - 2), "y": my_head["y"]},
                    "2": {"x": (my_head["x"] - 1), "y": (my_head["y"] - 1)},
                }
                head_detect_top = {
                    "0": {"x": my_head["x"], "y": (my_head["y"] - 2)},
                    "1": {"x": (my_head["x"] - 1), "y": (my_head["y"] - 1)},
                    "2": {"x": (my_head["x"] + 1), "y": (my_head["y"] - 1)},
                }
                head_detect_right = {
                    "0": {"x": (my_head["x"] - 1), "y": my_head["y"] + 1},
                    "1": {"x": (my_head["x"] + 2), "y": my_head["y"]},
                    "2": {"x": (my_head["x"] + 1), "y": (my_head["y"] - 1)},
                }
    else:
        pass

    if my_neck["x"] < my_head["x"]:
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds

    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]

    if my_head["x"] == 0:
        is_move_safe["left"] = False

    if my_head["x"] - (board_width - 1) == 0:
        is_move_safe["right"] = False

    if my_head["y"] - (board_height - 1) == 0:
        is_move_safe["up"] = False

    if my_head["y"] == 0:
        is_move_safe["down"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself

    my_body = game_state["you"]["body"]

    for part in my_body:
        if (my_head["x"] - 1) == part["x"] and my_head["y"] == part["y"]:
            is_move_safe["left"] = False
        if (my_head["x"] + 1) == part["x"] and my_head["y"] == part["y"]:
            is_move_safe["right"] = False
        if my_head["x"] == part["x"] and (my_head["y"] + 1) == part["y"]:
            is_move_safe["up"] = False
        if my_head["x"] == part["x"] and (my_head["y"] - 1) == part["y"]:
            is_move_safe["down"] = False

    # TODO: Step 2.1 - Prevention for "Greed"/Self-Destroy



    # TODO: Step 3 - Prevention for colliding with other Battlesnakes

    all_snakes = game_state["board"]["snakes"]

    opponents = [s for s in all_snakes if s['name'] != 'PythonicViperidaeUnik']

    for opponent in opponents:
        opponent_body = opponent["body"]

        for part in opponent_body:
            if ((my_head["x"] - 1) == part["x"] and my_head["y"] == part["y"]):
                is_move_safe["left"] = False
            if ((my_head["x"] + 1) == part["x"] and my_head["y"] == part["y"]):
                is_move_safe["right"] = False
            if (my_head["x"] == part["x"] and (my_head["y"] + 1) == part["y"]):
                is_move_safe["up"] = False
            if (my_head["x"] == part["x"] and (my_head["y"] - 1) == part["y"]):
                is_move_safe["down"] = False

        # TODO: Step 3.1 - Prevention for Head-to-Head-Situations

        if body_length > 1 and body_length <= opponent["length"]:
            opponent_head = opponent["head"]

            match body_direction:
                case {"x": 1, "y": 0}:
                    for key, coordinate in head_detect_left.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["up"] = False
                    for key, coordinate in head_detect_top.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["right"] = False
                    for key, coordinate in head_detect_right.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["down"] = False
                case {"x": -1, "y": 0}:
                    for key, coordinate in head_detect_left.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["down"] = False
                    for key, coordinate in head_detect_top.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["left"] = False
                    for key, coordinate in head_detect_right.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["up"] = False
                case {"x": 0, "y": 1}:
                    for key, coordinate in head_detect_left.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["left"] = False
                    for key, coordinate in head_detect_top.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["up"] = False
                    for key, coordinate in head_detect_right.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["right"] = False
                case {"x": 0, "y": -1}:
                    for key, coordinate in head_detect_left.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["left"] = False
                    for key, coordinate in head_detect_top.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["down"] = False
                    for key, coordinate in head_detect_right.items():
                        if opponent_head["x"] == coordinate["x"] and opponent_head["y"] == coordinate["y"]:
                            is_move_safe["right"] = False
        else:
            pass

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # TODO: Move towards food instead of random, to regain health and survive longer

    skip_flag = True
    foods = game_state['board']['food']
    nearest_food = None
    is_good_move = {"up": False, "down": False, "left": False, "right": False}

    for food in foods:
        distance_to_food = {"x": abs(my_head["x"] - food["x"]), "y": abs(my_head["y"] - food["y"])}

        if not skip_flag:
            if distance_to_food["x"] < prev_distance_to_food["x"] and distance_to_food["y"] < prev_distance_to_food["y"]:
                nearest_food = food

        skip_flag = False
        prev_distance_to_food = {"x": abs(my_head["x"] - food["x"]), "y": abs(my_head["y"] - food["y"])}

    for move in safe_moves:
        if move == "left":
            is_good_move[move] = (abs((my_head["x"] - 1) - nearest_food["x"])) < (abs((my_head["x"]) - nearest_food["x"]))
        if move == "right":
            is_good_move[move] = (abs((my_head["x"] + 1) - nearest_food["x"])) < (abs((my_head["x"]) - nearest_food["x"]))
        if move == "up":
             is_good_move[move] = (abs((my_head["y"] + 1) - nearest_food["y"])) < (abs((my_head["y"]) - nearest_food["y"]))
        if move == "down":
            is_good_move[move] = (abs((my_head["y"] - 1) - nearest_food["y"])) < (abs((my_head["y"]) - nearest_food["y"]))

    good_moves = []
    for move, isGood in is_good_move.items():
        if isGood:
            good_moves.append(move)

    if len(good_moves) == 0:
        return {"move": random.choice(safe_moves)}

    # Choose a random move from the safe ones
    next_move = random.choice(good_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
