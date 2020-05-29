import os
import shutil
import sys
import yaml
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import qdarkstyle

curr_dir = os.path.dirname(os.path.abspath(__file__))

with open(curr_dir + '/../config/studio_launcher.yaml', 'r') as yaml_file:
    studio_config = yaml.load(yaml_file, Loader=yaml.FullLoader)
icons_path = '../icons'
jobs_path = studio_config['jobs_path']


class TaskCreator(QtWidgets.QWidget):
    def __init__(self):
        super(TaskCreator, self).__init__()
        self.setWindowTitle('Task Creator')
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        """
        Create all the widgets required for the tool here
        :return: None
        """
        self.prj_cmb = QtWidgets.QComboBox()
        self.prj_cmb.addItems(studio_config['projects']['live'])
        self.shot_type_cmb = QtWidgets.QComboBox()
        self.shot_type_cmb.setMaximumWidth(100)
        self.shot_type_cmb.addItems(['Asset', 'Shot'])
        self.seq_le = QtWidgets.QLineEdit()
        self.seq_le.setPlaceholderText('assets')
        self.seq_le.setDisabled(True)
        self.shot_le = QtWidgets.QLineEdit()
        self.shot_le.setPlaceholderText('Enter asset name')
        self.task_chk = QtWidgets.QCheckBox('Create selected tasks')
        self.asset_type_list_wdg = QtWidgets.QListWidget()
        self.asset_type_list_wdg.addItems(studio_config['asset_type'])
        self.task_type_list_wdg = QtWidgets.QListWidget()
        self.task_type_list_wdg.addItems(studio_config['task_type'])
        self.task_type_list_wdg.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.task_type_list_wdg.setDisabled(True)
        self.create_shot_btn = QtWidgets.QPushButton('Create Shot')
        self.create_task_btn = QtWidgets.QPushButton('Create Tasks')
        self.create_task_btn.setDisabled(True)

    def create_layout(self):
        """
        Create layouts for the tool and put all the widgets in those layouts
        :return: None
        """
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)  # This sets the main_layout
        main_layout.setAlignment(QtCore.Qt.AlignTop)

        h_box1 = QtWidgets.QHBoxLayout()
        vbox_prj = QtWidgets.QVBoxLayout()
        hbox_prj = QtWidgets.QHBoxLayout()
        hbox_prj.addWidget(self.prj_cmb)
        hbox_prj.addWidget(self.shot_type_cmb)
        hbox_prj.addWidget(self.seq_le)
        hbox_prj.addWidget(self.shot_le)
        vbox_prj.addLayout(hbox_prj)
        vbox_prj.addWidget(self.asset_type_list_wdg)
        vbox_task = QtWidgets.QVBoxLayout()
        vbox_task.addWidget(self.task_chk)
        vbox_task.addWidget(self.task_type_list_wdg)
        h_box1.addLayout(vbox_prj)
        h_box1.addLayout(vbox_task)

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addWidget(self.create_shot_btn)
        h_box2.addWidget(self.create_task_btn)

        main_layout.addLayout(h_box1)
        main_layout.addLayout(h_box2)

        # Connections
        self.shot_type_cmb.currentIndexChanged.connect(self.toggle_asset_shot)
        self.create_shot_btn.clicked.connect(self.create_asset_or_shot)
        self.create_task_btn.clicked.connect(self.create_task)
        self.task_chk.clicked.connect(self.toggle_task)

    def toggle_asset_shot(self):
        if self.shot_type_cmb.currentText() == 'Shot':
            self.asset_type_list_wdg.setDisabled(True)
            self.seq_le.setPlaceholderText('Enter sequence name')
            self.seq_le.setDisabled(False)
            self.shot_le.setPlaceholderText('Enter shot number')
            self.shot_le.setDisabled(False)
        elif self.shot_type_cmb.currentText() == 'Asset':
            self.asset_type_list_wdg.setDisabled(False)
            self.seq_le.setPlaceholderText('assets')
            self.seq_le.setText('')
            self.seq_le.setDisabled(True)
            self.shot_le.setPlaceholderText('Enter asset name')

    def create_asset_or_shot(self):
        if self.shot_type_cmb.currentText() == 'Shot':
            _path = os.path.join(
                studio_config['jobs_path'],
                self.prj_cmb.currentText(),
                self.seq_le.text(),
                ''.join([self.seq_le.text(), self.shot_le.text()])
            )
            src = studio_config['show_template'] + '\\assets'
            if not os.path.exists(_path):
                shutil.copytree(src, _path)
        elif self.shot_type_cmb.currentText() == 'Asset':
            _path = os.path.join(
                studio_config['jobs_path'],
                self.prj_cmb.currentText(),
                self.seq_le.placeholderText(),
                '.'.join([self.asset_type_list_wdg.selectedItems()[0].text(), self.shot_le.text()])
            )
            src = studio_config['show_template'] + '\\assets'
            if not os.path.exists(_path):
                shutil.copytree(src, _path)

    def create_task(self):
        if not self.task_chk.isChecked():
            self.task_type_list_wdg.setDisabled(True)
            self.create_task_btn.setDisabled(True)

        if not self.task_type_list_wdg.selectedItems():
            return

        for task_item in self.task_type_list_wdg.selectedItems():
            if self.shot_type_cmb.currentText() == 'Shot':
                _path = os.path.join(
                    studio_config['jobs_path'],
                    self.prj_cmb.currentText(),
                    self.seq_le.text(),
                    ''.join([self.seq_le.text(), self.shot_le.text()]),
                    'TASKS', task_item.text()
                )
                src = studio_config['show_template'] + '\\TASKS\\' + task_item.text()
                print(src, _path)
                if not os.path.exists(_path):
                    shutil.copytree(src, _path)
            elif self.shot_type_cmb.currentText() == 'Asset':
                if not self.asset_type_list_wdg.selectedItems():
                    print('Please select asset type')
                    return
                _path = os.path.join(
                    studio_config['jobs_path'],
                    self.prj_cmb.currentText(),
                    self.seq_le.placeholderText(),
                    '.'.join([self.asset_type_list_wdg.selectedItems()[0].text(), self.shot_le.text()]),
                    'TASKS', task_item.text()
                )
                src = studio_config['show_template'] + '\\TASKS\\' + task_item.text()
                print(src, _path)
                if not os.path.exists(_path):
                    shutil.copytree(src, _path)

    def toggle_task(self):
        if self.task_chk.isChecked():
            self.task_type_list_wdg.setDisabled(False)
            self.create_task_btn.setDisabled(False)
        else:
            self.task_type_list_wdg.setDisabled(True)
            self.create_task_btn.setDisabled(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    dialog = TaskCreator()
    dialog.show()
    sys.exit(app.exec_())
