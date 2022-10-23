from ....scripts.gaming.base_game.game import BaseInfluenceGame, PhasesEnum
from ....scripts.all_builders import HexagonBuilder, MainUIBuilder, \
    StatisticsTabBuilder, GameTabBuilder
from ....scripts.gaming.blindness_game.main_ui import BlindnessMainUI
from ....scripts.gaming.map_info import MapInfo


class BlindnessInfluenceGame(BaseInfluenceGame):
    def __init__(self, map_info: MapInfo):
        super().__init__(map_info)
        self.main_ui: MainUIBuilder = BlindnessMainUI(self.map_info)
        self.statistics_tab: StatisticsTabBuilder = self.main_ui.statistics_tab
        self.game_tab: GameTabBuilder = self.main_ui.game_tab
        self.main_ui.show()

        super().__post_init__()

    def __post_init__(self):
        pass
