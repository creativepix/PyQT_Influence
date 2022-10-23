from PyQt5.Qt import Qt
from PIL import Image, ImageQt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QPushButton


BASE_HEXAGON_SIZE = 64


class LevelEditorHexagon(QPushButton):
    def __init__(self, widget, x, y, json_info, camera_delta_x=0,
                 camera_delta_y=0, zoom_percent=100):

        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError

        self.x = x
        self.y = y
        self.zoom_percent = zoom_percent
        self.camera_x = camera_delta_x
        self.camera_y = camera_delta_y
        self.lines = json_info['lines']
        self.max_points = json_info['max_points']
        self.now_points = json_info['now_points']
        self.owner_id = json_info['owner']

        self.hexagon_pixmap = QPixmap(":/gaming/images/gaming/hexagon.png")
        self.now_pixmap = self.hexagon_pixmap

        self.widget = widget
        super().__init__(self.widget)
        self.setStyleSheet('background-color: transparent')

        self.info_lb = QtWidgets.QLabel()
        self.info_lb.setContentsMargins(0, 0, 0, 0)
        self.info_lb.setStyleSheet('color: white')
        self.info_lb.setAlignment(Qt.AlignCenter)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.info_lb, alignment=QtCore.Qt.AlignCenter)

        self.__is_exist = json_info['is_exist']
        self.is_drawing = json_info['is_drawing']
        self.__is_selected = False

        self.repaint_hexagon()
        self.__update_pixmap()

        if not self.is_drawing or not self.is_exist:
            self.hide()

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

    def update_info(self):
        font_size = int(4 * self.zoom_percent / 100 + 1)
        self.info_lb.setText(f'Max: {self.max_points}\nNow: '
                             f'{self.now_points}\nOwner_id:\n{self.owner_id}')
        self.info_lb.setFont(QFont('MS Shell Dlg 2', font_size))

    def zoom(self, zoom_percent):
        self.zoom_percent = zoom_percent
        self.repaint_hexagon()

    def hide(self):
        self.info_lb.setText(None)
        self.setIcon(QIcon())

    def repaint_hexagon(self):
        self.update_geometry()
        if not self.is_drawing:
            self.hide()
            return
        self.update_info()

    def mouseMoveEvent(self, e):
        self.widget.mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        self.widget.mouseReleaseEvent(e)
        self.widget.parent.hexagon_select(self)

    def __update_pixmap(self):
        img = Image.fromqpixmap(self.hexagon_pixmap)
        data = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if data[x, y][:3] == (255, 255, 255) and not self.is_selected:
                    data[x, y] = (0, 0, 0, 0)
        self.now_pixmap = QPixmap.fromImage(ImageQt.ImageQt(img))

        icon = QIcon()
        icon.addPixmap(self.now_pixmap, QIcon.Normal, QIcon.Off)
        self.setIcon(icon)

    @property
    def is_exist(self):
        return self.__is_exist

    @is_exist.setter
    def is_exist(self, var):
        self.__is_exist = var
        self.repaint_hexagon()
        self.__update_pixmap()

    @property
    def is_selected(self):
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, var):
        self.__is_selected = var
        self.__update_pixmap()

    @property
    def is_drawing(self) -> bool:
        return self.__is_drawing

    @is_drawing.setter
    def is_drawing(self, var: bool):
        self.__is_drawing = var
        if not self.__is_drawing:
            self.hide()
