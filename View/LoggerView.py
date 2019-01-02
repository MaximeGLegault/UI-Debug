# Under MIT License, see LICENSE.txt

from PyQt5.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QVBoxLayout, \
                            QPushButton, QGroupBox, QCheckBox, QMessageBox, \
                            QFileDialog
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QMutex
from PyQt5.QtCore import QMutexLocker

from PyQt5.QtCore import QSize

from Model.DataInModel import DataInModel

__author__ = 'RoboCupULaval'


# noinspection PyArgumentList,PyUnresolvedReferences
class LoggerView(QWidget):
    def __init__(self, parent, controller):
        QWidget.__init__(self, parent)
        self._controller = controller

        self._queue_string_log = []

        self._model = None
        self._count = 0
        self._max_logger_line = 10
        self.pause = False

        # Mutex
        self._mutex = QMutex()

        # Timer
        self._timer_update = QTimer()
        self._timer_update.timeout.connect(self.update_logger)
        self._timer_update.start(100)

        self._widget_logger = QTextEdit(self)
        self.filter_crit = QCheckBox('Critical')
        self.filter_err = QCheckBox('Error')
        self.filter_warn = QCheckBox('Warning')
        self.filter_info = QCheckBox('Info')
        self.filter_debug = QCheckBox('Debug')
        self.btn_clear = QPushButton()
        self.btn_save = QPushButton()
        self.btn_refresh_data = QPushButton()
        self.btn_media_ctrl = QPushButton()
        self.init_ui()

    def update_logger(self):
        if not self.pause:
            try:
                QMutexLocker(self._mutex).relock()
                display_msg = self._queue_string_log + self._widget_logger.toPlainText().splitlines()
                self._widget_logger.setPlainText('\n'.join(display_msg[:self._max_logger_line]))
                self._queue_string_log.clear()
            finally:
                QMutexLocker(self._mutex).unlock()

    def init_ui(self):
        self._widget_logger.setReadOnly(True)
        layout = QHBoxLayout()

        layout_ctrl = QVBoxLayout()

        group_box = QGroupBox('Filtre')
        layout_filter = QVBoxLayout()
        layout_filter.setContentsMargins(0, 0, 0, 0)
        group_box.setLayout(layout_filter)
        self.filter_debug.setChecked(True)
        self.filter_info .setChecked(True)
        self.filter_warn.setChecked(True)
        self.filter_err.setChecked(True)
        self.filter_crit.setChecked(True)
        layout_filter.addWidget(self.filter_debug)
        layout_filter.addWidget(self.filter_info)
        layout_filter.addWidget(self.filter_warn)
        layout_filter.addWidget(self.filter_err)
        layout_filter.addWidget(self.filter_crit)
        layout_ctrl.addWidget(group_box)

        layout_btn = QHBoxLayout()
        self.btn_media_ctrl.setIcon(QIcon('Img/control_pause.png'))
        self.btn_media_ctrl.setIconSize(QSize(16, 16))
        self.btn_media_ctrl.setToolTip('Lecture/Pause')
        self.btn_media_ctrl.clicked.connect(self.pause_event)
        layout_btn.addWidget(self.btn_media_ctrl)

        self.btn_refresh_data.setIcon(QIcon('Img/database_refresh.png'))
        self.btn_refresh_data.setIconSize(QSize(16, 16))
        self.btn_refresh_data.setToolTip('Recharger tout')
        self.btn_refresh_data.setDisabled(True)
        self.btn_refresh_data.clicked.connect(self.reload_all_database)
        layout_btn.addWidget(self.btn_refresh_data)

        self.btn_save.setIcon(QIcon('Img/disk.png'))
        self.btn_save.setIconSize(QSize(16, 16))
        self.btn_save.setToolTip('Sauvegarder')
        self.btn_save.setDisabled(True)
        self.btn_save.clicked.connect(self.save)
        layout_btn.addWidget(self.btn_save)
        layout_ctrl.addLayout(layout_btn)

        self.btn_clear.setIcon(QIcon('Img/table_delete.png'))
        self.btn_clear.setIconSize(QSize(16, 16))
        self.btn_clear.setToolTip('Effacer')
        self.btn_clear.setDisabled(True)
        self.btn_clear.clicked.connect(self.clear)
        layout_btn.addWidget(self.btn_clear)

        # Initialisation Layout
        layout.addLayout(layout_ctrl)
        layout.addWidget(self._widget_logger)

        self.setLayout(layout)
        self.hide()

    def pause_event(self):
        self.pause = not self.pause
        if self.pause:
            self.btn_media_ctrl.setIcon(QIcon('Img/control_play.png'))
            self.btn_refresh_data.setDisabled(False)
            self.btn_clear.setDisabled(False)
            self.btn_save.setDisabled(False)
        else:
            self.btn_media_ctrl.setIcon(QIcon('Img/control_pause.png'))
            self.btn_clear.setDisabled(True)
            self.btn_refresh_data.setDisabled(True)
            self.btn_save.setDisabled(True)
            self.update()

    def reload_all_database(self):
        try:
            QMutexLocker(self._mutex).relock()
            if self._model is not None:
                messages = self._model.get_last_log(0)
                if messages is not None:
                    messages = list(filter(self._filter_with_checkbox, messages))
                    self._widget_logger.setPlainText('\n'.join(map(str, messages[::-1])))
        finally:
            QMutexLocker(self._mutex).unlock()

    def _filter_with_checkbox(self, logging):
        link_level_checkbox = {1: self.filter_debug,
                               2: self.filter_info,
                               3: self.filter_warn,
                               4: self.filter_err,
                               5: self.filter_crit}
        # noinspection PyBroadException
        try:
            if link_level_checkbox[logging.data['level']].isChecked():
                return True
            return False
        except Exception:
            return False

    def set_model(self, model):
        if isinstance(model, DataInModel):
            self._model = model
        else:
            raise TypeError('Logger should get data in model argument.')

    def refresh(self):
        if not self.pause:
            try:
                QMutexLocker(self._mutex).relock()
                if self._model is not None:
                    messages = self._model.get_last_log(self._count)
                    if messages is not None:
                        self._count += len(messages)
                        for msg in messages:
                            self._queue_string_log.append(str(msg))
            finally:
                QMutexLocker(self._mutex).unlock()

    def get_count(self):
        return self._count

    def clear(self):
        # noinspection PyCallByClass
        reply = QMessageBox.question(self, 'Suppression de la fil', 'Êtes-vous sûr de vouloir effacer la fil de'
                                     ' logging ?  ', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._widget_logger.clear()

    def save(self):
        # noinspection PyCallByClass
        path = QFileDialog.getSaveFileName(self, 'Enregistrer sous', '', '.txt')
        self._controller.write_logging_file(path, self._widget_logger.toPlainText())

    def show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self._controller.resize_window()
