# Under MIT License, see LICENSE.txt

from signal import signal, SIGINT

from PyQt5.QtCore import Qt

from Communication.GrSimReplacementSender import GrSimReplacementSender
from Communication.UDPServer import UDPServer
from Communication.vision import Vision
from Controller.FieldController import FieldController
from Controller.ParametersSubMenuController import ParametersSubMenuController
from Model.DataInModel import DataInModel
from Model.DataOutModel import DataOutModel
from Model.FrameModel import FrameModel
from Model.RecorderModel import RecorderModel
from Util.config import Config
from View.MainView import MainView
from View.StrategyCtrView import StrategyCtrView
from .DrawingObjectFactory import DrawingObjectFactory
from .QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


# todo see if we can remove some noinspection in this file
# noinspection PyArgumentList
class MainController:
    # TODO: Dissocier Controller de la fenêtre principale
    def __init__(self, config: Config):
        self.config = config
        self.team_color = config['COACH']['team_color']
        # todo remove unecessary declaration of a config?

        # Création des Contrôleurs
        self.draw_handler = DrawingObjectFactory(self)

        # Communication
        self.network_data_in = UDPServer(name='UDPServer',
                                         debug=False,
                                         rcv_port=int(self.config['COMMUNICATION']['ui_cmd_sender_port']),
                                         snd_port=int(self.config['COMMUNICATION']['ui_cmd_receiver_port']))
        self.network_vision = Vision(port=int(config['COMMUNICATION']['vision_port']))
        self.ai_server_is_serial = False

        self.grsim_sender = GrSimReplacementSender()

        # Création des Modèles
        self.model_frame = FrameModel(self)
        self.model_datain = DataInModel(self)
        self.model_dataout = DataOutModel(self)
        self.model_recorder = RecorderModel()

        # Création des sous-controllers
        self.field_controller = FieldController()
        self.parameters_submenu_controller = ParametersSubMenuController(self, self.field_controller,
                                                                         self.model_dataout,
                                                                         self.config['COMMUNICATION'])

        # Création des Vues
        self.main_view = MainView(self)
        self.view_field_screen = self.main_view.gamefield_view
        # self.view_logger = LoggerView(self.main_view, self)
        # self.view_field_screen = FieldView(self.main_view, self)
        # self.view_filter = FilterCtrlView(self)
        # self.view_param = ParametersSubMenuView(self.main_view, self, self.parameters_submenu_controller)
        self.view_controller = StrategyCtrView(self.main_view, self)
        # self.view_media = MediaControllerView(self)
        # self.view_status = StatusBarView(self.main_view, self)
        # self.view_robot_state = GameStateView(self.main_view, self)
        # self.view_plotter = PlotterView(self.main_view, self)

        # Initialisation des UI
        self.init_signals()

        self.main_view.show()

        # Positions enregistrées des robots
        self.teams_formation = []

        # Initialisation des modèles aux vues
        # self.view_logger.set_model(self.model_datain)
        # self.view_plotter.set_model(self.model_datain)
        self.model_datain.setup_udp_server(self.network_data_in)
        self.model_dataout.setup_udp_server(self.network_data_in)
        self.model_frame.set_vision(self.network_vision)
        self.model_frame.start()
        self.model_frame.set_recorder(self.model_recorder)
        self.model_datain.set_recorder(self.model_recorder)

    def init_signals(self):
        # noinspection PyTypeChecker
        signal(SIGINT, self.signal_handle)

    def update_logging(self):
        self.view_logger.refresh()

    def save_logging(self, path, texte):
        self.model_datain.write_logging_file(path, texte)

    # noinspection PyUnusedLocal
    def signal_handle(self, *args):
        """ Responsable du traitement des signaux """
        self.main_view.close()

    def resize_window(self):
        # self.setFixedSize(self.minimumSizeHint())
        pass

    def add_draw_on_screen(self, draw):
        """ Ajout un dessin sur la fenêtre du terrain """
        # noinspection PyPep8,PyBroadException
        try:
            qt_draw = self.draw_handler.get_qt_draw_object(draw)
            if qt_draw is not None:
                self.view_field_screen.load_draw(qt_draw)
        except Exception:
            # todo get rid of this too broad exception
            pass

    def set_ball_pos_on_screen(self, x, y):
        """ Modifie la position de la balle sur le terrain """
        self.view_field_screen.set_ball_pos(x, y)

    def set_robot_pos_on_screen(self, bot_id, team_color, pst, theta):
        """ Modifie la position et l'orientation d'un robot sur le terrain """
        self.view_field_screen.set_bot_pos(bot_id, team_color, pst[0], pst[1], theta)

    # noinspection PyMethodMayBeStatic
    def set_field_size(self, frame_geometry_field):
        """ Modifie la dimension du terrain provenant des frames de vision"""
        QtToolBox.field_ctrl.set_field_size(frame_geometry_field)

    def hide_ball(self):
        if self.view_field_screen.isVisible():
            self.view_field_screen.hide_ball()

    def hide_mob(self, bot_id=None, team_color=None):
        """ Cache l'objet mobile si l'information n'est pas update """
        if self.view_field_screen.isVisible():
            self.view_field_screen.hide_bot(bot_id, team_color)

    def update_target_on_screen(self):
        """ Interruption pour mettre à jour les données de la cible """
        # noinspection PyPep8, PyBroadException
        try:
            self.view_field_screen.auto_toggle_visible_target()
        except Exception:
            # todo get rid of this too broad exception
            pass

    def add_logging_message(self, name, message, level=2):
        """ Ajoute un message de logging typé """
        self.model_datain.add_logging(name, message, level=level)

    def get_drawing_object(self, index):
        """ Récupère un dessin spécifique """
        return self.draw_handler.get_specific_draw_object(index)

    def toggle_full_screen(self):
        """ Déclenche le plein écran """
        if not self.windowState() == Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowFullScreen)
        else:
            self.setWindowState(Qt.WindowActive)

    # noinspection PyMethodMayBeStatic
    def flip_screen_x_axe(self):
        """ Bascule l'axe des X de l'écran """
        QtToolBox.field_ctrl.flip_x_axe()

    # noinspection PyMethodMayBeStatic
    def flip_screen_y_axe(self):
        """ Bascule l'axe des Y de l'écran """
        QtToolBox.field_ctrl.flip_y_axe()

    def get_list_of_filters(self):
        """ Récupère la liste des filtres d'affichage """
        name_filter = list(self.view_field_screen.draw_filterable.keys())
        name_filter += list(self.view_field_screen.multiple_points_map.keys())
        name_filter = set(name_filter)
        name_filter.add('None')
        return name_filter

    def set_list_of_filters(self, list_filter):
        """ Assigne une liste de filtres d'affichage """
        self.view_field_screen.list_filter = list_filter

    def deselect_all_robots(self):
        """ Désélectionne tous les robots sur le terrain """
        self.view_field_screen.deselect_all_robots()

    def select_robot(self, bot_id, team_color):
        """ Sélectionne le robot spécifié par l'index sur le terrain """
        self.view_field_screen.select_robot(bot_id, team_color)

    def get_tactic_controller_is_visible(self):
        """ Requête pour savoir le l'onglet de la page tactique est visible """
        return self.view_controller.page_tactic.isVisible()

    # noinspection PyUnusedLocal
    # todo remove useless third parameters after checking if we use it or could use it
    def force_tactic_controller_select_robot(self, bot_id, team_color):
        """ Force le sélection du robot indiqué par l'index dans la combobox du contrôleur tactique """
        self.view_controller.selectRobot.setCurrentIndex(bot_id)

    def get_cursor_position_from_screen(self):
        """ Récupère la position du curseur depuis le terrain """
        x, y = self.view_field_screen.get_cursor_position()
        coord_x, coord_y = QtToolBox.field_ctrl.convert_screen_to_real_pst(x, y)
        return int(coord_x), int(coord_y)

    def toggle_recorder(self, p_bool):
        """ Active/Désactive le Recorder """
        if p_bool:
            self.model_frame.enable_recorder()
            self.model_datain.enable_recorder()
        else:
            self.model_frame.disable_recorder()
            self.model_datain.disable_recorder()

    def get_fps(self):
        """ Récupère la fréquence de rafraîchissement de l'écran """
        return self.view_field_screen.get_fps()

    def get_is_serial(self):
        """ Récupère si le serveur de strategyIA est en mode serial (True) ou udp (False)"""
        return self.ai_server_is_serial

    def set_is_serial(self, is_serial):
        """ Détermine si le serveur de strategyIA est en mode serial (True) ou udp (False)"""
        self.ai_server_is_serial = is_serial

    def send_handshake(self):
        """ Envoie un HandShake au client """
        self.model_dataout.send_handshake()

    def send_ports_rs(self):
        ports_info = dict(zip(['recv_port',
                               'send_port'],
                              [self.network_data_in.get_rcv_port(),
                               self.network_data_in.get_snd_port()]))
        self.model_dataout.send_ports_rs(ports_info)

    def send_server(self):
        """ Envoie si le serveur utilisé par strategyIA est en serial (True) ou en udp (False)"""
        server_info = dict(zip(['is_serial', 'ip', 'port'],
                               [self.ai_server_is_serial,
                                self.network_vision.get_ip(),
                                self.network_vision.get_port()]))
        self.model_dataout.send_server(server_info)

    # todo remove for real
    # moved to ParamtetersSubMenuController
    # def send_udp_config(self):
    #     udp_config_info = dict(zip(['ip', 'port'],
    #                                [self.udp_config.ip,
    #                                 self.udp_config.port]))
    #     self.model_dataout.send_udp_config(udp_config_info)

    def send_geometry(self):
        """ Envoie la géométrie du terrain """
        self.model_dataout.send_geometry(QtToolBox.field_ctrl)

    def waiting_for_robot_strategic_state(self):
        return self.model_datain.waiting_for_robot_strategic_state_event()

    def waiting_for_robot_state(self):
        return self.model_datain.waiting_for_robot_state_event()

    def waiting_for_play_info(self):
        return self.model_datain.waiting_for_play_info_event()

    def waiting_for_game_state(self):
        return self.model_datain.waiting_for_game_state_event()

    def get_team_color(self):
        return self.team_color

    # === RECORDER METHODS ===
    def recorder_is_playing(self):
        return self.model_recorder.is_playing()

    def recorder_get_cursor_percentage(self):
        return self.model_recorder.get_cursor_percentage()

    def recorder_trigger_pause(self):
        self.model_recorder.pause()

    def recorder_trigger_play(self):
        self.model_recorder.play()

    def recorder_trigger_back(self):
        self.model_recorder.back()

    def recorder_trigger_rewind(self):
        self.model_recorder.rewind()

    def recorder_trigger_forward(self):
        self.model_recorder.forward()

    def recorder_skip_to(self, value):
        self.model_recorder.skip_to(value)

    def save_teams_formation(self):
        self.teams_formation = self.view_field_screen.get_teams_formation()

    def restore_teams_formation(self):
        self.grsim_sender.send_robots_position(self.teams_formation)
