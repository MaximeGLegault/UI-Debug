# Under MIT License, see LICENSE.txt
from collections import OrderedDict

from PyQt5 import QtCore, Qt

from PyQt5.QtCore import QRect
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QAbstractSpinBox, QCheckBox
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QComboBox, \
                            QPushButton, QGroupBox, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont, QPalette, QColor, QCursor
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal

from Controller.QtToolBox import QtToolBox

__author__ = 'RoboCupULaval'


MAX_NUMBER_ROBOTS = 16


class StrategyCtrView(QWidget):

    NO_STRAT_LABEL = 'Aucune Stratégie disponible'
    NO_TACTIC_LABEL = 'Aucune Tactique disponible'

    def __init__(self, parent, controller):
        QWidget.__init__(self, parent)
        self._controller = controller
        self.play_info = None

        self.init_ui()
        self.hide()

        self._play_info_loop = QThread()
        self.init_loop()

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_combobox)
        self.update_timer.start(500)

        self.strategies = {}
        self.required_roles = {}
        self.optional_roles = {}
        self.tactic_default = []

    def init_loop(self):
        self._play_info_loop.run = self.update_play_info
        self._play_info_loop.daemon = True
        self._play_info_loop.start()

    def init_ui(self):
        self._active_team = 'green'

        # Création des pages d'onglet
        self.main_layout = QVBoxLayout(self)
        self.page_controller = QTabWidget(self)
        self.page_autonomous = QWidget()
        self.page_strategy = QWidget()
        self.page_tactic = QWidget()
        self.main_layout.addWidget(self.page_controller)
        self._layout = self.main_layout

        # Change background color to team's color
        bg_color = QColor("#3498db") if self._controller.team_color == "blue" else QColor("#f1c40f")
        self._reset_background_color_to(bg_color)

        # Création du contenu des pages
        # + Page Team
        self.page_autonomous_vbox = QVBoxLayout()
        self.page_autonomous_scrollarea = QScrollArea(self)
        self.page_autonomous_scrollarea.setGeometry(QRect(0, 0, 390, 190))
        self.page_autonomous_scrollarea.setWidgetResizable(True)

        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderLabels(["", ""])
        self.treeWidget.setColumnCount(2)
        self.page_autonomous_scrollarea.setWidget(self.treeWidget)

        self._populate_play_info()


        self.page_autonomous_but_play = QPushButton("Start")
        self.page_autonomous_but_play.clicked.connect(self.send_start_auto)
        but_play_font = QFont()
        but_play_font.setBold(True)
        self.page_autonomous_but_play.setFont(but_play_font)
        self.page_autonomous_but_play.setStyleSheet('QPushButton {color:green;}')

        self.page_autonomous_but_stop = QPushButton("Stop")
        self.page_autonomous_but_stop.clicked.connect(self.send_stop_auto)
        self.page_autonomous_but_stop.setFont(but_play_font)
        self.page_autonomous_but_stop.setStyleSheet('QPushButton {color:red;}')
        self.page_autonomous_but_stop.setVisible(False)

        self.page_autonomous_vbox.addWidget(self.page_autonomous_scrollarea)
        self.page_autonomous_vbox.addWidget(self.page_autonomous_but_play)
        self.page_autonomous_vbox.addWidget(self.page_autonomous_but_stop)

        self.page_autonomous.setLayout(self.page_autonomous_vbox)

        # + Page Strategy
        self.page_strat_vbox = QVBoxLayout()
        self.selectStrat = QComboBox()
        self.selectStrat.addItem(self.NO_STRAT_LABEL)
        self.selectStrat.currentIndexChanged.connect(self.strategy_selected)
        self.page_strat_use_role = QCheckBox("Forcer les rôles")
        self.page_strat_use_role.stateChanged.connect(self.toggle_strat_use_role)

        # QGroupBox Required Roles
        self.page_strat_form_required_roles = QFormLayout()
        qgroup_required_roles = QGroupBox('Sélectionnez les rôles obligatoires', self.page_strategy)
        required_roles_combox = QVBoxLayout()
        required_roles_combox.addLayout(self.page_strat_form_required_roles)
        qgroup_required_roles.setLayout(required_roles_combox)

        # QGroupBox Optional Roles
        self.page_strat_form_optional_roles = QFormLayout()
        qgroup_optional_roles = QGroupBox('Sélectionnez les rôles optionnels', self.page_strategy)
        optional_roles_combox = QVBoxLayout()
        optional_roles_combox.addLayout(self.page_strat_form_optional_roles)
        qgroup_optional_roles.setLayout(optional_roles_combox)

        # QGroupBox Strategy
        qgroup_strategy = QGroupBox('Sélectionnez votre stratégie', self.page_strategy)
        strat_combox = QVBoxLayout()
        strat_combox.addWidget(self.page_strat_use_role)
        strat_combox.addWidget(self.selectStrat)
        qgroup_strategy.setLayout(strat_combox)

        self.page_strat_but_quick1 = QPushButton('')
        self.page_strat_but_quick1.clicked.connect(self.send_quick_strat1)
        self.page_strat_but_quick1.setVisible(False)
        self.page_strat_but_quick2 = QPushButton('')
        self.page_strat_but_quick2.clicked.connect(self.send_quick_strat2)
        self.page_strat_but_quick2.setVisible(False)
        self.page_strat_but_apply = QPushButton('Appliquer')
        self.page_strat_but_apply.clicked.connect(self.send_selected_strat)
        self.page_strat_but_cancel = QPushButton("STOP (S)")
        but_cancel_font = QFont()
        but_cancel_font.setBold(True)
        self.page_strat_but_cancel.setFont(but_cancel_font)
        self.page_strat_but_cancel.setStyleSheet('QPushButton {color:red;}')
        self.page_strat_but_cancel.clicked.connect(self.send_strat_stop)


        but_quick_group = QHBoxLayout()
        but_quick_group.addWidget(self.page_strat_but_quick1)
        but_quick_group.addWidget(self.page_strat_but_quick2)
        but_group = QHBoxLayout()
        but_group.addWidget(self.page_strat_but_apply)
        but_group.addWidget(self.page_strat_but_cancel)
        self.page_strat_vbox.addWidget(qgroup_required_roles)
        self.page_strat_vbox.addWidget(qgroup_optional_roles)
        self.page_strat_vbox.addWidget(qgroup_strategy)
        self.page_strat_vbox.addLayout(but_quick_group)
        self.page_strat_vbox.addLayout(but_group)

        self.page_strategy.setLayout(self.page_strat_vbox)

        # + Page Tactic
        self.page_tact_vbox = QVBoxLayout()

        group_bot_select = QGroupBox('Sélectionnez la tactique du robot', self.page_tactic)
        group_vbox = QVBoxLayout()
        group_bot_select.setLayout(group_vbox)

        group_vbox.addWidget(QLabel('ID du robot :'))
        self.selectRobot = QComboBox()
        [self.selectRobot.addItem(str(x)) for x in range(MAX_NUMBER_ROBOTS)]
        self.selectRobot.currentIndexChanged.connect(self.handle_selection_robot_event_id)
        group_vbox.addWidget(self.selectRobot)

        group_vbox.addWidget(QLabel('Tactique à appliquer :'))
        self.selectTactic = QComboBox()
        self.selectTactic.addItem(self.NO_TACTIC_LABEL)
        group_vbox.addWidget(self.selectTactic)
        self.argumentsLine = QLineEdit()
        group_vbox.addWidget(self.argumentsLine)

        but_group_quick = QHBoxLayout()
        self.page_tactic_but_quick1 = QPushButton('')
        self.page_tactic_but_quick1.clicked.connect(self.send_quick_tactic1)
        self.page_tactic_but_quick1.setVisible(False)
        but_group_quick.addWidget(self.page_tactic_but_quick1)
        self.page_tactic_but_quick2 = QPushButton('')
        self.page_tactic_but_quick2.clicked.connect(self.send_quick_tactic2)
        self.page_tactic_but_quick2.setVisible(False)
        but_group_quick.addWidget(self.page_tactic_but_quick2)

        but_group_tact = QHBoxLayout()
        tact_apply_but = QPushButton('Appliquer')
        tact_apply_but.clicked.connect(self.send_apply_tactic)
        but_group_tact.addWidget(tact_apply_but)

        tact_stop_but = QPushButton('STOP (S)')
        tact_stop_but.setFont(but_cancel_font)
        tact_stop_but.setStyleSheet('QPushButton {color:red;}')
        tact_stop_but.clicked.connect(self.send_tactic_stop)
        but_group_tact.addWidget(tact_stop_but)

        tact_stop_all_but = QPushButton('STOP ALL')
        tact_stop_all_but.setFont(but_cancel_font)
        tact_stop_all_but.setStyleSheet('QPushButton {color:red;}')
        tact_stop_all_but.clicked.connect(self.send_tactic_stop_all)

        self.page_tact_vbox.addWidget(group_bot_select)
        self.page_tact_vbox.addLayout(but_group_quick)
        self.page_tact_vbox.addLayout(but_group_tact)
        self.page_tact_vbox.addWidget(tact_stop_all_but)

        self.page_tactic.setLayout(self.page_tact_vbox)

        # + Onglets
        self.page_controller.addTab(self.page_autonomous, 'AutoPlay')
        self.page_controller.addTab(self.page_strategy, 'Stratégie')
        self.page_controller.addTab(self.page_tactic, 'Tactique')
        self.page_controller.currentChanged.connect(self.tab_selected)

    @pyqtSlot(int)
    def handle_selection_robot_event_id(self, index):
        self._controller.deselect_all_robots()
        self._controller.select_robot(index, self._controller.get_team_color())

    @pyqtSlot(int)
    def handle_selection_robot_event_team(self, index):
        self._controller.deselect_all_robots()
        self._controller.select_robot(self.selectRobot.currentIndex(), self._controller.get_team_color())

    @pyqtSlot(int)
    def tab_selected(self, index):
        if index == 0 or index == 1:
            self._controller.deselect_all_robots()
        elif index == 2:
            id_bot = self.selectRobot.currentIndex()
            self._controller.select_robot(id_bot, self._controller.get_team_color())

    @pyqtSlot(str)
    def handle_team_color(self, team_color):
        self._active_team = team_color.lower()
        self.teamColorLabel.setText(self._controller.get_team_color().capitalize())

    def hideEvent(self, event):
        self._controller.deselect_all_robots()
        super().hideEvent(event)

    def keyPressEvent(self, event):
        key = event.key()

        pos = self._controller.view_field_screen.mapFromGlobal(QCursor.pos())
        if key == QtCore.Qt.Key_Plus:
            QtToolBox.field_ctrl.zoom(pos.x(), pos.y(), QtToolBox.field_ctrl.scroll_slowing_factor)
        elif key == QtCore.Qt.Key_Minus:
            QtToolBox.field_ctrl.dezoom(pos.x(), pos.y(), -QtToolBox.field_ctrl.scroll_slowing_factor)

        page_id = self.page_controller.currentIndex()
        if page_id == 1: # Strategy
            if key == QtCore.Qt.Key_Q:
                self.send_quick_strat1()
            if key == QtCore.Qt.Key_W:
                self.send_quick_strat2()
            if key == QtCore.Qt.Key_S:
                self.send_strat_stop()
        elif page_id == 2: # Tactic
            if key == QtCore.Qt.Key_Q:
                self.send_quick_tactic1()
            if key == QtCore.Qt.Key_W:
                self.send_quick_tactic2()
            if key == QtCore.Qt.Key_S:
                self.send_tactic_stop()

    def _reset_background_color_to(self, bg_color):
        palette = QPalette()
        palette.setColor(self.backgroundRole(), bg_color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def update_combobox(self):
        if self._controller.model_datain._data_STA_config is not None:
            data = self._controller.model_datain._data_STA_config.data

            if data['tactic'] is not None:
                tactics = self.get_tactic_list()
                for tact in data['tactic']:
                    if not tact in tactics:
                        self.refresh_tactic(data['tactic'])
                        break

            if data['strategy'] is not None:
                self.strategies = data['strategy']
                strats = self.get_strat_list()
                for strat in data['strategy']:
                    if not strat in strats:
                        self.refresh_strat(data['strategy'])
                        break

            if data['tactic_default'] is not None:
                self.refresh_tactic_default(data['tactic_default'])

            if data['strategy_default'] is not None:
                self.refresh_strat_default(data['strategy_default'])

        self._populate_play_info()

    def get_strat_list(self):
        strat = []
        for i in range(self.selectStrat.count()):
            if not self.selectStrat.count() == 1:
                strat.append(self.selectStrat.itemText(i))
        return strat

    def get_tactic_list(self):
        tactics = []
        for i in range(self.selectTactic.count()):
            if not self.selectTactic.count() == 1:
                tactics.append(self.selectTactic.itemText(i))
        return tactics

    def refresh_tactic_default(self, new_default):
        self.refresh_default(self.page_tactic_but_quick1,
                             self.page_tactic_but_quick2,
                             new_default)
        self.tactic_default = new_default

    def refresh_strat_default(self, new_default):
        self.refresh_default(self.page_strat_but_quick1,
                             self.page_strat_but_quick2,
                             new_default)
        self.strat_default = new_default

    def refresh_default(self, but1, but2, new_default):
        if len(new_default) > 0:
            but1.setVisible(True)
            but1.setText(new_default[0] + " (Q)")
        else:
            but1.setVisible(False)

        if len(new_default) > 1:
            but2.setVisible(True)
            but2.setText(new_default[1] + " (W)")
        else:
            but2.setVisible(False)


    def refresh_tactic(self, tactics):
        self.selectTactic.clear()
        if tactics is not None:
            tactics.sort()
            for tactic in tactics:
                self.selectTactic.addItem(tactic)
        else:
            self.selectTactic.addItem(self.NO_TACTIC_LABEL)

    def refresh_strat(self, strats):
        self.selectStrat.clear()
        if strats is not None:
            strats = OrderedDict(sorted(strats.items()))
            for strat in strats:
                self.selectStrat.addItem(strat)
        else:
            self.selectStrat.addItem(self.NO_STRAT_LABEL)

    def toggle_strat_use_role(self):
        for combo_box in (*self.required_roles.values(), *self.optional_roles.values()):
            combo_box.setEnabled(self.page_strat_use_role.isChecked())

    def strategy_selected(self):
        name = str(self.selectStrat.currentText())
        if name != '':
            # ====== Required Roles ======
            required_roles = self.strategies[name]["required_roles"]

            # Remove role widget
            nb_widget_required_roles = self.page_strat_form_required_roles.rowCount()
            for i in reversed(range(0, nb_widget_required_roles)):
                self.page_strat_form_required_roles.removeRow(i)

            # delete unused role
            for prev_role in list(self.required_roles.keys()):
                if prev_role not in required_roles:
                    del self.required_roles[prev_role]

            # Add new one
            for i, r in enumerate(required_roles):
                select_robot = QComboBox()
                [select_robot.addItem(str(x)) for x in range(MAX_NUMBER_ROBOTS)]

                self.page_strat_form_required_roles.insertRow(i, r, select_robot)

                self.required_roles[r] = select_robot
                self.required_roles[r].setEnabled(self.page_strat_use_role.isChecked())

            # ====== Optional Roles ======
            optional_roles = self.strategies[name]["optional_roles"]

            # Remove role widget
            nb_widget_optional_roles = self.page_strat_form_optional_roles.rowCount()
            for i in reversed(range(0, nb_widget_optional_roles)):
                self.page_strat_form_optional_roles.removeRow(i)

            # delete unused role
            for prev_role in list(self.optional_roles.keys()):
                if prev_role not in optional_roles:
                    del self.optional_roles[prev_role]

            # Add new one
            for i, r in enumerate(optional_roles):
                select_robot = QComboBox()
                select_robot.addItem("")
                [select_robot.addItem(str(x)) for x in range(MAX_NUMBER_ROBOTS)]

                self.page_strat_form_optional_roles.insertRow(i, r, select_robot)

                self.optional_roles[r] = select_robot
                self.optional_roles[r].setEnabled(self.page_strat_use_role.isChecked())

    def _send_strategy(self, strategy_name, role=None):
        self._controller.model_dataout.send_strategy(strategy_name, self._controller.get_team_color(), role)

    def send_quick_strat1(self):
        if len(self.strat_default) > 0:
            self._send_strategy(self.strat_default[0])

    def send_quick_strat2(self):
        if len(self.strat_default) > 1:
            self._send_strategy(self.strat_default[1])

    def send_quick_tactic1(self):
        if len(self.tactic_default) > 0:
            self.send_tactic(self.tactic_default[0])

    def send_quick_tactic2(self):
        if len(self.tactic_default) > 1:
            self.send_tactic(self.tactic_default[1])

    def send_selected_strat(self):
        strat_name = str(self.selectStrat.currentText())

        if self.page_strat_use_role.isChecked():
            roles = {r: int(box.currentText()) for r, box in dict(**self.required_roles, **self.optional_roles).items() if box.currentText() != ''}
            # In case we have twice the same id, change background color
            if len(set(roles.values())) != len(roles):
                bg_color = QColor("#FF0000")
                self._reset_background_color_to(bg_color)
                return
            else:
                bg_color = QColor("#3498db") if self._controller.team_color == "blue" else QColor("#f1c40f")
                self._reset_background_color_to(bg_color)
        else:
            roles = None

        if strat_name != self.NO_STRAT_LABEL:
            self._send_strategy(strat_name, roles)

    def send_apply_tactic(self):
        tactic = str(self.selectTactic.currentText())
        if tactic != self.NO_TACTIC_LABEL:
            self.send_tactic(tactic)

    def send_tactic(self, tactic: str):
        id_bot = int(self.selectRobot.currentText())
        args_textbox = str(self.argumentsLine.text()).split()
        target = self._controller.model_dataout.target
        self._controller.model_dataout.send_tactic(id_bot, self._controller.get_team_color(), tactic=tactic, target=target, args=args_textbox)

    def send_tactic_stop(self):
        id_bot = int(self.selectRobot.currentText())
        self._controller.model_dataout.send_tactic(id_bot, self._controller.get_team_color(), 'Stop', args=None)

    def send_tactic_stop_all(self):
        for id_bot in range(MAX_NUMBER_ROBOTS):  # TODO (pturgeon): Changer pour constante globable (ou liste?)
            self._controller.model_dataout.send_tactic(id_bot, self._controller.get_team_color(), 'Stop', args=None)

    def send_strat_stop(self):
        self._send_strategy('DoNothing')

    def toggle_show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self._controller.resize_window()

    def send_start_auto(self):
        self._controller.model_dataout.send_auto_play(True)

    def send_stop_auto(self):
        self._controller.model_dataout.send_auto_play(False)

    # noinspection PyPackageRequirements
    def _populate_play_info(self):
        self.treeWidget.clear()

        if self.play_info is None:
            return

        self.teamColorRow = QTreeWidgetItem(self.treeWidget)
        self.teamColorRow.setText(0, "Our color")
        self.teamColorRow.setText(1, self._controller.get_team_color().capitalize())

        self.refereeInfo = QTreeWidgetItem(self.treeWidget)
        self.refereeInfo.setText(0, "Referee info")
        self.refereeInfo.setExpanded(True)
        self.currentRefCommand = QTreeWidgetItem(self.refereeInfo)
        self.currentRefCommand.setText(0, "Command")
        self.currentRefCommand.setText(1, self.play_info['referee']['command'])

        self.currentGameStage = QTreeWidgetItem(self.refereeInfo)
        self.currentGameStage.setText(0, "Stage")
        self.currentGameStage.setText(1, self.play_info['referee']['stage'])

        self.stageTimeLeftItem = QTreeWidgetItem(self.refereeInfo)
        self.stageTimeLeftItem.setText(0, "Stage time left")
        self.stageTimeLeft = QTimeEdit(QTime().fromMSecsSinceStartOfDay(self.play_info['referee']['stage_time_left'] / 1000))
        self.stageTimeLeft.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.stageTimeLeft.setReadOnly(True)
        self.stageTimeLeft.setDisplayFormat("m:ss")
        self.treeWidget.setItemWidget(self.stageTimeLeftItem, 1, self.stageTimeLeft)

        
        self.autoPlayInfo = QTreeWidgetItem(self.treeWidget)
        self.autoPlayInfo.setText(0, "AutoPlay info")
        self.autoPlayInfo.setExpanded(True)
        self.autoState = QTreeWidgetItem(self.autoPlayInfo)
        self.autoState.setText(0, "State")
        self.autoState.setText(1, self.play_info['auto_play']['current_state'])

        self.currentStrategy = QTreeWidgetItem(self.autoPlayInfo)
        self.currentStrategy.setText(0, "Strategy")
        self.currentStrategy.setText(1, self.play_info['auto_play']['selected_strategy'])


        self.teamInfo = {}
        for team in ("ours", "theirs"):
            info = self.play_info["referee_team"][team]
            self.teamInfo[team] = {}
            self.teamInfo[team]["item"] = QTreeWidgetItem(self.treeWidget)
            self.teamInfo[team]["item"].setText(0, info["name"])
            self.teamInfo[team]["goalie"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["goalie"].setText(0, "Goalie ID")
            self.teamInfo[team]["goalie"].setText(1, str(info["goalie"]))
            self.teamInfo[team]["score"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["score"].setText(0, "Score")
            self.teamInfo[team]["score"].setText(1,str(info["score"]))
            self.teamInfo[team]["red_cards"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["red_cards"].setText(0, "Red cards")
            self.teamInfo[team]["red_cards"].setText(1, str(info["red_cards"]))
            self.teamInfo[team]["yellow_cards"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["yellow_cards"].setText(0, "Yellow cards")
            self.teamInfo[team]["yellow_cards"].setText(1, str(info["yellow_cards"]))
            self.teamInfo[team]["yellow_card_times_item"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["yellow_card_times_item"].setText(0, "Yellow cards time")
            if len(info["yellow_card_times"]):
                yellow_card_time = min(info["yellow_card_times"]) / 1000
            else:
                yellow_card_time = 0
            self.teamInfo[team]["yellow_card_times"] = QTimeEdit(QTime().fromMSecsSinceStartOfDay(yellow_card_time))
            self.teamInfo[team]["yellow_card_times"].setButtonSymbols(QAbstractSpinBox.NoButtons)
            self.teamInfo[team]["yellow_card_times"].setReadOnly(True)
            self.teamInfo[team]["yellow_card_times"].setDisplayFormat("m:ss")
            self.treeWidget.setItemWidget(self.teamInfo[team]["yellow_card_times_item"], 1,
                                          self.teamInfo[team]["yellow_card_times"])
            self.teamInfo[team]["timeouts"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["timeouts"].setText(0, "Timeouts")
            self.teamInfo[team]["timeouts"].setText(1, str(info["timeouts"]))
            self.teamInfo[team]["timeout_time_item"] = QTreeWidgetItem(self.teamInfo[team]["item"])
            self.teamInfo[team]["timeout_time_item"].setText(0, "Timeout time")
            self.teamInfo[team]["timeout_time"] = QTimeEdit(QTime().fromMSecsSinceStartOfDay(info["timeout_time"] / 1000))
            self.teamInfo[team]["timeout_time"].setButtonSymbols(QAbstractSpinBox.NoButtons)
            self.teamInfo[team]["timeout_time"].setReadOnly(True)
            self.teamInfo[team]["timeout_time"].setDisplayFormat("m:ss")
            self.treeWidget.setItemWidget(self.teamInfo[team]["timeout_time_item"], 1,
                                          self.teamInfo[team]["timeout_time"])
            self.teamInfo[team]["item"].setExpanded(True)

        if self._controller.get_team_color() != self._active_team:
            self._active_team = self._controller.get_team_color()
            self.teamColorRow.setText(1, self._active_team.capitalize())

        

    def update_play_info(self):
        while True:

            self.play_info = self._controller.waiting_for_play_info()

            self.page_autonomous_but_stop.setVisible(self.play_info['auto_flag'])
            self.page_autonomous_but_play.setVisible(not self.play_info['auto_flag'])



