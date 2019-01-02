# Under MIT License, see LICENSE.txt

import argparse
import sys

# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import QApplication

from Controller.MainController import MainController
from Util.config import Config

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


if __name__ == '__main__':
    args = argument_parser()
    app = QApplication(sys.argv)

    config = Config(args.path_field_config, args.team_color)

    # todo pretty up when done
    f = MainController(config)  # args.team_color, int(config["vision_port"]), ui_cmd_sender_port, ui_cmd_receiver_port)
    # f.show()
    sys.exit(app.exec())
