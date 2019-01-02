# Under MIT License, see LICENSE.txt

from Controller.DrawingObject.BaseDrawingObject import BaseDrawingObject
from Controller.MobileObject.BaseMobileObject import BaseMobileObject

__author__ = 'RoboCupULaval'


class DrawingObjectFactory:
    def __init__(self, controller):
        self._controller = controller
        self._name = DrawingObjectFactory.__name__
        self._catalog_from_datain_class_to_qt_object = dict()
        self._init_object_catalog()

    def _init_object_catalog(self):
        """ Initialise le catalogue d'objet pour la factory """
        self._import_data_in_classes()
        for subclass in BaseDrawingObject.__subclasses__() + BaseMobileObject.__subclasses__():
            self._catalog_from_datain_class_to_qt_object[subclass.get_datain_associated()] = subclass

    def _import_data_in_classes(self):
        """ Importe les objets dans les sous-dossiers de Model.DataObject """
        from os import listdir
        from os.path import isfile, join, isdir
        from importlib.machinery import SourceFileLoader

        path_current_dir = __file__.replace(DrawingObjectFactory.__name__ + '.py', '')
        folders_inside_current_dir = [f for f in listdir(path_current_dir)
                                      if isdir(join(path_current_dir, f)) and f.count('_') == 0]
        for folder in folders_inside_current_dir:
            files = [f for f in listdir(join(path_current_dir, folder))
                     if isfile(join(path_current_dir, folder, f)) and f.count('_') == 0]
            for file in files:
                SourceFileLoader("", join(path_current_dir, folder, file)).load_module()

    def get_qt_draw_object(self, data_draw):
        """ Génère un DataObject en fonction data_draw paquet reçu """
        try:
            return self._catalog_from_datain_class_to_qt_object[type(data_draw).__name__](data_draw)
        except Exception as e:
            msg = "Problème lors de la création de l'objet Qt avec " + str(e)
            self._controller.add_logging_message(self._name, msg, level=3)

    def get_specific_draw_object(self, index):
        try:
            return self._catalog_from_datain_class_to_qt_object[index]
        except Exception as e:
            msg = "Problème lors de la création de l'objet Qt avec " + str(e)
            self._controller.add_logging_message(self._name, msg, level=3)
