from enum import Enum


class DetectionAreas(Enum):
    NONE = {
        "left": [],
        "up": [],
        "right": [],
        "down": [],
    }
    LEFT = {
        "left": [(-2, 0), (-1, -1), (-1, 1)],
        "up": [(1, 1), (0, 2), (-1, 1)],
        "right": [],
        "down": [(1, -1), (0, -2), (-1, -1)],
    }
    UP = {
        "left": [(-1, -1), (-2, 0), (-1, 1)],
        "up": [(0, 2), (-1, 1), (1, 1)],
        "right": [(1, -1), (2, 0), (1, 1)],
        "down": [],
    }
    RIGHT = {
        "left": [],
        "up": [(1, 1), (0, 2), (-1, 1)],
        "right": [(2, 0), (1, 1), (1, -1)],
        "down": [(1, -1), (0, -2), (-1, -1)],
    }
    DOWN = {
        "left": [(-1, 1), (-2, 0), (-1, -1)],
        "up": [],
        "right": [(1, 1), (2, 0), (1, -1)],
        "down": [(0, -2), (1, -1), (-1, -1)],
    }

    @classmethod
    def get_area_by_direction(cls, name):
        """
        TODO: Docstring
        """
        for a in cls:
            if a.name == name:
                return a.value
