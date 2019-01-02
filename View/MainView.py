# Under MIT License, see LICENSE.txt

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout, QHBoxLayout, QPushButton, QMenuBar, QAction, QMessageBox

from Controller import MainController
from View.ParametersSubMenuView import ParametersSubMenuView


class MainView(QWidget):

    def __init__(self, controller: MainController):
        super().__init__(None, Qt.Widget)
        self._controller = controller

        self.view_param = ParametersSubMenuView(self, self._controller, self._controller.parameters_submenu_controller)
        self.init_ui()

    # noinspection PyArgumentList
    def init_ui(self):
        self.setWindowTitle('RoboCup ULaval | GUI Debug | Team ' + 'blue')
        self.setWindowIcon(QIcon('Img/favicon.jpg'))
        self.resize(975, 550)

        sub_layout = QSplitter(self)
        sub_layout.setContentsMargins(0, 0, 0, 0)

        field_widget = QWidget()
        field_layout = QVBoxLayout()

        # under the field buttons: Save teams and restore teams buttons
        under_the_field_buttons_widget = QWidget()
        under_the_field_buttons_layout = QHBoxLayout(field_widget)

        btn_save_teams_formation = QPushButton("Save teams formation")
        btn_save_teams_formation.clicked.connect(self._controller.save_teams_formation)
        btn_restore_teams_formation = QPushButton("Restore teams formation")
        btn_restore_teams_formation.clicked.connect(self._controller.restore_teams_formation)
        under_the_field_buttons_layout.addWidget(btn_save_teams_formation)
        under_the_field_buttons_layout.addWidget(btn_restore_teams_formation)
        under_the_field_buttons_layout.setContentsMargins(0, 0, 0, 0)
        under_the_field_buttons_widget.setLayout(under_the_field_buttons_layout)

        # field_layout.addWidget(self.view_field_screen)
        field_layout.addWidget(under_the_field_buttons_widget)
        field_widget.setLayout(field_layout)

        sub_layout.addWidget(field_widget)

        QSplitter.setSizes(sub_layout, [200, 500, 100, 100])

        ver_splitter = QSplitter(Qt.Vertical, self)
        ver_splitter.setContentsMargins(0, 0, 0, 0)

        ver_splitter.addWidget(sub_layout)
        view_menu = QMenuBar(self)

        main_layout = QVBoxLayout()
        main_layout.addWidget(view_menu)
        main_layout.addWidget(ver_splitter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        view_menu.setFixedHeight(30)

        file_menu = view_menu.addMenu('Fichier')
        view_menu = view_menu.addMenu('Affichage')
        tool_menu = view_menu.addMenu('Outil')
        help_menu = view_menu.addMenu('Aide')
        shortcuts_action = QAction('Raccourcis', self)
        help_action = QAction('À propos', self)
        # noinspection PyUnresolvedReferences
        shortcuts_action.triggered.connect(self.set_shorcuts_message_box)
        # noinspection PyUnresolvedReferences
        help_action.triggered.connect(self.set_about_message_box)
        help_menu.addAction(shortcuts_action)
        help_menu.addAction(help_action)

        # => Menu Fichier

        param_action = QAction('Paramètres', self)
        param_action.triggered.connect(self.view_param.show)
        file_menu.addAction(param_action)

        file_menu.addSeparator()

        exit_action = QAction('Quitter', self)
        # exit_action.triggered.connect(self.closeEvent)
        file_menu.addAction(exit_action)

        # => Menu Vue
        field_menu = view_menu.addMenu('Terrain')

        toggle_frame_rate = QAction("Afficher la fréquence", self)
        toggle_frame_rate.setCheckable(True)
        # toggle_frame_rate.triggered.connect(self.view_field_screen.toggle_frame_rate)
        field_menu.addAction(toggle_frame_rate)

        field_menu.addSeparator()

        flip_x_action = QAction("Changer l'axe des X", self)
        flip_x_action.setCheckable(True)
        # flip_x_action.triggered.connect(self.flip_screen_x_axe)
        field_menu.addAction(flip_x_action)

        flip_y_action = QAction("Changer l'axe des Y", self)
        flip_y_action.setCheckable(True)
        # flip_y_action.triggered.connect(self.flip_screen_y_axe)
        field_menu.addAction(flip_y_action)

        view_menu.addSeparator()

        cam_menu = view_menu.addMenu('Camera')

        reset_cam_action = QAction("Réinitialiser la caméra", self)
        # reset_cam_action.triggered.connect(self.view_field_screen.reset_camera)
        cam_menu.addAction(reset_cam_action)

        lock_cam_action = QAction("Bloquer la caméra", self)
        # lock_cam_action.triggered.connect(self.view_field_screen.toggle_lock_camera)
        cam_menu.addAction(lock_cam_action)

        view_menu.addSeparator()

        bot_menu = view_menu.addMenu('Robot')

        vector_action = QAction('Afficher Vecteur vitesse des robots', self)
        vector_action.setCheckable(True)
        # vector_action.triggered.connect(self.view_field_screen.toggle_vector_option)
        bot_menu.addAction(vector_action)

        nuumb_action = QAction('Afficher Numéro des robots', self)
        nuumb_action.setCheckable(True)
        # nuumb_action.triggered.connect(self.view_field_screen.show_number_option)
        nuumb_action.trigger()
        bot_menu.addAction(nuumb_action)

        view_menu.addSeparator()

        fullscreen_action = QAction('Fenêtre en Plein écran', self)
        fullscreen_action.setCheckable(True)
        # fullscreen_action.triggered.connect(self.toggle_full_screen)
        fullscreen_action.setShortcut(Qt.Key_F2)
        view_menu.addAction(fullscreen_action)

        # => Menu Outil
        filter_action = QAction('Filtre pour dessins', self)
        filter_action.setCheckable(True)
        # filter_action.triggered.connect(self.view_filter.show_hide)
        tool_menu.addAction(filter_action)

        strategy_controller_action = QAction('Contrôleur de Stratégie', self)
        strategy_controller_action.setCheckable(True)
        strategy_controller_action.setChecked(False)
        # strategy_controller_action.triggered.connect(self.view_controller.toggle_show_hide)
        # strategy_controller_action.trigger()
        tool_menu.addAction(strategy_controller_action)

        tool_menu.addSeparator()

        media_action = QAction('Contrôleur Média', self, checkable=True)
        # mediaAction.triggered.connect(self.view_media.toggle_visibility)
        tool_menu.addAction(media_action)

        rob_state_action = QAction('État des robots', self)
        rob_state_action.setCheckable(True)
        # rob_state_action.triggered.connect(self.view_robot_state.show_hide)
        # rob_state_action.trigger()
        tool_menu.addAction(rob_state_action)

        logger_action = QAction('Loggeur', self)
        logger_action.setCheckable(True)
        # logger_action.triggered.connect(self.view_logger.show_hide)
        tool_menu.addAction(logger_action)

        plotter_action = QAction('Plot', self)
        plotter_action.setCheckable(True)
        # plotter_action.triggered.connect(self.view_plotter.show_hide)
        tool_menu.addAction(plotter_action)

    def set_about_message_box(self):
        # noinspection PyCallByClass
        QMessageBox.about(self, 'À Propos', 'ROBOCUP ULAVAL © 2016\n\ncontact@robocupulaval.com')

    def set_shorcuts_message_box(self):
        # noinspection PyCallByClass
        QMessageBox.about(self, 'Raccourcis', '\n'.join(['- Double-clic droit : Placer la balle',
                                                         '- Ctrl : Entrer dans le mode slingshot',
                                                         '\n  Dans le mode slingshot :\n',
                                                         '- Shift : Verrouiller la force du tir',
                                                         '- Clic gauche pour tirer la balle']))
