import json
from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget
from ...saving.maps_manager import MapsManager
from ...scripts.level_editor.level_editor_hexagon import LevelEditorHexagon


class LevelEditorHexagonGridWidget(QWidget):
    def __init__(self, map_name, parent=None):
        self.parent = parent
        super(LevelEditorHexagonGridWidget, self).__init__(self.parent)

        self.hexagon_grid = list()
        all_rows = MapsManager().get_all_rows(map_name)

        for row_ind in range(len(all_rows)):
            self.hexagon_grid.append([])
            for col_ind in range(len(all_rows[row_ind])):
                cell: dict = json.loads(all_rows[row_ind][col_ind])
                new_hex = LevelEditorHexagon(self, col_ind, row_ind, cell)
                self.hexagon_grid[-1].append(new_hex)

        self.now_movement_x, self.now_movement_y = None, None
        self.last_movement_x, self.last_movement_y = None, None
        self.zooming_percent = 100

    def mouseMoveEvent(self, a0):
        x, y = a0.windowPos().x(), a0.windowPos().y()
        if self.last_movement_x is None or self.last_movement_y is None:
            self.last_movement_x, self.last_movement_y = x, y
        self.now_movement_x, self.now_movement_y = x, y
        movement_difference_x = self.now_movement_x - self.last_movement_x
        movement_difference_y = self.now_movement_y - self.last_movement_y
        for hexagon_row in self.hexagon_grid:
            for hexagon in hexagon_row:
                hexagon.camera_x += movement_difference_x
                hexagon.camera_y += movement_difference_y
                hexagon.repaint_hexagon()
        self.last_movement_x, self.last_movement_y = x, y

    def mouseReleaseEvent(self, a0):
        self.last_movement_x, self.last_movement_y = None, None

    def wheelEvent(self, a0):
        plus = 1
        if a0.angleDelta().y() < 0 and self.zooming_percent > 45:
            plus = -1
        self.zooming_percent += plus
        for hexagon_row in self.hexagon_grid:
            for hexagon in hexagon_row:
                hexagon.zoom_percent = self.zooming_percent
                hexagon.repaint_hexagon()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
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
