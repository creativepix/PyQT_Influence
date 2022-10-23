import csv
import datetime as dt
import json

from ..constants import STATISTICS_FIELD_NAMES, STATISTICS_PATH, \
    STATISTICS_DATE_FORMAT


class StatisticsManager:
    @staticmethod
    def get_statistics():
        return csv.DictReader(open(STATISTICS_PATH, newline=''),
                              fieldnames=STATISTICS_FIELD_NAMES)

    def delete_statistics(self, id_statistics: int):
        rows = []
        with open(STATISTICS_PATH, 'r') as inp:
            for row in csv.reader(inp):
                rows.append(row)
        step_out = 0
        with open(STATISTICS_PATH, 'w') as out:
            writer = csv.writer(out)
            for row in rows:
                if not any(row):
                    continue
                if row[1] != str(id_statistics):
                    row[1] = str(int(row[1]) - step_out)
                    writer.writerow(row)
                else:
                    step_out += 1

    def get_by_name(self, name):
        statistics = self.get_statistics()
        for row in statistics:
            if row['save_id'] == name.split('.')[0]:
                row['date'] = dt.datetime.strptime(row['date'],
                                                   STATISTICS_DATE_FORMAT)
                row['num_players'] = int(row['num_players'])
                row['save_id'] = int(row['save_id'])
                row['game_type'] = list(filter(lambda x: any(x),
                                               row['game_type'].split(' ')))

                def keys_to_int(dicti: dict):
                    return dict((int(key), val) for key, val in dicti.items())

                row['player_names'] = keys_to_int(json.loads(
                    row['player_names'].replace("'", "\"")))
                row['player_colors'] = keys_to_int(json.loads(
                    row['player_colors'].replace("'", "\"")))
                row['statistics'] = keys_to_int(json.loads(
                    row['statistics'].replace("'", "\"")))

                return row
        return None

    def get_names(self):
        all_names = []
        statistics = self.get_statistics()
        for row in statistics:
            name = f'{row["save_id"]}. {row["date"]} {row["save_name"]}' \
                   f'_{row["game_type"]}_{row["num_players"]}'
            all_names.append(name)
        return all_names

    def save_statistics(self, map_info, statistics: dict):
        with open(STATISTICS_PATH, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=STATISTICS_FIELD_NAMES)

            date = dt.datetime.now().strftime(STATISTICS_DATE_FORMAT)
            save_id = sum([1 for _ in self.get_statistics()])
            player_names = dict()
            player_colors = dict()
            new_statistics = dict()
            for ind in range(len(map_info.all_players_query)):
                player_names[str(ind)] = map_info.all_players_query[ind].name
                player_colors[str(ind)] = map_info.all_players_query[ind].color
            for key, value in statistics.items():
                new_statistics[str(key.id)] = value
            writer.writerow({'date': date, 'save_id': save_id,
                             'save_name': map_info.map_name,
                             'game_type': map_info.game_type,
                             'num_players': map_info.player_nums,
                             'player_names': player_names,
                             'player_colors': player_colors,
                             'statistics': new_statistics})
