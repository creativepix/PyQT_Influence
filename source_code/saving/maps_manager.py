import json
import sqlite3
from sqlite3 import Cursor
from ..constants import MAPS_PATH, GAME_TYPE_IDS


def set_default_values(cursor_ind=None):
    def new_set_default_values(func):
        def new_func(*args, **kwargs):
            new_args = list(args)
            if cursor_ind is not None:
                if cursor_ind >= len(new_args):
                    new_args += [MapsManager().get_cursor()]
            return func(*new_args, **kwargs)
        return new_func
    return new_set_default_values


class MapsManager:
    @staticmethod
    def get_db():
        return sqlite3.connect(MAPS_PATH)

    def get_cursor(self, db=None):
        if db is None:
            db = self.get_db()
        return db.cursor()

    @set_default_values(3)
    def set_game_types(self, map_name, new_game_types, cursor: Cursor = None):
        new_game_type_ids = ' '.join([str(key)
                                      for key, value in GAME_TYPE_IDS.items()
                                      if value in new_game_types])
        cursor.execute(f"UPDATE MAPS_INFO SET GAME_TYPE_IDS="
                       f"'{new_game_type_ids}' WHERE MAP_NAME='{map_name}'")

    @set_default_values(3)
    def set_hexagons(self, map_name, hexagons, cursor: Cursor = None):
        hex_jsons = []
        for row in hexagons:
            hex_jsons.append([])
            for hexagon in row:
                owner = "null" if \
                    hexagon.owner_id is None else hexagon.owner_id
                hex_json = '{'\
                           f'"is_drawing": {int(hexagon.is_drawing)},'\
                           f'"is_exist": {int(hexagon.is_exist)},'\
                           f'"lines": "{hexagon.lines}",'\
                           f'"max_points": {hexagon.max_points},'\
                           f'"now_points": {hexagon.now_points},'\
                           f'"owner": {owner}'\
                           '}'
                hex_jsons[-1].append(hex_json)
        question_marks = ("?," * self.get_size(map_name, cursor)[1]).strip(",")
        cursor.execute(f"DELETE FROM {map_name}")
        cursor.executemany(f'INSERT INTO {map_name} VALUES ({question_marks})',
                           hex_jsons)

    @set_default_values(2)
    def delete_map(self, map_name, cursor: Cursor = None):
        cursor.execute(f'DELETE FROM MAPS_INFO WHERE MAP_NAME="{map_name}"')
        cursor.execute(f'DROP TABLE {map_name}')

    @set_default_values(3)
    def rename_map(self, now_name, new_name, cursor: Cursor = None):
        cursor.execute(f'ALTER TABLE {now_name} RENAME TO {new_name};')
        cursor.execute(f"UPDATE MAPS_INFO SET MAP_NAME='{new_name}' "
                       f"WHERE MAP_NAME='{now_name}'")

    # @set_default_values()
    def add_map(self, map_name, size, game_types):
        """size = (lengh, width)"""
        db = self.get_db()
        cursor = db.cursor()

        cols = ','.join([f'COL{i + 1} TEXT NOT NULL'
                         for i in range(size[1])])
        script = f'CREATE TABLE {map_name} ({cols});'
        game_type_ids = ' '.join(
            [str(key) for key, value in GAME_TYPE_IDS.items()
             if value in game_types])

        cursor.execute(script)
        cursor.execute(f"INSERT INTO MAPS_INFO VALUES (?,?)",
                       (map_name, game_type_ids))
        base_hex_json = '''{
    "is_drawing": 1,
    "is_exist": true,
    "lines": "1 1 1 1 1 1",
    "max_points": 8,
    "now_points": 0,
    "owner": null
}'''
        question_marks = ("?," * size[1]).strip(",")
        cursor.executemany(f'INSERT INTO {map_name} VALUES ({question_marks})',
                           [[base_hex_json] * size[1]] * size[0])
        db.commit()

    @set_default_values(2)
    def get_all_rows(self, map_name: str, cursor: Cursor = None):
        return cursor.execute(f'SELECT * FROM {map_name}').fetchall()

    @set_default_values(1)
    def get_names(self, cursor: Cursor = None):
        names = cursor.execute(
            'SELECT name FROM sqlite_master WHERE type="table";').fetchall()
        return list(filter(lambda x: x[0] != 'MAPS_INFO', names))

    @set_default_values(2)
    def get_all_player_ids(self, map_name: str, cursor: Cursor = None):
        all_rows = self.get_all_rows(map_name, cursor)
        all_players = set()

        for row in all_rows:
            for cell in row:
                cell_json = json.loads(cell)
                if cell_json['owner'] is not None:
                    all_players.add(cell_json['owner'])
        return sorted(list(all_players))

    @set_default_values(2)
    def get_size(self, map_name: str, cursor: Cursor = None):
        """returning (width, height)"""
        all_rows = self.get_all_rows(map_name, cursor)
        return len(all_rows), 0 if len(all_rows) == 0 else len(all_rows[0])

    @set_default_values(2)
    def get_game_types(self, map_name: str, cursor: Cursor = None):
        executing = f'SELECT GAME_TYPE_IDS FROM MAPS_INFO ' \
                    f'WHERE MAP_NAME="{map_name}"'
        return [GAME_TYPE_IDS[int(type_id)] for type_id in
                cursor.execute(executing).fetchall()[0][0].split(' ')
                if any(type_id)]
