# Under MIT License, see LICENSE.txt
from configparser import ConfigParser, ParsingError
from typing import Union

__author__ = "RobocupULaval"


class Config:
    def __init__(self, path: str, team_color=None):
        self._config = Config.default_config()
        self.load_config(path)
        self._adjust_ports_by_team_color(team_color)

    def load_config(self, path: str):
        config_parser = ConfigParser(allow_no_value=False)
        try:
            print("Loading", path, " port configuration file.")
            config_parser.read_file(open(path))
        except FileNotFoundError:
            raise RuntimeError("Impossible de lire le fichier de configuration.")
        except ParsingError:
            raise RuntimeError("Le fichier de configuration est mal configuré.\nExiting!")

        dict_update = {s: dict(config_parser.items(s)) for s in config_parser.sections()}

        # todo do better?
        if len(dict_update.keys()) != 1 or list(dict_update.keys())[0] != 'COMMUNICATION':
            raise RuntimeError("Le fichier de configuration ne devrait avoir qu'un champ nommé COMMUNICATION")

        self._config['COMMUNICATION'].update(dict_update['COMMUNICATION'])

    def _adjust_ports_by_team_color(self, team_color: Union[str, None]):
        if team_color is None:
            return

        # Has already blue teamcolor/ports by default
        if self['COACH']['team_color'] == 'yellow':
            self['COACH']['team_color'] = 'yellow'
            self['COACH']['ui_cmd_sender_port'] = self['COACH']['yellow_team_sender_port']
            self['COACH']['ui_cmd_receiver_port'] = self['COACH']['yellow_team_receiver_port']

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, key, value):
        self._config[key] = value

    @staticmethod
    def default_config():
        return {
            'COMMUNICATION': {
                'type': 'grsim',
                'vision_address': '224.5.23.2',
                'vision_port': 10227,
                'referee_address': '224.5.23.1',
                'referee_port': 10023,
                'ui_cmd_sender_port': 14444,
                'ui_cmd_receiver_port': 15555,
                # DO NOT TOUCH EVER THEY ARE HARDCODED BOTH IN THE IA AND IN UI-DEBUG
                'blue_team_sender_port': 14444,
                'blue_team_receiver_port': 15555,
                'yellow_team_sender_port': 16666,
                'yellow_team_receiver_port': 17777,
            },
            'COACH': {
                'default_color': 'blue',
                'team_color': 'blue',
            }
        }
