from ...constants import GAME_TYPE_IDS
from ...scripts import gaming
from ...scripts.gaming.map_info import MapInfo


def load_game(map_info: MapInfo):
    if map_info.game_type == GAME_TYPE_IDS[0]:
        gaming.base_game.game.BaseInfluenceGame(map_info)
    elif map_info.game_type == GAME_TYPE_IDS[1]:
        gaming.blindness_game.game.BlindnessInfluenceGame(map_info)
