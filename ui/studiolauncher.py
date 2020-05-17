import os
import sys
import yaml
import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui

curr_dir = os.path.dirname(os.path.abspath(__file__))
print(curr_dir)
with open(curr_dir + '/../config/studio_launcher.yaml', 'r') as yaml_file:
    studio_config = yaml.load(yaml_file, Loader=yaml.FullLoader)
icons_path = '../icons'
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
        self.name_lbl = QtWidgets.QLabel('Name: ')
        self.name_le = QtWidgets.QLineEdit()
        self.all_chb = QtWidgets.QCheckBox('All')
        self.selected_chb = QtWidgets.QCheckBox('Selected')
        self.hidden_chb = QtWidgets.QCheckBox('Hidden')
        self.locked_chb = QtWidgets.QCheckBox('Locked')
        self.run_btn = QtWidgets.QPushButton('Run')

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
        for prj in live_projects:
            prj_lbl = QtWidgets.QLabel(prj)
            prj_icon = QtWidgets.QLabel(prj)
            icon = icons_path + '/' + prj + '.jpg'
            if os.path.exists(icon):
                prj_icon.setPixmap(icon)
            else:
                icon = icons_path + '/default.jpg'
                prj_icon.setPixmap(icon)

            prj_lbl.setText(prj)
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(prj_icon)
            vbox.addWidget(prj_lbl)
            h_box1.addLayout(vbox)
            print(prj)

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addWidget(self.all_chb)
        h_box2.addWidget(self.selected_chb)
        h_box2.addWidget(self.hidden_chb)
        h_box2.addWidget(self.locked_chb)

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addWidget(self.run_btn)

        main_layout.addLayout(h_box1)
        main_layout.addLayout(h_box2)
        main_layout.addLayout(h_box3)


class Project(QtWidgets.QWidget):
    def __init__(self):
        super(Project, self).__init__()
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    icon = QtGui.QIcon(icons_path + '/vfx_rnd.jpg')
    app.setWindowIcon(icon)
    dialog = StudioLauncher()
    dialog.show()
    sys.exit(app.exec_())
