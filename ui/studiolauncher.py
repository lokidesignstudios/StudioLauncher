import os
import sys
import yaml
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import qdarkstyle

curr_dir = os.path.dirname(os.path.abspath(__file__))
print(curr_dir)
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

    def create_widgets(self):
        """
        Create all the widgets required for the tool here
        :return: None
        """
        self.prj_lbl = QtWidgets.QLabel('Projects')
        self.shot_lbl = QtWidgets.QLabel('Shot')
        self.task_lbl = QtWidgets.QLabel('Task')

    def create_layout(self):
        """
        Create layouts for the tool and put all the widgets in those layouts
        :return: None
        """
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)  # This sets the main_layout
        main_layout.setAlignment(QtCore.Qt.AlignTop)

        h_box1 = QtWidgets.QHBoxLayout()
        live_projects = studio_config['projects']['live']
        vbox_prj = QtWidgets.QListWidget()
        vbox_shot = QtWidgets.QVBoxLayout()
        vbox_task = QtWidgets.QVBoxLayout()
        for prj_name in live_projects:
            prj_wdg = Project(prj_name)
            vbox_prj.addWidget(self.prj_lbl)
            vbox_prj.addWidget(prj_wdg)
            print(prj_name)

        h_box1.addLayout(vbox_prj)

        main_layout.addLayout(h_box1)

    def get_shots(self):


class Project(QtWidgets.QWidget):
    """
    This Class represents Project/Job
    """
    def __init__(self, prj_name):
        super(Project, self).__init__()
        self.create_widget(prj_name)
        self.create_layout()

    def create_widget(self, prj_name):
        self.prj_name = QtWidgets.QLabel(prj_name)
        self.prj_icon = QtWidgets.QLabel(prj_name)
        self.prj_icon.setFixedSize(150, 150)
        self.icon = icons_path + '/' + prj_name + '.jpg'
        if os.path.exists(self.icon):
            self.prj_icon.setPixmap(self.icon)
        else:
            icon = icons_path + '/default.jpg'
            self.prj_icon.setPixmap(icon)

        self.prj_name.setText(prj_name)

    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.setLayout(main_layout)
        main_layout.addWidget(self.prj_icon)
        main_layout.addWidget(self.prj_name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    dialog = StudioLauncher()
    dialog.show()
    sys.exit(app.exec_())
