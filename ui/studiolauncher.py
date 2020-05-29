import os
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
print(studio_config)


class StudioLauncher(QtWidgets.QWidget):
    def __init__(self):
        super(StudioLauncher, self).__init__()
        self.setWindowTitle(studio_config['package_name'])
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)
        self.create_widgets()
        self.create_layout()
        self.get_projects()

    def create_widgets(self):
        """
        Create all the widgets required for the tool here
        :return: None
        """
        self.prj_lbl = QtWidgets.QLabel('Projects')
        self.shot_lbl = QtWidgets.QLabel('Shot')
        self.task_lbl = QtWidgets.QLabel('Task')
        self.prj_list_wdg = QtWidgets.QListWidget()
        self.seq_list_wdg = QtWidgets.QListWidget()
        self.shot_list_wdg = QtWidgets.QListWidget()
        self.task_list_wdg = QtWidgets.QListWidget()
        self.maya_btn = QtWidgets.QPushButton('Maya')
        self.nuke_btn = QtWidgets.QPushButton('Nuke')
        self.houdini_btn = QtWidgets.QPushButton('Houdini')
        self.realflow_btn = QtWidgets.QPushButton('Realflow')
        maya_icon = icons_path + '/maya.png'
        maya_icon = QtGui.QIcon(maya_icon)
        nuke_icon = icons_path + '/nuke.png'
        nuke_icon = QtGui.QIcon(nuke_icon)
        houdini_icon = icons_path + '/houdini.png'
        houdini_icon = QtGui.QIcon(houdini_icon)
        realflow_icon = icons_path + '/qube.png'
        realflow_icon = QtGui.QIcon(realflow_icon)
        self.maya_btn.setIcon(maya_icon)
        self.nuke_btn.setIcon(nuke_icon)
        self.houdini_btn.setIcon(houdini_icon)
        self.realflow_btn.setIcon(realflow_icon)

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
        vbox_prj.addWidget(QtWidgets.QLabel('Projects'))
        vbox_prj.addWidget(self.prj_list_wdg)
        h_box1.addLayout(vbox_prj)

        vbox_seq = QtWidgets.QVBoxLayout()
        vbox_seq.addWidget(QtWidgets.QLabel('Sequence'))
        vbox_seq.addWidget(self.seq_list_wdg)
        h_box1.addLayout(vbox_seq)

        vbox_shot = QtWidgets.QVBoxLayout()
        vbox_shot.addWidget(QtWidgets.QLabel('Shots'))
        vbox_shot.addWidget(self.shot_list_wdg)
        h_box1.addLayout(vbox_shot)

        vbox_task = QtWidgets.QVBoxLayout()
        vbox_task.addWidget(QtWidgets.QLabel('Tasks'))
        vbox_task.addWidget(self.task_list_wdg)
        h_box1.addLayout(vbox_task)

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addWidget(self.maya_btn)
        h_box2.addWidget(self.nuke_btn)
        h_box2.addWidget(self.houdini_btn)
        h_box2.addWidget(self.realflow_btn)

        main_layout.addLayout(h_box1)
        main_layout.addLayout(h_box2)

        # Connections
        self.prj_list_wdg.itemClicked.connect(self.get_sequence)
        self.seq_list_wdg.itemClicked.connect(self.get_shots)
        self.shot_list_wdg.itemClicked.connect(self.get_task)
        self.maya_btn.clicked.connect(self.prepare_maya_env)

    def get_projects(self):
        live_projects = studio_config['projects']['live']
        for prj_name in live_projects:
            icon = icons_path + '/' + prj_name + '.jpg'
            prj_icon = QtGui.QIcon(icon)
            prj_item = QtWidgets.QListWidgetItem(prj_icon, prj_name)
            self.prj_list_wdg.addItem(prj_item)

    def get_sequence(self):
        self.seq_list_wdg.clear()
        selected_prj = self.prj_list_wdg.selectedItems()[0]
        if selected_prj:
            seq_path = os.path.join(jobs_path, selected_prj.text())
            if os.path.exists(seq_path):
                seq_list = os.listdir(seq_path)
                self.seq_list_wdg.addItems(seq_list)
                print(seq_list)
                return seq_list

    def get_shots(self):
        self.shot_list_wdg.clear()
        selected_prj = self.prj_list_wdg.selectedItems()[0]
        selected_seq = self.seq_list_wdg.selectedItems()[0]
        if selected_seq:
            shot_path = os.path.join(jobs_path, selected_prj.text(), selected_seq.text())
            if os.path.exists(shot_path):
                shot_list = os.listdir(shot_path)
                self.shot_list_wdg.addItems(shot_list)
                print(shot_list)
                return shot_list

    def get_task(self):
        self.task_list_wdg.clear()
        selected_prj = self.prj_list_wdg.selectedItems()[0]
        selected_seq = self.seq_list_wdg.selectedItems()[0]
        selected_shot = self.shot_list_wdg.selectedItems()[0]
        if selected_shot:
            task_path = os.path.join(jobs_path, selected_prj.text(), selected_seq.text(), selected_shot.text(), 'TASK')
            print(task_path)
            if os.path.exists(task_path):
                task_list = os.listdir(task_path)
                self.task_list_wdg.addItems(task_list)
                print(task_list)
                return task_list

    def prepare_maya_env(self):
        try:
            prj_sel = self.prj_list_wdg.selectedItems()[0]
            seq_sel = self.seq_list_wdg.selectedItems()[0]
            shot_sel = self.shot_list_wdg.selectedItems()[0]
            task_sel = self.task_list_wdg.selectedItems()[0]
            maya_prj_path = os.path.join(jobs_path, prj_sel.text(),
                                         seq_sel.text(), shot_sel.text(),
                                         task_sel.text(), 'maya')
            if os.path.exists(maya_prj_path):
                os.environ['MAYA_PROJECT'] = maya_prj_path
        except IndexError as e:
            print('No Seq, Shot or Task is selected:', e)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    dialog = StudioLauncher()
    dialog.show()
    sys.exit(app.exec_())
