from abc import abstractmethod
from typing import Union
from PyQt5 import QtGui
from ..scripts.gaming.player import Player


class HexagonBuilder(object):
    @abstractmethod
    def update_geometry(self) -> None:
        pass

    @abstractmethod
    def update_points(self) -> None:
        pass

    @abstractmethod
    def zoom(self, zoom_percent: float) -> None:
        pass

    @abstractmethod
    def repaint_hexagon(self) -> None:
        pass

    @abstractmethod
    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        pass

    @abstractmethod
    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        pass

    @abstractmethod
    def _update_pixmap(self) -> None:
        pass


class HexagonGridWidgetBuilder(object):
    @abstractmethod
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        pass


class InfluenceGameBuilder(object):
    @abstractmethod
    def plus_one_clicked(self) -> None:
        pass

    @abstractmethod
    def max_clicked(self) -> None:
        pass

    @abstractmethod
    def update_now_player_txt(self) -> None:
        pass

    @abstractmethod
    def skip(self) -> None:
        pass

    @abstractmethod
    def get_num_reinforcement_points(self) -> int:
        pass

    @abstractmethod
    def transition_phase(self) -> None:
        pass

    @abstractmethod
    def attack_hexagon(self, attacked_hexagon: HexagonBuilder) -> None:
        pass

    @abstractmethod
    def selected_hexagon(self, hexagon: HexagonBuilder) -> None:
        pass

    @abstractmethod
    def update_grid(self) -> None:
        pass

    @abstractmethod
    def is_win(self) -> Union[bool, Player]:
        pass

    @abstractmethod
    def end_game(self, winner: Player) -> None:
        pass


class MainUIBuilder(object):
    @abstractmethod
    def change_active_tab(self, index: int) -> None:
        pass

    @abstractmethod
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass

    @abstractmethod
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass

    @abstractmethod
    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        pass

    @abstractmethod
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        pass


class GameTabBuilder(object):
    @abstractmethod
    def hide_grid(self) -> None:
        pass

    @abstractmethod
    def show_grid(self) -> None:
        pass

    @abstractmethod
    def resize(self) -> None:
        pass

    @abstractmethod
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass

    @abstractmethod
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass

    @abstractmethod
    def wheelEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass

    @abstractmethod
    def end_game(self, winner: Player) -> None:
        pass

    @abstractmethod
    def _init_make_map(self) -> None:
        pass


class StatisticsTabBuilder(object):
    @abstractmethod
    def update_statistics(self) -> None:
        pass

    @abstractmethod
    def resize(self) -> None:
        pass

    @abstractmethod
    def save_statistics(self) -> None:
        pass

