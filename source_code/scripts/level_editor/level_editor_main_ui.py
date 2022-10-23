from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from ...saving.maps_manager import MapsManager
from ...scripts.level_editor.level_editor_hexagon import LevelEditorHexagon
from ...scripts.level_editor.level_editor_hexagon_grid_widget import \
    LevelEditorHexagonGridWidget
from ...uis.level_editor_ui import Ui_MainWindow


NULL_COLOR = '100 100 0'


class LevelEditorUI(QMainWindow, Ui_MainWindow):
    def __init__(self, map_name, main_ui):
        super().__init__()
        self.setupUi(self)
        self.main_ui = main_ui
        if not self.main_ui.widget_level_editor_menu.isHidden():
            self.main_ui.go_level_editor_menu()

        self.map_name = map_name

        # обязательно при изменении количества режимов
        self.game_types_boxes = [self.game_type_classic_checkbox,
                                 self.game_type_blindness_checkbox]
        self.rad_btns = [self.set_points_radbtn, self.set_max_radbtn,
                         self.set_player_radbtn, self.edit_lines_radbtn,
                         self.edit_cells_radbtn]
        self.last_selected_hexagon = None
        for rad_btn in self.rad_btns:
            def reset_last_selected_hexagon():
                if self.last_selected_hexagon is not None:
                    self.last_selected_hexagon.is_selected = False
                    self.last_selected_hexagon = None
            rad_btn.toggled.connect(reset_last_selected_hexagon)

        maps_manager = MapsManager()
        game_types = maps_manager.get_game_types(self.map_name)
        for game_type_box in self.game_types_boxes:
            if game_type_box.text() in game_types:
                game_type_box.setChecked(True)
        self.rad_btns[0].setChecked(True)
        self.map_name_edit.setText(self.map_name)

        self.save_btn.clicked.connect(self.save_map)
        self.linear_player_ids_btn.clicked.connect(self.linear_player_ids)

        self.hexagon_grid_widget = LevelEditorHexagonGridWidget(self.map_name,
                                                                self)

        self.show()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        w, h = a0.size().width(), a0.size().height()
        self.hexagon_grid_widget.setGeometry(0, 100, w, h - 100)

    def get_checked_setting_id(self):
        for i in range(len(self.rad_btns)):
            if self.rad_btns[i].isChecked():
                return i
        return None

    def linear_player_ids(self):
        all_rows = self.hexagon_grid_widget.hexagon_grid
        all_player_ids = set()
        new_all_player_ids = dict()
        min_ = 0
        for hexagon_col in all_rows:
            for hexagon in hexagon_col:
                if hexagon.owner_id is not None:
                    all_player_ids.add(hexagon.owner_id)
        for player_id in sorted(list(all_player_ids)):
            if player_id not in new_all_player_ids.keys():
                new_all_player_ids[player_id] = min_
                min_ += 1
        for hexagon_col in all_rows:
            for hexagon in hexagon_col:
                if hexagon.owner_id is not None:
                    hexagon.owner_id = new_all_player_ids[hexagon.owner_id]
                    hexagon.repaint_hexagon()

    def hexagon_select(self, hexagon: LevelEditorHexagon):
        setting_id = self.get_checked_setting_id()
        if not hexagon.is_drawing and setting_id != 4:
            return
        if setting_id in [0, 1, 2]:
            # создаётся новый стандартный диалог, так как обычный
            # QInputDialog.getInt(...) при использовании будет цветом заднего
            # фона окна, то есть чёрного, и ничего не будет видно
            dialog = QtWidgets.QInputDialog(self)
            dialog.setInputMode(QtWidgets.QInputDialog.InputMode.IntInput)
            dialog.setStyleSheet('background-color: white')
        if setting_id == 0:
            dialog.setWindowTitle('Начальное количество очков')
            dialog.setLabelText('Введите начальное количество очков: ')
            dialog.setIntMinimum(0)
            dialog.setIntValue(0)
            dialog.setIntMaximum(hexagon.max_points)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                hexagon.now_points = dialog.intValue()
        elif setting_id == 1:
            dialog.setWindowTitle('Максимальное количество очков')
            dialog.setLabelText('Введите максимальное количество очков: ')
            dialog.setIntMinimum(1)
            dialog.setIntValue(8)
            dialog.setIntMaximum(999)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                hexagon.max_points = dialog.intValue()
        elif setting_id == 2:
            dialog.setWindowTitle('Player_id')
            dialog.setLabelText('Введите начальное player_id в очереди: ')
            dialog.setIntMinimum(-1)
            dialog.setIntValue(-1)
            dialog.setIntMaximum(20)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                hexagon.owner_id = dialog.intValue() if dialog.intValue() \
                                                        > -1 else None
        elif setting_id == 3:
            if not hexagon.is_drawing:
                return
            if self.last_selected_hexagon is None:
                self.last_selected_hexagon = hexagon
                self.last_selected_hexagon.is_selected = True
            else:
                def reverse_int_str(num):
                    return '0' if num == '1' else '1'

                new_lines1 = hexagon.lines.split(' ')
                new_lines2 = self.last_selected_hexagon.lines.split(' ')
                if hexagon.y == self.last_selected_hexagon.y:
                    if hexagon.x + 1 == self.last_selected_hexagon.x:
                        new_lines1[3] = reverse_int_str(new_lines1[3])
                        new_lines2[2] = reverse_int_str(new_lines2[2])
                    elif hexagon.x - 1 == self.last_selected_hexagon.x:
                        new_lines1[2] = reverse_int_str(new_lines1[2])
                        new_lines2[3] = reverse_int_str(new_lines2[3])
                elif hexagon.y - 1 == self.last_selected_hexagon.y:
                    hexagon, self.last_selected_hexagon = \
                        self.last_selected_hexagon, hexagon
                    new_lines1, new_lines2 = new_lines2, new_lines1
                if hexagon.y + 1 == self.last_selected_hexagon.y:
                    if self.last_selected_hexagon.y % 2 == 0:
                        if hexagon.x == self.last_selected_hexagon.x:
                            new_lines1[4] = reverse_int_str(new_lines1[4])
                            new_lines2[1] = reverse_int_str(new_lines2[1])
                        elif hexagon.x + 1 == self.last_selected_hexagon.x:
                            new_lines1[5] = reverse_int_str(new_lines1[5])
                            new_lines2[0] = reverse_int_str(new_lines2[0])
                    else:
                        if hexagon.x == self.last_selected_hexagon.x:
                            new_lines1[5] = reverse_int_str(new_lines1[5])
                            new_lines2[0] = reverse_int_str(new_lines2[0])
                        elif hexagon.x - 1 == self.last_selected_hexagon.x:
                            new_lines1[4] = reverse_int_str(new_lines1[4])
                            new_lines2[1] = reverse_int_str(new_lines2[1])
                hexagon.lines = ' '.join(new_lines1)
                self.last_selected_hexagon.lines = ' '.join(new_lines2)

                hexagon.is_selected = False
                self.last_selected_hexagon.is_selected = False
                self.last_selected_hexagon = None
        elif setting_id == 4:
            hexagon.is_exist = not hexagon.is_exist
            hexagon.is_drawing = hexagon.is_exist
            hexagon.owner_id = None

        hexagon.repaint_hexagon()

    def save_map(self):
        maps_manager = MapsManager()
        db = maps_manager.get_db()
        cursor = db.cursor()

        self.linear_player_ids()
        if self.map_name != self.map_name_edit.text():
            maps_manager.rename_map(self.map_name, self.map_name_edit.text(),
                                    cursor)
            self.map_name = self.map_name_edit.text()

        new_game_types = []
        for game_type_box in self.game_types_boxes:
            if game_type_box.isChecked():
                new_game_types.append(game_type_box.text())
        maps_manager.set_game_types(self.map_name, new_game_types, cursor)

        maps_manager.set_hexagons(self.map_name,
                                  self.hexagon_grid_widget.hexagon_grid,
                                  cursor)

        db.commit()

        if not self.main_ui.widget_level_editor_menu.isHidden():
            self.main_ui.go_level_editor_menu()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Saved")
        msg.setInformativeText('Map was successfully saved')
        msg.setWindowTitle("Saving")
        msg.exec_()
