from typing import Dict


class Board:
    def __init__(self, board: Dict) -> None:
        self._width = board["width"]
        self._height = board["height"]
        self._snakes = board["snakes"]
        self._foods = board["food"]

    @property
    def width(self) -> int:
        """
        Get the Width of the Board.
        Returns an Int of the Size accordingly.
        """
        return self._width

    @property
    def height(self) -> int:
        """
        Get the Height of the Board.
        Returns an Int of the Size accordingly.
        """
        return self._height

    @property
    def size(self) -> int:
        """
        Get the Size of the Board.
        Returns an Int of the Size (as Coordinates begin on 0).
        """
        return ((self._width + self._height) / 2) - 1

    @property
    def snakes(self) -> Dict:
        """
        TODO: Docstring
        """
        return self._snakes

    @property
    def foods(self) -> Dict:
        """
        TODO: Docstring
        """
        return self._foods

    def get_snake_by_head(self, head):
        """
        TODO: Docstring
        """

        for s in self._snakes:
            if s["head"] == head:
                return s
        return {}
