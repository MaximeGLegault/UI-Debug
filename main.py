# Under MIT License, see LICENSE.txt

import argparse
import sys
from configparser import ParsingError, ConfigParser
from typing import Dict

# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import QApplication

from Controller.MainController import MainController

__author__ = 'RoboCupULaval'


def argument_parser() -> argparse.Namespace:
    """ Argument parser """
    parser = argparse.ArgumentParser(description='option pour initialiser le UI-debug')
    parser.add_argument('path_field_config', metavar='use_type', type=str, default='../StrategyIA/config/field/sim.cfg',
                        help='Path to the field config file in the StratetyIA config/field folder.')
    parser.add_argument('team_color', metavar='team_color', type=str, default='blue',
                        help='team_color, set the color to use for the ports')
    args_ = parser.parse_args()
    return args_


def load_config(path) -> Dict:
    config_parser = ConfigParser(allow_no_value=False)
    try:
        print("Loading", path, " port configuration file.")
        config_parser.read_file(open(path))
    except FileNotFoundError:
        raise RuntimeError("Impossible de lire le fichier de configuration.")
    except ParsingError:
        raise RuntimeError("Le fichier de configuration est mal configuré.\nExiting!")

    return {s: dict(config_parser.items(s)) for s in config_parser.sections()}["COMMUNICATION"]


if __name__ == '__main__':
    args = argument_parser()
    app = QApplication(sys.argv)

    config = load_config(args.path_field_config)

    # DO NOT TOUCH EVER THEY ARE HARDCODED BOTH IN THE IA AND IN UI-DEBUG
    if args.team_color == "blue":
        ui_cmd_sender_port = 14444  # DO NOT TOUCH
        ui_cmd_receiver_port = 15555  # DO NOT TOUCH
    else:
        ui_cmd_sender_port = 16666  # DO NOT TOUCH
        ui_cmd_receiver_port = 17777  # DO NOT TOUCH

    f = MainController(args.team_color, int(config["vision_port"]), ui_cmd_sender_port, ui_cmd_receiver_port)
    f.show()
    sys.exit(app.exec())
