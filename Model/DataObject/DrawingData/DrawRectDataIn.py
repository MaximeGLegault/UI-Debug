# Under MIT License, see LICENSE.txt

from Model.DataObject.BaseDataObject import catch_format_error
from Model.DataObject.DrawingData.BaseDataDraw import BaseDataDraw

__author__ = 'RoboCupULaval'


class DrawRectDataIn(BaseDataDraw):
    def __init__(self, data_in):
        super().__init__(data_in)
        self._format_data()

    @catch_format_error
    def _check_obligatory_data(self):
        """ Vérifie les données obligatoires """
        assert isinstance(self.data, dict),\
            "data: {} n'est pas un dictionnaire.".format(type(self.data))
        keys = self.data.keys()

        assert 'top_left' in keys, \
            "data['top_left'] n'existe pas."
        assert self._point_is_valid(self.data['top_left']), \
            "data['top_left']: {} n'est pas un point valide.".format(self.data['top_left'])

        assert 'bottom_right' in keys, \
            "data['bottom_right'] n'existe pas."
        assert self._point_is_valid(self.data['bottom_right']), \
            "data['bottom_right']: {} n'est pas un point valide.".format(self.data['bottom_right'])

    @catch_format_error
    def _check_optional_data(self):
        """ Vérifie les données optionnelles """
        keys = self.data.keys()
        if 'color' in keys:
            assert self._colorRGB_is_valid(self.data['color']), \
                "data['color']: {} n'est pas une couleur valide.".format(self.data['color'])
        else:
            self.data['color'] = (0, 0, 0)

        if 'is_fill' in keys:
            assert isinstance(self.data['is_fill'], bool), \
                "data['is_fill']: {} n'est pas du bon type (bool)".format(type(self.data['is_fill']))
        else:
            self.data['is_fill'] = False

        if 'width' in keys:
            assert isinstance(self.data['width'], int), \
                "data['width']: {} n'est pas du bon type (int)".format(type(self.data['width']))
        else:
            self.data['width'] = 2

        if 'style' in keys:
            assert self.data['style'] in self.line_style_allowed, \
                "data['style']: {} n'est pas une style valide".format(self.data['style'])
        else:
            self.data['style'] = 'SolidLine'

        if 'timeout' in keys:
            assert self.data['timeout'] >= 0, \
                "data['timeout']: {} n'est pas valide.".format(self.data['timeout'])
        else:
            self.data['timeout'] = 0

    @staticmethod
    def get_default_data_dict():
        return dict(zip(["top_left", 'bottom_right'],
                        [(-250, -250), (0, -500)]))

    @staticmethod
    def get_type():
        return 3006
