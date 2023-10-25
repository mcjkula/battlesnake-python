class Game:
    def __init__(self, game, turn):
        self._game_id = game["id"]
        self._source = game["source"]
        self._game_map = game["map"]
        self._timeout = game["timeout"]
        self._turn = turn

    @property
    def game_id(self):
        return self._game_id

    @property
    def source(self):
        return self._source

    @property
    def game_map(self):
        return self._game_map

    @property
    def timeout(self):
        return self._timeout

    @property
    def turn(self):
        return self._turn