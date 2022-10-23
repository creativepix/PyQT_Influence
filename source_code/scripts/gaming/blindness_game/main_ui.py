from PyQt5.QtWidgets import QMainWindow

from ....scripts.all_builders import GameTabBuilder, StatisticsTabBuilder
from ....scripts.gaming.base_game.main_ui import BaseMainUI
from ....scripts.gaming.base_game.statistics_tab import StatisticsTab
from ....scripts.gaming.blindness_game.game_tab import BlindnessGameTab
from ....scripts.gaming.map_info import MapInfo


class BlindnessMainUI(BaseMainUI):
    def __init__(self, map_info: MapInfo):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        self.map_info = map_info
        self.setWindowTitle(self.map_info.map_name)

        self.game_tab: GameTabBuilder = BlindnessGameTab(self, self.map_info)
        self.statistics_tab: StatisticsTabBuilder = \
            StatisticsTab(self.map_info, self)

        self.tab_widget.currentChanged.connect(self.change_active_tab)

        super().__post_init__()
