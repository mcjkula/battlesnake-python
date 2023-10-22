from enum import Enum

class Direction(Enum):
    NONE = (0, 0, False)
    LEFT = (-1, 0, True)
    UP = (0, 1, True)
    RIGHT = (1, 0, True)
    DOWN = (0, -1, True)

    @property
    def is_actual_direction(self):
        return self.value[2]

    @property
    def coords(self):
        return self.value[:2]

    @classmethod
    def get_name_by_direction(cls, value):
        for d in cls:
            if d.coords == value:
                return d.name
