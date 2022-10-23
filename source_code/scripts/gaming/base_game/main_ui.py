from PyQt5.QtWidgets import QMainWindow
from ....scripts.gaming.base_game.game_tab import BaseGameTab
from ....scripts.gaming.base_game.statistics_tab import StatisticsTab
from ....scripts.all_builders import MainUIBuilder, \
    GameTabBuilder, StatisticsTabBuilder
from ....scripts.gaming.map_info import MapInfo
from ....uis.influence_gaming_starting_ui import Ui_MainWindow


class BaseMainUI(QMainWindow, Ui_MainWindow, MainUIBuilder):
    def __init__(self, map_info: MapInfo):
        super().__init__()
        self.setupUi(self)
        self.map_info = map_info
        self.setWindowTitle(self.map_info.map_name)

        self.game_tab: GameTabBuilder = BaseGameTab(self, self.map_info)
        self.statistics_tab: StatisticsTabBuilder = \
            StatisticsTab(self.map_info, self)

        self.tab_widget.currentChanged.connect(self.change_active_tab)

        self.__post_init__()

    def __post_init__(self):
        pass

    def change_active_tab(self, index):
        if index == 0:
            self.game_tab.show_grid()
        else:
            self.game_tab.hide_grid()

    def mouseMoveEvent(self, a0):
        if self.tab_widget.currentIndex() == 0:
            self.game_tab.mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0):
        if self.tab_widget.currentIndex() == 0:
            self.game_tab.mouseReleaseEvent(a0)

    def wheelEvent(self, a0):
        if self.tab_widget.currentIndex() == 0:
            self.game_tab.wheelEvent(a0)

    def resizeEvent(self, a0):
        self.game_tab.resize()
        self.statistics_tab.resize()
