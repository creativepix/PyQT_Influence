import random
import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialogButtonBox, \
    QRadioButton, QLabel, QPushButton, QLineEdit, QColorDialog, \
    QWidget, QVBoxLayout, QHBoxLayout
from ...saving.maps_manager import MapsManager
from ...saving.statistics_manager import StatisticsManager
from ...scripts.gaming import choose_game
from ...scripts.gaming.map_info import MapInfo
from ...scripts.gaming.player import Player
from ...scripts.level_editor.level_editor_main_ui import LevelEditorUI
from ...scripts.statistics.statistics_window import StatisticsWindow
from ...uis.choosing_filter_main_menu import Ui_ChoosingFilterMainMenu
from ...uis.choosing_game_feature_main_menu import Ui_ChoosingGameFeature
from ...uis.home_main_menu import Ui_HomeMainMenu
from ...uis.level_editor_main_menu import Ui_LevelEditorMainMenu


class MainMenuWindow(QMainWindow):
    def __init__(self):
        super(MainMenuWindow, self).__init__()
        self.setWindowTitle('MainMenu')
        self.setFixedSize(325, 415)

        self.widget_home_menu = QWidget(self)
        self.widget_level_editor_menu = QWidget(self)
        self.widget_choosing_filter_menu = QWidget(self)
        self.widget_choosing_game_feature_menu = QWidget(self)

        self.ui_home_menu = Ui_HomeMainMenu()
        self.ui_level_editor_menu = Ui_LevelEditorMainMenu()
        self.ui_choosing_filter_menu = Ui_ChoosingFilterMainMenu()
        self.ui_choosing_game_feature_menu = Ui_ChoosingGameFeature()

        self.ui_home_menu.setupUi(self.widget_home_menu)
        self.ui_level_editor_menu.setupUi(self.widget_level_editor_menu)
        self.ui_choosing_filter_menu.setupUi(self.widget_choosing_filter_menu)
        self.ui_choosing_game_feature_menu.setupUi(
            self.widget_choosing_game_feature_menu)

        self.ui_home_menu.level_editor_btn.clicked.connect(
            self.go_level_editor_menu)
        self.ui_home_menu.play_btn.clicked.connect(self.go_choosing_filter(0))
        self.ui_home_menu.statistics_btn.clicked.connect(
            self.go_choosing_filter(1))

        self.ui_level_editor_menu.delet_btn.clicked.connect(
            self.delete_save_level_editor)
        self.ui_level_editor_menu.button_box.button(
            QDialogButtonBox.Ok).clicked.connect(self.ok_level_editor)
        self.ui_level_editor_menu.button_box.button(
            QDialogButtonBox.Cancel).clicked.connect(self.go_home)

        self.ui_choosing_filter_menu.button_box.button(
            QDialogButtonBox.Cancel).clicked.connect(self.go_home)

        self.ui_choosing_game_feature_menu.button_box.button(
            QDialogButtonBox.Cancel).clicked.connect(
            self.go_choosing_filter(0))

        self.go_home()

    def go_home(self):
        self.widget_home_menu.show()
        self.widget_level_editor_menu.hide()
        self.widget_choosing_filter_menu.hide()
        self.widget_choosing_game_feature_menu.hide()

    def go_level_editor_menu(self):
        self.ui_level_editor_menu.error_lb.setText(None)

        self.widget_home_menu.hide()
        self.widget_level_editor_menu.show()
        self.widget_choosing_filter_menu.hide()
        self.widget_choosing_game_feature_menu.hide()

        self.ui_level_editor_menu.savings_list.clear()

        maps_manager = MapsManager()
        cursor = maps_manager.get_cursor()
        map_names = [el[0] for el in maps_manager.get_names(cursor)]

        for map_name in map_names:
            self.ui_level_editor_menu.savings_list.addItem(map_name)

        def make_new_map():
            if self.ui_level_editor_menu.map_name_edit.text() in \
                    [el[0] for el in maps_manager.get_names(cursor)] or\
                    not any(self.ui_level_editor_menu.map_name_edit.text()):
                self.ui_level_editor_menu.error_lb.setText(
                    'Введите оргинальное название')
                return
            # обязательно изменить  при изменение доступных режимов
            game_types_boxes = [
                self.ui_level_editor_menu.game_type_classic_checkbox,
                self.ui_level_editor_menu.game_type_blindness_checkbox]
            game_types = [game_type.text() for game_type in game_types_boxes
                          if game_type.isChecked()]
            new_map_name = self.ui_level_editor_menu.map_name_edit.text()
            try:
                float(new_map_name)
                self.ui_level_editor_menu.error_lb.setText(
                    'В названия должна быть\nхотя бы одна буква')
            except ValueError:
                try:
                    maps_manager.add_map(new_map_name, (
                        self.ui_level_editor_menu.spin_size_lengh.value(),
                        self.ui_level_editor_menu.spin_size_width.value()),
                                         game_types)
                    LevelEditorUI(
                        self.ui_level_editor_menu.map_name_edit.text(), self)
                except sqlite3.OperationalError:
                    self.ui_level_editor_menu.error_lb.setText(
                        'Что-то пошло не так.')

        self.ui_level_editor_menu.make_new_map_btn.clicked.connect(
            make_new_map)

    def go_choosing_filter(self, widget_id):
        """widget_id=0 => Game
        widget_id=1 => Statistics"""

        def func():
            self.widget_home_menu.hide()
            self.widget_level_editor_menu.hide()
            self.widget_choosing_filter_menu.show()
            self.widget_choosing_game_feature_menu.hide()

            self.ui_choosing_filter_menu.error_lb.setText(None)

            try:
                self.ui_choosing_filter_menu.additional_btn.\
                    clicked.disconnect()
            except TypeError:
                pass

            if widget_id == 0:
                ok_method = self.ok_choosing_game

                maps_manager = MapsManager()
                cursor = maps_manager.get_cursor()
                map_names = [el[0] for el in maps_manager.get_names(cursor)]

                self.ui_choosing_filter_menu.additional_btn.setText(
                    'Cлучайная')
                self.ui_choosing_filter_menu.additional_btn.clicked.connect(
                    self.go_choosing_random_game_feature)
            else:
                ok_method = self.ok_choosing_statistics

                statistics_manager = StatisticsManager()
                map_names = statistics_manager.get_names()

                self.ui_choosing_filter_menu.additional_btn.setText('Удалить')
                self.ui_choosing_filter_menu.additional_btn.clicked.connect(
                    self.delete_statistic)

            self.ui_choosing_filter_menu.button_box.button(
                QDialogButtonBox.Ok).clicked.disconnect()
            self.ui_choosing_filter_menu.button_box.button(
                QDialogButtonBox.Ok).clicked.connect(ok_method)

            num_players_groups, game_type_groups = dict(), dict()
            for map_name in map_names:
                if widget_id == 0:
                    num_players = len(
                        maps_manager.get_all_player_ids(map_name, cursor))
                    if num_players < 1:
                        continue
                    for game_type in maps_manager.get_game_types(map_name):
                        game_type_groups[game_type] = game_type_groups.get(
                            game_type, []) + [map_name]
                else:
                    statistics_row = statistics_manager.get_by_name(map_name)
                    num_players = statistics_row['num_players']
                    game_types = statistics_row['game_type']
                    for game_type in game_types:
                        game_type_groups[game_type] = game_type_groups.get(
                            game_type, []) + [map_name]
                num_players_groups[num_players] = num_players_groups.get(
                    num_players, []) + [map_name]

            self.ui_choosing_filter_menu.num_players_combo.clear()
            self.ui_choosing_filter_menu.game_type_combo.clear()

            self.ui_choosing_filter_menu.num_players_combo.addItems(
                ['None'] + list(map(str, num_players_groups.keys())))
            self.ui_choosing_filter_menu.game_type_combo.addItems(
                ['None'] + list(sorted(game_type_groups.keys())))

            def onChoosingFilterChanged():
                saving_list = list()

                current_num_player = self.ui_choosing_filter_menu. \
                    num_players_combo.currentText()
                current_game_type = self.ui_choosing_filter_menu. \
                    game_type_combo.currentText()
                if not any(current_num_player) or not any(current_game_type):
                    return

                if current_num_player == 'None':
                    num_players_maps = [elem2 for elem1 in
                                        num_players_groups.values()
                                        for elem2 in elem1]
                else:
                    num_players_maps = num_players_groups[
                        int(current_num_player)]
                if current_game_type == 'None':
                    game_types_maps = [elem2 for elem1 in
                                       game_type_groups.values()
                                       for elem2 in elem1]
                else:
                    game_types_maps = game_type_groups[current_game_type]

                intersection = set(num_players_maps).intersection(
                    set(game_types_maps))
                for map_ in sorted(intersection,
                                   key=lambda x: (x if widget_id == 0 else int(
                                       x.split('.')[0]))):
                    if map_ not in saving_list:
                        saving_list.append(map_)

                self.ui_choosing_filter_menu.savings_list.clear()
                self.ui_choosing_filter_menu.savings_list.addItems(
                    saving_list)

            try:
                self.ui_choosing_filter_menu.game_type_combo. \
                    currentTextChanged.disconnect()
            except TypeError:
                pass
            try:
                self.ui_choosing_filter_menu.num_players_combo.\
                    currentTextChanged.disconnect()
            except TypeError:
                pass

            self.ui_choosing_filter_menu.game_type_combo. \
                currentTextChanged.connect(onChoosingFilterChanged)
            self.ui_choosing_filter_menu.num_players_combo. \
                currentTextChanged.connect(onChoosingFilterChanged)
            onChoosingFilterChanged()

        return func

    def go_choosing_random_game_feature(self):
        maps_name, savings_list = [], self.ui_choosing_filter_menu.savings_list
        for row in range(savings_list.count()):
            maps_name.append(savings_list.item(row).text())
        if not any(maps_name):
            self.ui_choosing_filter_menu.error_lb.setText(
                'Выберите что-нибудь')
            return
        self.go_choosing_game_feature(random.choice(maps_name))

    def go_choosing_game_feature(self, map_name):
        self.widget_home_menu.hide()
        self.widget_level_editor_menu.hide()
        self.widget_choosing_filter_menu.hide()
        self.widget_choosing_game_feature_menu.show()

        all_game_types_btns, all_player_layouts = [], []
        maps_manager = MapsManager()
        cursor = maps_manager.get_cursor()

        self.ui_choosing_game_feature_menu.error_lb.setText(None)

        def change_color(button):
            def func():
                color = QColorDialog.getColor()
                button.setStyleSheet(f'background-color: {color.name()}')
            return func

        wid_names, wid_types = QWidget(), QWidget()
        vbox_names, vbox_types = QVBoxLayout(), QVBoxLayout()
        wid_names.setLayout(vbox_names)
        wid_types.setLayout(vbox_types)

        player_ids = maps_manager.get_all_player_ids(map_name, cursor)
        for i in range(len(player_ids)):
            horizontal_layout = QHBoxLayout()
            horizontal_layout.setContentsMargins(5, 5, 5, 5)

            lb = QLabel(f'Игрок под id {player_ids[i]}: ', self)
            name = QLineEdit(self)
            btn_color = QPushButton('Цвет', self)
            btn_color.clicked.connect(change_color(btn_color))

            horizontal_layout.addWidget(lb)
            horizontal_layout.addWidget(name)
            horizontal_layout.addWidget(btn_color)

            all_player_layouts.append(horizontal_layout)
            vbox_names.addLayout(horizontal_layout)
        for game_type in maps_manager.get_game_types(map_name, cursor):
            btn = QRadioButton(game_type, self)
            btn.setStyleSheet('margin-left:100%;')

            all_game_types_btns.append(btn)
            vbox_types.addWidget(btn)
        self.ui_choosing_game_feature_menu.player_names_scroll.setWidget(
            wid_names)
        self.ui_choosing_game_feature_menu.game_types_scroll.setWidget(
            wid_types)

        def play_game():
            now_game_type = None
            error_lb = self.ui_choosing_game_feature_menu.error_lb
            for game_type_ind in range(len(all_game_types_btns)):
                if all_game_types_btns[game_type_ind].isChecked():
                    now_game_type = all_game_types_btns[game_type_ind].text()
                    break
                if game_type_ind + 1 == len(all_game_types_btns):
                    error_lb.setText('Выберите режим')
                    return
            all_players, all_names = [], []
            for j in range(len(all_player_layouts)):
                naming = all_player_layouts[j].itemAt(1).widget().text()
                color = all_player_layouts[j].itemAt(2).widget().palette(). \
                    button().color()
                color = f'{color.red()} {color.green()} {color.blue()}'
                if not any(naming):
                    error_lb.setText('Введите имена')
                    return
                all_players.append(Player(j, naming, color))
                all_names.append(naming)
            if any([all_names.count(naming) > 1 for naming in all_names]):
                error_lb.setText('Введите разные имена')
                return
            if self.ui_choosing_game_feature_menu.\
                    random_players_query_checkbox.isChecked():
                random.shuffle(all_players)
            map_info = MapInfo(map_name, now_game_type, len(all_players),
                               all_players)
            choose_game.load_game(map_info)

        self.ui_choosing_game_feature_menu.button_box.button(
            QDialogButtonBox.Ok).clicked.disconnect()
        self.ui_choosing_game_feature_menu.button_box.button(
            QDialogButtonBox.Ok).clicked.connect(play_game)

    def ok_choosing_game(self):
        cur_item = self.ui_choosing_filter_menu.savings_list.currentItem()
        if cur_item is None:
            self.ui_choosing_filter_menu.error_lb.setText(
                'Выберите что-нибудь')
            return
        self.go_choosing_game_feature(cur_item.text())

    def ok_choosing_statistics(self):
        cur_item = self.ui_choosing_filter_menu.savings_list.currentItem()
        if cur_item is None:
            self.ui_choosing_filter_menu.error_lb.setText(
                'Выберите что-нибудь')
            return
        cur_item = cur_item.text()
        StatisticsWindow(cur_item, self)

    def ok_level_editor(self):
        if self.ui_level_editor_menu.savings_list.currentItem() is None:
            self.ui_level_editor_menu.error_lb.setText('Выберите что-нибудь')
            return
        map_name = self.ui_level_editor_menu.savings_list.currentItem().text()
        LevelEditorUI(map_name, self)

    def delete_save_level_editor(self):
        if self.ui_level_editor_menu.savings_list.currentItem() is None:
            self.ui_level_editor_menu.error_lb.setText(
                'Выберите, что удалить')
            return

        maps_manager = MapsManager()
        db = maps_manager.get_db()
        cursor = maps_manager.get_cursor(db)
        maps_manager.delete_map(
            self.ui_level_editor_menu.savings_list.currentItem().text(),
            cursor)

        self.ui_level_editor_menu.savings_list.clear()
        map_names = [el[0] for el in maps_manager.get_names(cursor)]
        for map_name in map_names:
            self.ui_level_editor_menu.savings_list.addItem(map_name)

        db.commit()

    def delete_statistic(self):
        if self.ui_choosing_filter_menu.savings_list.currentItem() is None:
            self.ui_choosing_filter_menu.error_lb.setText(
                'Выберите, что удалить')
            return

        StatisticsManager().delete_statistics(
            int(self.ui_choosing_filter_menu.savings_list.currentItem().
                text().split('.')[0]))
        # для обновления статистик
        self.go_choosing_filter(1)()


class MainMenu:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainMenuWindow()

    def show(self):
        self.window.show()
        sys.exit(self.app.exec_())
