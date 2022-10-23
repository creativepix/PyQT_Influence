from PyQt5.QtGui import QColor
import pyqtgraph as pg
from ....saving.statistics_manager import StatisticsManager
from ....scripts.gaming.base_game.hexagon import BaseHexagon
from ....scripts.all_builders import StatisticsTabBuilder, \
    MainUIBuilder
from ....scripts.gaming.map_info import MapInfo


class StatisticsTab(StatisticsTabBuilder):
    def __init__(self, map_info: MapInfo, main_ui: MainUIBuilder):
        self.main_ui = main_ui
        self.map_info = map_info

        self.statistics = dict()
        self.graphWidget = pg.PlotWidget(self.main_ui.statistics_tab_widget)

        self.__post_init__()

    def __post_init__(self):
        self.update_statistics()

    def update_statistics(self):
        self.graphWidget.clear()
        self.graphWidget.addLegend()
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setTitle('Influence Statistics')
        self.graphWidget.setBackground(QColor(0, 0, 0))
        styles = {'color': 'gray', 'font-size': '17px'}
        self.graphWidget.setLabel('left', 'Points', **styles)
        self.graphWidget.setLabel('bottom', 'Phase number', **styles)
        all_players = {}
        for hexagon_row in self.main_ui.game_tab.hexagon_grid:
            for hexagon in hexagon_row:
                hexagon: BaseHexagon = hexagon
                if hexagon.owner is not None:
                    all_players[hexagon.owner] = \
                        all_players.get(hexagon.owner, 0) + hexagon.now_points
        len_stat = max([len(elem) for elem in self.statistics.values()] + [0])
        for player in self.statistics.keys():
            if player not in all_players.keys():
                all_players[player] = 0
        for key, value in all_players.items():
            stat_value = self.statistics.get(key, [0] * len_stat) + [value]
            self.statistics[key] = stat_value

            pen = pg.mkPen(color=list(map(int, key.color.split(' '))), width=5)
            self.graphWidget.plot(self.statistics[key], pen=pen, name=key.name)

    def resize(self):
        self.graphWidget.setGeometry(0, 0, self.main_ui.size().width(),
                                     self.main_ui.size().height() - 50)

    def save_statistics(self):
        statistics_manager = StatisticsManager()
        statistics_manager.save_statistics(self.map_info, self.statistics)
