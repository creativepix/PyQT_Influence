from PyQt5.QtGui import QColor
import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow
from ...saving.statistics_manager import StatisticsManager
from ...scripts.gaming.player import Player


class StatisticsWindow(QMainWindow):
    def __init__(self, statistics_name: str, parent=None):
        super(StatisticsWindow, self).__init__(parent)
        self.setWindowTitle(statistics_name.split(' ')[1].split('_')[0])
        self.setGeometry(100, 100, 500, 500)

        statistics_row = StatisticsManager().get_by_name(statistics_name)

        statistics = dict()

        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.addLegend()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setTitle('Influence Statistics')
        self.graphWidget.setBackground(QColor(0, 0, 0))
        styles = {'color': 'gray', 'font-size': '17px'}
        self.graphWidget.setLabel('left', 'Points', **styles)
        self.graphWidget.setLabel('bottom', 'Phase number', **styles)
        for key, value in statistics_row['statistics'].items():
            player = Player(key, statistics_row['player_names'][key],
                            statistics_row['player_colors'][key])
            statistics[player] = value
        for key in statistics.keys():
            pen = pg.mkPen(color=list(map(int, key.color.split(' '))), width=5)
            self.graphWidget.plot(statistics[key], pen=pen, name=key.name)

        self.show()

    def resize(self):
        self.graphWidget.setGeometry(0, 0, self.size().width(),
                                     self.size().height() - 50)
