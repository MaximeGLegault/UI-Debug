# Under MIT License, see LICENSE.txt

from math import cos
from math import sin

from Controller.MobileObject.BaseMobileObject import BaseMobileObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class RobotMob(BaseMobileObject):
    def __init__(self, bot_id, x=0, y=0, theta=0, is_yellow=True):
        BaseMobileObject.__init__(self, x, y, theta)
        self._id = bot_id
        self._is_yellow = is_yellow
        self._show_number = False
        self._show_vector = False
        self._vector = (0, 0)
        self._radius = 180 / 2

    def draw(self, painter):
        # TODO Ajouter vecteur de direction
        if self.isVisible():
            x, y, theta = QtToolBox.field_ctrl.convert_real_to_scene_pst(self._x, self._y, self._theta)
            if self._is_yellow:
                painter.setBrush(QtToolBox.create_brush(color=(255, 255, 100)))
            else:
                painter.setBrush(QtToolBox.create_brush(color=(100, 150, 255)))

            painter.setPen(QtToolBox.create_pen(color=(0, 0, 0),
                                                style='SolidLine',
                                                width=1))

            radius = self._radius * QtToolBox.field_ctrl.ratio_screen
            painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)
            painter.drawLine(x, y, x + cos(theta) * radius, y + sin(theta) * radius)

            if self._show_number:
                painter.drawText(x + radius, y + radius * 2, str(self._id))

    def show_number(self):
        self._show_number = True

    def hide_number(self):
        self._show_number = False

    def number_isVisible(self):
        return self._show_number

    @staticmethod
    def get_qt_item(drawing_data_in):
        return

    @staticmethod
    def get_datain_associated():
        return 'robot'
