# Under MIT License, see LICENSE.txt
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, \
    QGroupBox, QFormLayout, QLineEdit, QLabel, \
    QPushButton, QHBoxLayout, QRadioButton

from Controller import MainController, ParametersSubMenuController
from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


class ParametersSubMenuView(QDialog):
    def __init__(self, parent, controller: MainController,
                 own_controller: ParametersSubMenuController):
        super().__init__(parent, Qt.Dialog)
        self._controller = controller
        self._own_controller = own_controller
        self._layout = QVBoxLayout()
        self.tabs_widget = QTabWidget(self)
        self._dimensions_tab = QWidget(self, Qt.Widget)
        self._network_tab = QWidget(self, Qt.Widget)
        self.init_ui()
        self.init_network_tab()
        self.init_dimension_tab()
        self.init_bottom_page()

    # noinspection PyArgumentList
    def init_ui(self):
        self._layout.addWidget(self.tabs_widget)
        self.tabs_widget.addTab(self._dimensions_tab, 'Dimensions')
        self.tabs_widget.addTab(self._network_tab, 'Réseau')

        self.setWindowTitle('Paramètres')
        self.move(150, 150)
        self.setLayout(self._layout)

    # noinspection PyAttributeOutsideInit,PyUnresolvedReferences,PyArgumentList
    def init_network_tab(self):
        network_tab_main_layout = QVBoxLayout(self._network_tab)
        network_tab_main_layout.setAlignment(QtCore.Qt.AlignTop)
        self._network_tab.setLayout(network_tab_main_layout)

        # PARAM UI Server
        ui_server_box = QGroupBox('UI Server')
        network_tab_main_layout.addWidget(ui_server_box)
        ui_server_box_form_layout = QFormLayout()
        ui_server_box.setLayout(ui_server_box_form_layout)

        # => network ui server receiving port
        self.network_ui_server_receiving_port = QLineEdit()
        ui_server_box_form_layout.addRow(QLabel("Port de réception :"), self.network_ui_server_receiving_port)
        # => network ui server sending port
        self.network_ui_server_sending_port = QLineEdit()
        ui_server_box_form_layout.addRow(QLabel("Port d'envoi :"), self.network_ui_server_sending_port)
        # => Bouton envoie des ports recv et send
        button_send_ports_ui_server = QPushButton('Envoyer les paramètres')
        button_send_ports_ui_server.clicked.connect(self._controller.send_ports_rs)
        ui_server_box_form_layout.addRow(button_send_ports_ui_server)

        # PARAM VISION
        group_vision_box = QGroupBox('Vision')
        network_tab_main_layout.addWidget(group_vision_box)
        ui_server_box_form_layout = QFormLayout()
        group_vision_box.setLayout(ui_server_box_form_layout)

        # => IP
        self.network_vision_ip_address = QLineEdit()
        ui_server_box_form_layout.addRow(QLabel("IP :"), self.network_vision_ip_address)

        # => Port
        self.network_vision_port = QLineEdit()
        ui_server_box_form_layout.addRow(QLabel("Port :"), self.network_vision_port)

        # => UDP/Serial
        self.radiobox_vision_udp = QRadioButton()
        self.radiobox_vision_udp.setChecked(True)
        self.radiobox_vision_udp_label = QLabel("UDP :")
        ui_server_box_form_layout.addRow(self.radiobox_vision_udp_label, self.radiobox_vision_udp)

        self.radiobox_vision_serial = QRadioButton()
        self.radiobox_vision_serial.toggled.connect(self.toggle_udp_config)
        ui_server_box_form_layout.addRow(QLabel("Serial :"), self.radiobox_vision_serial)

        button_send_vision_serveur_infos = QPushButton('Envoyer les paramètres du réseau')
        button_send_vision_serveur_infos.clicked.connect(self._controller.send_server)
        ui_server_box_form_layout.addRow(button_send_vision_serveur_infos)

        # PARAM UI Server
        group_udp_serial = QGroupBox('Configuration UDP/Serial')
        network_tab_main_layout.addWidget(group_udp_serial)
        ui_server_box_form_layout = QFormLayout()
        group_udp_serial.setLayout(ui_server_box_form_layout)

        # => IP Multicast UDP
        self.form_udp_multicast_ip = QLineEdit()
        ui_server_box_form_layout.addRow(QLabel("IP Multicast:"), self.form_udp_multicast_ip)
        # => Port Multicast UDP
        self.form_udp_multicast_port = QLineEdit()
        ui_server_box_form_layout.addRow(QLabel("Port Multicast:"), self.form_udp_multicast_port)
        # => Bouton envoie configuration UDP
        # todo ask about button to send configuration
        but_send_udp_multicast = QPushButton('Envoyer les paramètres de l\'UDP')
        but_send_udp_multicast.clicked.connect(self._own_controller.send_udp_config)
        ui_server_box_form_layout.addRow(but_send_udp_multicast)

    # noinspection PyAttributeOutsideInit,PyUnresolvedReferences,PyArgumentList
    def init_dimension_tab(self):
        layout_main = QVBoxLayout(self._dimensions_tab)
        self._dimensions_tab.setLayout(layout_main)

        # Changement des dimensions du terrain
        group_field = QGroupBox('Dimensions')
        layout_main.addWidget(group_field)
        layout_field = QFormLayout()
        group_field.setLayout(layout_field)

        # => Taille du terrain (Longueur / Largeur)
        layout_field.addRow(QLabel('\nDimension du terrain'))
        self.form_field_length = QLineEdit()
        layout_field.addRow(QLabel('longueur :'), self.form_field_length)
        self.form_field_width = QLineEdit()
        layout_field.addRow(QLabel('largeur :'), self.form_field_width)

        # => Taille du but (largeur / profondeur)
        layout_field.addRow(QLabel('\nDimension des buts'))
        self.form_goal_depth = QLineEdit()
        layout_field.addRow(QLabel('profondeur :'), self.form_goal_depth)
        self.form_goal_width = QLineEdit()
        layout_field.addRow(QLabel('largeur :'), self.form_goal_width)

        # => Taille de la zone de réparation (Rayon / Ligne)
        layout_field.addRow(QLabel('\nZone des buts'))
        self.form_defense_radius = QLineEdit()
        layout_field.addRow(QLabel('rayon :'), self.form_defense_radius)
        self.form_defense_stretch = QLineEdit()
        layout_field.addRow(QLabel('largeur :'), self.form_defense_stretch)

        # => Taille de la zone centrale (Rayon)
        layout_field.addRow(QLabel('\nRayon central'))
        self.form_center_radius = QLineEdit()
        layout_field.addRow(QLabel('rayon :'), self.form_center_radius)

        # Changement de ratio Mobs / Terrain
        layout_field.addRow(QLabel('\nRatio Terrain/Mobs'))
        self.form_ratio_mobs = QLineEdit()
        layout_field.addRow(QLabel('ratio :'), self.form_ratio_mobs)

        self.restore_values()

        but_send_geometry = QPushButton('Envoyer la Géométrie du terrain')
        but_send_geometry.clicked.connect(self._controller.send_geometry)
        layout_field.addRow(but_send_geometry)

    # noinspection PyArgumentList,PyUnresolvedReferences
    def init_bottom_page(self):
        # Bas de fenêtre
        layout_bottom = QHBoxLayout()
        self._layout.addLayout(layout_bottom)

        # => Bouton OK
        but_ok = QPushButton('Ok')
        but_ok.clicked.connect(self._apply_param_and_leave)
        layout_bottom.addWidget(but_ok)

        # => Bouton Annuler
        but_cancel = QPushButton('Annuler')
        but_cancel.clicked.connect(self.hide)
        layout_bottom.addWidget(but_cancel)

        # => Bouton Appliquer
        but_apply = QPushButton('Appliquer')
        but_apply.clicked.connect(self._apply_param)
        layout_bottom.addWidget(but_apply)

        # => Bouton Défaut
        but_default = QPushButton('Défaut')
        but_default.setStyleSheet("QPushButton {font:italic}")
        but_default.clicked.connect(self.restore_default_values)
        layout_bottom.addWidget(but_default)

    def _apply_param_and_leave(self):
        if self._apply_param():
            self.hide()

    def restore_default_values(self):
        # FIELD DIMENSION
        self.form_ratio_mobs.setText(str(QtToolBox.field_ctrl.ratio_field_mobs_default))

        # NETWORK
        self.network_ui_server_receiving_port.setText(str(self._controller.network_data_in.get_default_rcv_port()))
        self.network_ui_server_sending_port.setText(str(self._controller.network_data_in.get_default_snd_port()))
        self.network_vision_ip_address.setText(str(self._controller.network_vision.get_default_ip()))
        self.network_vision_port.setText(str(self._controller.network_vision.get_default_port()))
        self.radiobox_vision_serial.setChecked(False)
        self.radiobox_vision_udp.setChecked(True)
        self.form_udp_multicast_ip.setText(str(self._own_controller.default_vision_ip_address))
        self.form_udp_multicast_ip.setDisabled(False)
        self.form_udp_multicast_port.setText(str(self._own_controller.default_vision_port))
        self.form_udp_multicast_port.setDisabled(False)

        self._apply_param()

    def restore_values(self):
        self.form_field_length.setText(str(QtToolBox.field_ctrl.field_length))
        self.form_field_width.setText(str(QtToolBox.field_ctrl.field_width))

        self.form_goal_depth.setText(str(QtToolBox.field_ctrl.goal_depth))
        self.form_goal_width.setText(str(QtToolBox.field_ctrl.goal_width))

        self.form_defense_radius.setText(str(QtToolBox.field_ctrl.defense_radius))
        self.form_defense_stretch.setText(str(QtToolBox.field_ctrl.defense_stretch))

        self.form_center_radius.setText(str(QtToolBox.field_ctrl.center_circle_radius))

        self.form_ratio_mobs.setText(str(QtToolBox.field_ctrl.ratio_field_mobs))

        self.network_ui_server_receiving_port.setText(str(self._controller.network_data_in.get_rcv_port()))
        self.network_ui_server_sending_port.setText(str(self._controller.network_data_in.get_snd_port()))
        self.network_vision_ip_address.setText(str(self._controller.network_vision.get_ip()))
        self.network_vision_port.setText(str(self._controller.network_vision.get_port()))
        self.form_udp_multicast_ip.setText(str(self._controller.config['COMMUNICATION']['vision_address']))
        self.form_udp_multicast_port.setText(str(self._controller.config['COMMUNICATION']['vision_port']))

    def toggle_udp_config(self):
        if self.radiobox_vision_serial.isChecked():
            self.form_udp_multicast_ip.setDisabled(True)
            self.form_udp_multicast_port.setDisabled(True)
        else:
            self.form_udp_multicast_ip.setDisabled(False)
            self.form_udp_multicast_port.setDisabled(False)

    def hide(self):
        self.restore_values()
        self._apply_param()
        super().hide()

    # noinspection PyBroadException,PyUnusedLocal
    def _apply_param(self):
        is_wrong = False
        style_bad = "QLineEdit {background: rgb(255, 100, 100)}"
        style_good = "QLineEdit {background: rgb(255, 255, 255)}"

        try:
            self.form_field_length.setStyleSheet(style_good)
            QtToolBox.field_ctrl.field_length = int(self.form_field_length.text())
        except Exception as e:
            self.form_field_length.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_field_width.setStyleSheet(style_good)
            QtToolBox.field_ctrl.field_width = int(self.form_field_width.text())
        except Exception as e:
            self.form_field_width.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_goal_depth.setStyleSheet(style_good)
            QtToolBox.field_ctrl.goal_depth = int(self.form_goal_depth.text())
        except Exception as e:
            self.form_goal_depth.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_goal_width.setStyleSheet(style_good)
            QtToolBox.field_ctrl.goal_width = int(self.form_goal_width.text())
        except Exception as e:
            self.form_goal_width.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_center_radius.setStyleSheet(style_good)
            QtToolBox.field_ctrl.center_circle_radius = int(self.form_center_radius.text())
        except Exception as e:
            self.form_center_radius.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_defense_radius.setStyleSheet(style_good)
            QtToolBox.field_ctrl.defense_radius = int(self.form_defense_radius.text())
        except Exception as e:
            self.form_defense_radius.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_defense_stretch.setStyleSheet(style_good)
            QtToolBox.field_ctrl.defense_stretch = int(self.form_defense_stretch.text())
        except Exception as e:
            self.form_defense_stretch.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_ratio_mobs.setStyleSheet(style_good)
            QtToolBox.field_ctrl.ratio_field_mobs = float(self.form_ratio_mobs.text())
        except Exception as e:
            print(e)
            self.form_ratio_mobs.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.network_ui_server_receiving_port.setStyleSheet(style_good)
            if not self._controller.network_data_in.get_rcv_port() == int(self.network_ui_server_receiving_port.text()):
                self._controller.network_data_in.new_rcv_connexion(int(self.network_ui_server_receiving_port.text()))
        except Exception as e:
            self.network_ui_server_receiving_port.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.network_ui_server_sending_port.setStyleSheet(style_good)
            if not self._controller.network_data_in.get_snd_port() == int(self.network_ui_server_sending_port.text()):
                self._controller.network_data_in.set_snd_port(int(self.network_ui_server_sending_port.text()))
        except Exception as e:
            self.network_ui_server_sending_port.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.network_vision_ip_address.setStyleSheet(style_good)
            self.network_ui_server_receiving_port.setStyleSheet(style_good)
            if not self._controller.network_vision.get_ip() == str(self.network_vision_ip_address.text()) \
                    or not self._controller.network_vision.get_port() == int(self.network_vision_port.text()):
                self._controller.network_vision.set_new_connexion(str(self.network_vision_ip_address.text()),
                                                                  int(self.network_vision_port.text()))
        except Exception as e:
            self.network_vision_ip_address.setStyleSheet(style_bad)
            self.network_vision_port.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.radiobox_vision_serial.setStyleSheet(style_good)
            self.radiobox_vision_udp_label.setStyleSheet(style_good)
            if self._controller.get_is_serial != self.radiobox_vision_serial.isChecked():
                self._controller.set_is_serial(self.radiobox_vision_serial.isChecked())
            self.toggle_udp_config()
        except Exception as e:
            self.radiobox_vision_serial.setStyleSheet(style_bad)
            self.radiobox_vision_udp_label.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_udp_multicast_ip.setStyleSheet(style_good)
            if self._own_controller.default_vision_ip_address != str(self.form_udp_multicast_ip.text()):
                self._own_controller.default_vision_ip_address = self.form_udp_multicast_ip.text()
            self.toggle_udp_config()
        except Exception as e:
            self.form_udp_multicast_ip.setStyleSheet(style_bad)
            is_wrong = True

        try:
            self.form_udp_multicast_port.setStyleSheet(style_good)
            if self._own_controller.default_vision_port != str(self.form_udp_multicast_port.text()):
                self._own_controller.default_vision_port = self.form_udp_multicast_port.text()
        except Exception as e:
            self.form_udp_multicast_port.setStyleSheet(style_bad)
            is_wrong = True

        if is_wrong:
            return False
        else:
            return True
