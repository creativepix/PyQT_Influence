from typing import List
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen

from ....scripts.all_builders import HexagonGridWidgetBuilder, \
    HexagonBuilder


class BaseHexagonGridWidget(HexagonGridWidgetBuilder, QWidget):
    def __init__(self, parent: QWidget,
                 hexagon_grid: List[List[HexagonBuilder]] = None):
        self.parent = parent
        super(QWidget, self).__init__(self.parent)
        self.hexagon_grid = hexagon_grid

        self.__post_init__()

    def __post_init__(self):
        pass

    def paintEvent(self, a0):
        self.parent.update()
        painter = QPainter(self)
        painter.setPen(QPen(Qt.gray, 2, Qt.SolidLine))

        painter.begin(self.parent)

        for row_ind in range(len(self.hexagon_grid)):
            for col_ind in range(len(self.hexagon_grid[row_ind])):
                hexagon = self.hexagon_grid[row_ind][col_ind]
                if not hexagon.is_drawing or not hexagon.is_exist:
                    continue
                lines = hexagon.lines.split(' ')

                from_x = int(hexagon.pos().x() + hexagon.width() / 2)
                from_y = int(hexagon.pos().y() + hexagon.height() / 2)

                try:
                    hexagon2 = self.hexagon_grid[row_ind][col_ind + 1]
                    if not hexagon2.is_drawing:
                        raise IndexError
                    lines2 = hexagon2.lines.split(' ')
                    if lines2[2] == '1' or lines[3] == '1':
                        to_x = int(from_x + hexagon.width() * 2)
                        to_y = from_y
                        painter.drawLine(from_x, from_y, to_x, to_y)
                except IndexError:
                    pass

                try:
                    if row_ind % 2 == 0:
                        hexagon2 = self.hexagon_grid[row_ind + 1][col_ind - 1]
                        if col_ind - 1 < 0:
                            raise IndexError
                    else:
                        hexagon2 = self.hexagon_grid[row_ind + 1][col_ind]
                    if not hexagon2.is_drawing:
                        raise IndexError
                    lines2 = hexagon2.lines.split(' ')
                    if lines2[1] == '1' or lines[4] == '1':
                        to_x = int(from_x - hexagon.width())
                        to_y = int(from_y + hexagon.width() * 1.5)
                        painter.drawLine(from_x, from_y, to_x, to_y)
                except IndexError:
                    pass

                try:
                    if row_ind % 2 == 0:
                        hexagon2 = self.hexagon_grid[row_ind + 1][col_ind]
                    else:
                        hexagon2 = self.hexagon_grid[row_ind + 1][col_ind + 1]
                    if not hexagon2.is_drawing:
                        raise IndexError
                    lines2 = hexagon2.lines.split(' ')
                    if lines2[0] == '1' or lines[5] == '1':
                        to_x = int(from_x + hexagon.width())
                        to_y = int(from_y + hexagon.width() * 1.5)
                        painter.drawLine(from_x, from_y, to_x, to_y)
                except IndexError:
                    pass

        painter.end()
