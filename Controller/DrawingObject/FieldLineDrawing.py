# Under MIT License, see LICENSE.txt

from PyQt5 import QtCore

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'

# Should probably have a class for color
BLUE_COLOR = (0, 0, 255)
YELLOW_COLOR = (255, 255, 0)

class FieldLineDrawing(BaseDrawingObject):
    def __init__(self):
        BaseDrawingObject.__init__(self)

    def draw(self, painter):
        if self.isVisible():
            # Dessine les lignes
            painter.setBrush(QtToolBox.create_brush(is_visible=False))

            painter.setPen(QtToolBox.create_pen(color=(255, 255, 255),
                                                style='SolidLine',
                                                width=QtToolBox.field_ctrl.line_width * QtToolBox.field_ctrl.ratio_screen))

            # Dessine tous les arcs
            for name, arc in QtToolBox.field_ctrl.field_arcs.items():
                #print(name, arc.thickness)
                self.drawArc(painter, arc.center, arc.radius, arc.start_angle, arc.end_angle)
            for name, line in QtToolBox.field_ctrl.field_lines.items():
                #print(name, line.thickness)
                self.drawLine(painter, line.p1, line.p2)

            # Dessine left goal
            painter.setPen(QtToolBox.create_pen(color=BLUE_COLOR,
                                                style='SolidLine',
                                                width=50 * QtToolBox.field_ctrl.ratio_screen))
            for name, line in QtToolBox.field_ctrl.field_goal_left.items():
                print(name, line.p1)
                self.drawLine(painter, line)

            # Dessine right goal
            painter.setPen(QtToolBox.create_pen(color=YELLOW_COLOR,
                                                style='SolidLine',
                                                width=50 * QtToolBox.field_ctrl.ratio_screen))
            for name, line in QtToolBox.field_ctrl.field_goal_right.items():
                self.drawLine(painter, line)

    def drawArc(self, painter,  arc):
        x, y, _  = QtToolBox.field_ctrl.convert_real_to_scene_pst(arc.center[0] - arc.radius,
                                                                  arc.center[1] + arc.radius)
        width = arc.radius * 2 * QtToolBox.field_ctrl.ratio_screen
        # Qt is weird and it require a rectangle to be defined to draw an arc
        rect = QtCore.QRect(x, y, width, width)
        # Angle are calculate in 1/16th of a degree
        painter.drawArc(rect,
                        int(arc.start_angle) * 16,
                        int(arc.end_angle - arc.start_angle) * 16)

    def drawLine(self, painter, line):
        x1, y1, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(line.p1[0], line.p1[1])
        x2, y2, _ = QtToolBox.field_ctrl.convert_real_to_scene_pst(line.p2[0], line.p2[1])

        painter.drawLine(x1, y1, x2, y2)

    @staticmethod
    def get_datain_associated():
        return 'field-lines'
