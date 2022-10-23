import random
from enum import Enum
from ....scripts.gaming.base_game.main_ui import BaseMainUI
from ....scripts.all_builders import InfluenceGameBuilder, \
    HexagonBuilder, MainUIBuilder, StatisticsTabBuilder, GameTabBuilder
from ....scripts.gaming.map_info import MapInfo
from ....scripts.gaming.player import Player

ATTACK_WIN_PERCENTS = {-1: 25, 0: 50, 1: 75}


class PhasesEnum(Enum):
    ATTACK = 0
    REINFORCEMENT = 1


NO_ONE_PLAYER = Player(-1, 'None', '0 0 0')


class BaseInfluenceGame(InfluenceGameBuilder):
    def __init__(self, map_info: MapInfo):
        self.map_info = map_info
        self.map_info.setGameClass(self)

        self.phase = PhasesEnum.ATTACK
        self.reinforcement_points_left = 0
        self.now_player = self.map_info.all_players_query[0]
        self.is_ended = False
        self.attacking_hexagon: HexagonBuilder = None

        self.main_ui: MainUIBuilder = BaseMainUI(self.map_info)
        self.statistics_tab: StatisticsTabBuilder = self.main_ui.statistics_tab
        self.game_tab: GameTabBuilder = self.main_ui.game_tab

        self.__post_init__()

    def __post_init__(self):
        self.main_ui.show()
        self.update_now_player_txt()
        self.update_grid()

    def plus_one_clicked(self):
        self.main_ui.max_btn.setChecked(False)

    def max_clicked(self):
        self.main_ui.plus_one_btn.setChecked(False)

    def update_now_player_txt(self):
        txt = f'Ходит игрок {self.now_player.name}'
        self.main_ui.status_text.setText(txt)

    def skip(self):
        while self.reinforcement_points_left > 0:
            is_plused = False
            for hexagon_row in self.game_tab.hexagon_grid:
                for hexagon in hexagon_row:
                    if hexagon.owner != self.now_player or \
                            not hexagon.is_drawing or \
                            hexagon.max_points == hexagon.now_points:
                        continue
                    hexagon.now_points += 1
                    self.reinforcement_points_left -= 1
                    is_plused = True
                    if self.reinforcement_points_left <= 0:
                        break
                if self.reinforcement_points_left <= 0:
                    break
            if not is_plused:
                break
        self.update_grid()

    def get_num_reinforcement_points(self):
        all_reinforcement_points = 0
        for hexagon_row in self.game_tab.hexagon_grid:
            for hexagon in hexagon_row:
                if hexagon.owner == self.now_player:
                    all_reinforcement_points += 1
        return all_reinforcement_points

    def transition_phase(self):
        if self.phase == PhasesEnum.ATTACK:
            self.phase = PhasesEnum.REINFORCEMENT
            self.main_ui.attack_phase.setEnabled(False)
            self.main_ui.reinforcement_phase.setEnabled(True)
            self.main_ui.reinforcement_points.show()
            self.main_ui.reinforcement_points_label.show()

            self.main_ui.now_phase_lb.setText('Фаза укрепления')

            self.reinforcement_points_left = \
                self.get_num_reinforcement_points()
            self.main_ui.reinforcement_points.setText(
                str(self.reinforcement_points_left))
        else:
            self.phase = PhasesEnum.ATTACK
            self.main_ui.attack_phase.setEnabled(True)
            self.main_ui.reinforcement_phase.setEnabled(False)
            self.main_ui.reinforcement_points.hide()
            self.main_ui.reinforcement_points_label.hide()
            self.skip()

            self.main_ui.now_phase_lb.setText('Фаза атаки')

            any_ = False
            while not any_:
                ind = self.map_info.all_players_query.index(
                    self.now_player) + 1
                try:
                    self.now_player = self.map_info.all_players_query[ind]
                except IndexError:
                    self.now_player = self.map_info.all_players_query[0]
                for row in self.game_tab.hexagon_grid:
                    for hexagon in row:
                        if hexagon.owner == self.now_player:
                            any_ = True
                            break
            self.update_now_player_txt()

        self.main_ui.plus_one_btn.setChecked(False)
        self.main_ui.max_btn.setChecked(False)

        if self.attacking_hexagon is not None:
            self.attacking_hexagon.is_selected = False
        self.attacking_hexagon = None

        self.main_ui.statistics_tab.update_statistics()

    def attack_hexagon(self, attacked_hexagon):
        def won_attack():
            attacked_hexagon.now_points = max(1, points_difference)
            attacked_hexagon.color = self.attacking_hexagon.color
            attacked_hexagon.owner = self.attacking_hexagon.owner
            if attacked_hexagon.max_points < attacked_hexagon.now_points:
                self.attacking_hexagon.now_points = \
                    attacked_hexagon.now_points - \
                    attacked_hexagon.max_points + 1
                attacked_hexagon.now_points = attacked_hexagon.max_points
            else:
                self.attacking_hexagon.now_points = 1
            self.attacking_hexagon = attacked_hexagon

        def lost_attack():
            self.attacking_hexagon.now_points = 1
            # перед points_difference стоит минус, так как изначально
            # points_difference = атакующая - атакованная, а здесь нужно
            # наоборот
            attacked_hexagon.now_points = max(1, -points_difference)

        points_difference = (self.attacking_hexagon.now_points -
                             attacked_hexagon.now_points)
        if attacked_hexagon.now_points == 0:
            points_difference = self.attacking_hexagon.now_points - 1
            won_attack()
        elif points_difference in list(ATTACK_WIN_PERCENTS.keys()):
            win_percent = ATTACK_WIN_PERCENTS[points_difference]
            is_won_attacked = random.randrange(0, 100) < win_percent
            if is_won_attacked:
                won_attack()
            else:
                lost_attack()
        elif points_difference < 0:
            lost_attack()
        else:
            won_attack()

        attacked_hexagon.update_points()
        self.attacking_hexagon.update_points()

        if self.attacking_hexagon.now_points == 1:
            self.attacking_hexagon = None
        else:
            self.attacking_hexagon.is_selected = True

    def selected_hexagon(self, hexagon):
        if self.is_ended:
            return
        if self.phase == PhasesEnum.ATTACK:
            if hexagon.owner == self.now_player:
                if hexagon.now_points < 2:
                    return
                if self.attacking_hexagon is not None:
                    self.attacking_hexagon.is_selected = False
                self.attacking_hexagon = hexagon
                self.attacking_hexagon.is_selected = True
            else:
                if self.attacking_hexagon is None:
                    return
                self.attacking_hexagon.is_selected = False

                def is_connecting_lines():
                    lines = self.attacking_hexagon.lines.split(' ')

                    def any_left_right(inds: list, coof1, coof2):
                        if hexagon.x + 1 * coof1 == self.attacking_hexagon.x:
                            return lines[inds[0]] == '1'
                        elif hexagon.x - 1 * coof2 == self.attacking_hexagon.x:
                            return lines[inds[1]] == '1'
                        return False

                    if hexagon.y == self.attacking_hexagon.y:
                        return any_left_right([2, 3], 1, 1)
                    elif hexagon.y + 1 == self.attacking_hexagon.y:
                        left_right = [0, 1]
                    elif hexagon.y - 1 == self.attacking_hexagon.y:
                        left_right = [4, 5]
                    else:
                        return False
                    if self.attacking_hexagon.y % 2 == 0:
                        return any_left_right(left_right, 1, 0)
                    return any_left_right(left_right, 0, 1)

                if not is_connecting_lines():
                    self.attacking_hexagon = None
                    return

                self.attack_hexagon(hexagon)
        else:
            if hexagon.owner != self.now_player:
                return

            difference_points = hexagon.max_points - hexagon.now_points

            if self.main_ui.plus_one_btn.isChecked():
                plus = min(1, difference_points)
            elif self.main_ui.max_btn.isChecked():
                plus = min(self.reinforcement_points_left, difference_points)
            else:
                plus = 0

            if self.reinforcement_points_left - plus < 0:
                return
            hexagon.now_points += plus
            self.reinforcement_points_left -= plus
            self.main_ui.reinforcement_points.setText(
                str(self.reinforcement_points_left))
        self.update_grid()

    def update_grid(self):
        player_hexagons = 0
        all_hexagons = 0
        for hexagon_row in self.game_tab.hexagon_grid:
            for hexagon in hexagon_row:
                if hexagon.is_exist:
                    hexagon.repaint_hexagon()
                    all_hexagons += 1
                    if hexagon.owner is not None:
                        player_hexagons += 1
        self.main_ui.progress_bar.setMaximum(all_hexagons)
        self.main_ui.progress_bar.setValue(player_hexagons)

        is_win = self.is_win()
        if isinstance(is_win, Player):
            self.end_game(is_win)

    def is_win(self):
        all_players = []
        for hexagon_row in self.game_tab.hexagon_grid:
            for hexagon in hexagon_row:
                if hexagon.owner is not None and \
                        hexagon.owner not in all_players:
                    all_players.append(hexagon.owner)
        if len(all_players) == 1:
            for player_query in self.map_info.all_players_query:
                if player_query == all_players[0]:
                    return player_query
            return NO_ONE_PLAYER
        elif len(all_players) == 0:
            return NO_ONE_PLAYER
        return False

    def end_game(self, winner):
        self.is_ended = True
        if self.attacking_hexagon is not None:
            self.attacking_hexagon.is_selected = False
        self.attacking_hexagon = None
        self.game_tab.end_game(winner)
        self.main_ui.statistics_tab.update_statistics()
        self.statistics_tab.save_statistics()
