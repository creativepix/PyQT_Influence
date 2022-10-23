from typing import List
from ...scripts.gaming.player import Player


class MapInfo:
    def __init__(self, map_name: str, game_type: str, player_nums: int,
                 all_players_query: List[Player]):
        self.map_name = map_name
        self.game_type = game_type
        self.player_nums = player_nums
        self.all_players_query = all_players_query
        self.game_class = None

    def setGameClass(self, game_class):
        self.game_class = game_class
