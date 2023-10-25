from typing import Dict, Tuple
from .additionals import Direction, DetectionAreas
import random


class Snake:
    def __init__(self, snake: Dict) -> None:
        self._head = snake["head"]
        self._neck = None
        self._length = snake["length"]

        if len(snake["body"]) > 1:
            self._neck = snake["body"][1]

    @property
    def head(self) -> Tuple[int, int]:
        return (self._head["x"], self._head["y"])

    @property
    def neck(self) -> Tuple[int, int]:
        """
        Get the Coordinates of the Neck (if there is no Neck yet, it will just get the coordinates of the Head).
        Returns a Tuple with them accordingly.
        """
        if self._neck is not None:
            return (self._neck["x"], self._neck["y"])
        return self.head

    @property
    def length(self) -> int:
        return self._length

    @property
    def direction(self) -> Tuple[int, int]:
        """
        Get the Direction of the Snake, based on the Coordinate-Delta from Head to Neck.
        Returns a Tuple with (dx, dy), where "dx" is the X-Delta and "dy" the Y-Delta.
        """
        if self._neck is not None:
            dx = self._head["x"] - self._neck["x"]
            dy = self._head["y"] - self._neck["y"]
            return (dx, dy)
        return (0, 0)

    @property
    def detection_area(self) -> Dict:
        direction = Direction.get_name_by_direction(self.direction)
        return DetectionAreas.get_area_by_direction(direction)

    def move_position(self, move) -> Tuple[int, int]:
        """
        Get the Coordinates of the current Position with the currently given Move.
        Returns a Tuple with them accordingly.
        """
        return (self.head[0] + move[0], self.head[1] + move[1])

    def nearest_food(self, foods) -> Tuple[int, int]:
        """
        TODO: Docstring
        """
        nearest_food = None
        min_distance = float('inf')

        for f in foods:
            distance = abs(self.head[0] - f["x"]) + abs(self.head[1] - f["y"])

            if distance < min_distance:
                min_distance = distance
                nearest_food = (f["x"], f["y"])

        return nearest_food
