from ....scripts.all_builders import MainUIBuilder
from ....scripts.gaming.base_game.game_tab import BaseGameTab
from ....scripts.gaming.blindness_game.hexagon_grid_widget import \
    BlindnessHexagonGridWidget
from ....scripts.gaming.map_info import MapInfo


class BlindnessGameTab(BaseGameTab):
    def __init__(self, main_ui: MainUIBuilder, map_info: MapInfo):
        super().__init__(main_ui, map_info)
        self.widget_hexagon_grid.setParent(None)

        self.widget_hexagon_grid = BlindnessHexagonGridWidget(
            self.main_ui.centralwidget)
        self.widget_hexagon_grid.setObjectName("widget_hexagon_grid")

        super().__post_init__()

    def __post_init__(self):
        pass
