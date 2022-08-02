from PySide6.QtWidgets import QApplication, QLabel, QPushButton
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QLineEdit


# ******************************************************************************


class SettingSearchDialog(QDialog):
    def __init__(self):
        super().__init__()  # Invoke __init__ of QDialog base class

        self.search_item = None
        self.setWindowTitle("search")
        self.setMinimumSize(230, 80)




        self.nameLabel_1 = QLabel(self)
        self.nameLabel_1.setText('task: ')
        self.nameLabel_1.move(30, 10)
        self.nameLine_1 = QLineEdit(self)
        self.nameLine_1.move(150, 10)


        # line_layout_2 = QHBoxLayout()
        # self.nameLabel_2 = QLabel(self)
        # self.nameLabel_2.setText('result: ')
        # self.nameLine_2 = QLineEdit(self)
        # line_layout_2.addWidget(self.nameLabel_2)
        # line_layout_2.addWidget(self.nameLine_2)


        confirmButton = QPushButton('OK', self)
        confirmButton.clicked.connect(self.on_clicked_action)
        confirmButton.move(170, 50)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        cancelButton.move(270, 50)

    def on_clicked_action(self):
        self.search_item = self.nameLine_1.text()
        self.accept()

    def get_search(self):
        return self.search_item


# Main program
if __name__ == "__main__":
    application = QApplication([])

    # Create and show the dialog
    settingsearchDialog = SettingsearchDialog()
    settingsearchDialog.show()

    exit(application.exec())
