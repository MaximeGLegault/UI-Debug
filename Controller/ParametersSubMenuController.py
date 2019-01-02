# Under MIT License, see LICENSE.txt
from Controller import FieldController

__author__ = 'RobocupULaval'

from typing import Dict

import Controller
from Model.DataOutModel import DataOutModel


class ParametersSubMenuController:
    def __init__(self, main_controller: Controller, field_controller: FieldController, model_dataout: DataOutModel,
                 communication_config: Dict):
        self._main_controller = main_controller
        self._field_controller = field_controller
        self._model_dataout = model_dataout
        self._communication_config = communication_config
        self._default_vision_ip_address = self._communication_config['vision_address']
        self._default_vision_port = self._communication_config['vision_port']

    def send_udp_config(self):
        udp_config_info = dict(zip(['ip', 'port'],
                                   [self._communication_config['vision_address'],
                                    self._communication_config['vision_port']]))
        self._model_dataout.send_udp_config(udp_config_info)

    @property
    def default_vision_ip_address(self):
        return self._default_vision_ip_address

    @default_vision_ip_address.setter
    def default_vision_ip_address(self, value):
        # todo plug in call to something so we can really update
        self._communication_config['vision_address'] = value

    @property
    def default_vision_port(self):
        return self._default_vision_port

    @default_vision_port.setter
    def default_vision_port(self, value):
        # todo plug in call to something so we can really update
        self._communication_config['vision_port'] = value
