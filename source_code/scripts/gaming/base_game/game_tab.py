import json
from typing import List
from ....saving.maps_manager import MapsManager
from ....scripts.gaming import base_game
from ....scripts import all_builders
from ....scripts.all_builders import MainUIBuilder, HexagonBuilder
from ....scripts.gaming.map_info import MapInfo


class BaseGameTab(all_builders.GameTabBuilder):
    def __init__(self, main_ui: MainUIBuilder, map_info: MapInfo):
        self.main_ui = main_ui
        self.map_info = map_info

        self.main_ui.reinforcement_points.hide()
        self.main_ui.reinforcement_points_label.hide()
        self.main_ui.next_phase_btn.clicked.connect(
            self.map_info.game_class.transition_phase)
        self.main_ui.skip_btn.clicked.connect(
            self.map_info.game_class.transition_phase)
        self.main_ui.plus_one_btn.clicked.connect(
            self.map_info.game_class.plus_one_clicked)
        self.main_ui.max_btn.clicked.connect(
            self.map_info.game_class.max_clicked)

        hex_grid_widget = base_game.hexagon_grid_widget.BaseHexagonGridWidget
        self.widget_hexagon_grid = hex_grid_widget(self.main_ui.centralwidget)
        self.widget_hexagon_grid.setObjectName("widget_hexagon_grid")

        self.hexagon_grid: List[List[HexagonBuilder]] = []

        self.last_movement_x, self.last_movement_y = None, None
        self.now_movement_x, self.now_movement_y = 0, 0

        self.zooming_percent = 75

        self.__post_init__()

    def __post_init__(self):
        self._init_make_map()

    def hide_grid(self):
        self.widget_hexagon_grid.hide()

    def show_grid(self):
        self.widget_hexagon_grid.show()

    def resize(self):
        w, h = self.main_ui.size().width(), self.main_ui.size().height()
        self.widget_hexagon_grid.setGeometry(5, 109, w - 15, h - 116)
        self.main_ui.tab_widget.setGeometry(self.main_ui.tab_widget.x(),
                                            self.main_ui.tab_widget.y(),
                                            w + 1, h + 1)

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

    def end_game(self, winner):
        self.main_ui.attack_phase.setEnabled(False)
        self.main_ui.reinforcement_phase.setEnabled(False)
        self.main_ui.status_text.setText(f'Игрок {winner.name} победил!')

    def _init_make_map(self):
        all_rows = MapsManager().get_all_rows(self.map_info.map_name)

        for row_ind in range(len(all_rows)):
            self.hexagon_grid.append([])
            for col_ind in range(len(all_rows[row_ind])):
                cell: dict = json.loads(all_rows[row_ind][col_ind])
                new_hex = base_game.hexagon.BaseHexagon(self.map_info,
                                                        self.widget_hexagon_grid,
                                                        col_ind, row_ind, cell,
                                                        zoom_percent=
                                                    self.zooming_percent)
                self.hexagon_grid[-1].append(new_hex)
        self.widget_hexagon_grid.hexagon_grid = self.hexagon_grid
