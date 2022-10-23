from PIL import Image, ImageQt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QFont
from ....scripts.gaming.map_info import MapInfo
from ....scripts.all_builders import HexagonBuilder
from ....scripts.gaming.player import Player


# гескагоны в квадратах -> их размер size * size
BASE_HEXAGON_SIZE = 64
NULL_COLOR = '100 100 0'


class BaseHexagon(QPushButton, HexagonBuilder):
    def __init__(self, map_info: MapInfo, widget: QWidget,
                 x: float, y: float, json_info: dict, camera_delta_x=0,
                 camera_delta_y=0, zoom_percent=100):

        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError
        super().__init__(widget)

        self.map_info = map_info
        self.x = x
        self.y = y
        self.zoom_percent = zoom_percent
        self.camera_x = camera_delta_x
        self.camera_y = camera_delta_y
        self.lines: str = json_info['lines']
        self.max_points: int = json_info['max_points']
        self.now_points: int = json_info['now_points']
        owner_id = json_info['owner']
        self.is_exist: bool = json_info['is_exist']
        self.hexagon_pixmap = QPixmap(":/gaming/images/gaming/hexagon.png")
        self.now_pixmap = self.hexagon_pixmap

        self.__is_selected = False
        if owner_id is not None:
            self.__owner = self.map_info.all_players_query[owner_id]
            self.color = self.owner.color
        else:
            self.__owner = None
            self.color = NULL_COLOR
        self.__is_drawing: bool = json_info['is_drawing']
        self.is_drawing = self.__is_drawing

        self.setStyleSheet('background-color: transparent')

        self.points_lb = QtWidgets.QLabel()
        self.points_lb.setContentsMargins(0, 0, 0, 0)
        self.points_lb.setStyleSheet('color: white')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.points_lb, alignment=QtCore.Qt.AlignCenter)

        self.__post_init__()

    def __post_init__(self):
        self.repaint_hexagon()
        self._update_pixmap()

    def update_geometry(self):
        size = int(BASE_HEXAGON_SIZE * self.zoom_percent / 100)
        local_x = (2 * self.x * BASE_HEXAGON_SIZE)
        local_y = (50 * BASE_HEXAGON_SIZE * self.y / 32)

        if self.y % 2 == 0:
            x = int(self.camera_x + local_x * self.zoom_percent / 100)
        else:
            x = int(size + self.camera_x + local_x * self.zoom_percent / 100)
        # 50 - это базовый промежуток по Y между первым и вторым
        # рядом гексагонов с размером 32 * 32
        y = int(self.camera_y + local_y * self.zoom_percent / 100)

        self.setGeometry(QtCore.QRect(x, y, size, size))
        self.setIconSize(QtCore.QSize(size, size))

    def update_points(self):
        font_size = int(10 * self.zoom_percent / 100 + 1)
        self.points_lb.setText(f'{self.now_points}/{self.max_points}')
        self.points_lb.setFont(QFont('MS Shell Dlg 2', font_size))

    def zoom(self, zoom_percent):
        self.zoom_percent = zoom_percent
        self.repaint_hexagon()

    def repaint_hexagon(self):
        self.update_points()
        self.update_geometry()

    def mouseMoveEvent(self, e):
        self.map_info.game_class.game_tab.mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        self.map_info.game_class.game_tab.mouseReleaseEvent(e)
        self.map_info.game_class.selected_hexagon(self)

    def _update_pixmap(self):
        rgb = list(map(int, self.color.split(' ')))

        img = Image.fromqpixmap(self.hexagon_pixmap)
        data = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if data[x, y][:3] == (255, 255, 255) and not self.is_selected:
                    data[x, y] = (0, 0, 0, 0)
                elif data[x, y] == (84, 84, 84, 255):
                    data[x, y] = (rgb[0], rgb[1], rgb[2], 255)
        self.now_pixmap = QPixmap.fromImage(ImageQt.ImageQt(img))

        icon = QIcon()
        icon.addPixmap(self.now_pixmap, QIcon.Normal, QIcon.Off)
        self.setIcon(icon)

    @property
    def owner(self) -> Player:
        return self.__owner

    @owner.setter
    def owner(self, var: Player):
        self.__owner = var
        self._update_pixmap()

    @property
    def is_selected(self) -> bool:
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, var: bool):
        self.__is_selected = var
        self._update_pixmap()

    @property
    def is_drawing(self) -> bool:
        return self.__is_drawing

    @is_drawing.setter
    def is_drawing(self, var: bool):
        self.__is_drawing = var
        if var and self.isHidden():
            self.show()
        elif not var and not self.isHidden():
            self.hide()
