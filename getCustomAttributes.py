import base64
import json

def encodeObject(obj: dict) -> str:
    """Turns an object into a base64 encoded JSON string for easier transport to
    New Relic.
    """
    return base64.urlsafe_b64encode(json.dumps(obj).encode()).decode()

def getSnakeData(snake: dict) -> str:
    """Gets some useful information about a snake and encodes it. This is necessary to
    keep the custom attribute size under 255bytes.
    """
    return encodeObject({
        "body": snake["body"],
        "head": snake["head"],
        "color": snake["customizations"]["color"]
    })

def getCustomAttributes(data: dict) -> dict:
    game = data["game"]
    board = data["board"]
    you = data["you"]

    attributes = {
        "snakeGameId": game["id"],
        "snakeRules": game["ruleset"]["name"],
        "snakeTurn": data["turn"],

        "snakeBoardHeight": board["height"],
        "snakeBoardWidth": board["width"],
        "snakeBoardFood": encodeObject(board["food"]),
        "snakeBoardHazards": encodeObject(board["hazards"]),

        "snakeName": you["name"],
        "snakeId": you["id"],
        "snakeHealth": you["health"],
        "snakeLength": you["length"],
        "snakeData": getSnakeData(you)
    }

    opponents = [s for s in board["snakes"] if s["id"] != you["id"]]

    for i, snake in enumerate(opponents):
        attributes["snakeOpponent_{}_Name".format(i + 1)] = snake["name"]
        attributes["snakeOpponent_{}_Id".format(i + 1)] = snake["id"]
        attributes["snakeOpponent_{}_Health".format(i + 1)] = snake["health"]
        attributes["snakeOpponent_{}_Length".format(i + 1)] = snake["length"]
        attributes["snakeOpponent_{}_Data".format(i + 1)] = getSnakeData(snake)

    return attributes

def getCustomAttributesEnd(data: dict) -> dict:
    game = data["game"]
    board = data["board"]
    you = data["you"]

    attributes = {
        "snakeGameId": game["id"],
        "snakeRules": game["ruleset"]["name"],
        "snakeTurn": data["turn"],

        "snakeName": you["name"],
        "snakeId": you["id"],
        "snakeHealth": you["health"],
        "snakeLength": you["length"],

        "snakeGameWinnerName": board["snakes"][0]["name"] if len(board["snakes"]) > 0 else None,
        "snakeGameWinnerId":  board["snakes"][0]["id"] if len(board["snakes"]) > 0 else None,
        "snakeGameIsWin": board["snakes"][0]["name"] == you["name"] if len(board["snakes"]) > 0 else False,
        "snakeGameReplayLink": "https://play.battlesnake.com/g/{id}".format(id=game["id"]),
    }

    return attributes