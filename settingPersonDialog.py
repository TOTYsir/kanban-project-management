#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Yue Wang
# Created Date: 21/04/2021
# version = '1.0'
# ---------------------------------------------------------------------------
""" Person Dialog for Recording the Name of Person Who is Responsible for It """

# ---------------------------------------------------------------------------

from PySide6.QtWidgets import QApplication, QLabel, QPushButton
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QLineEdit


# ******************************************************************************


class SettingPersonDialog(QDialog):
    def __init__(self, current_person="", person_name=""):
        super().__init__()  # Invoke __init__ of QDialog base class

        self.current_person = current_person
        self.person_name = person_name

        self.setWindowTitle("Person Name Setting")
        self.setMinimumSize(230, 80)

        self.nameLabel_1 = QLabel(self)
        self.nameLabel_1.setText('Person Name: ')
        self.nameLabel_1.move(30, 10)
        self.nameLine = QLineEdit(self)
        self.nameLine.move(150, 10)

        confirm_button = QPushButton('OK', self)
        confirm_button.clicked.connect(self.on_clicked_action)
        confirm_button.move(170, 50)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.on_reject_action)
        cancel_button.move(270, 50)

    def on_clicked_action(self):
        """ Record the person name when clicking OK """
        self.person_name = self.nameLine.text()
        print(self.person_name)
        self.accept()

    def on_reject_action(self):
        """ Keep the person name when clicking Cancel """
        self.person_name = self.current_person
        self.reject()

    def closeEvent(self, event):
        """ Keep the person name when directly closing the dialog """
        self.person_name = self.current_person
        self.reject()


# Main program
if __name__ == "__main__":
    application = QApplication([])

    # Create and show the dialog
    settingPersonDialog = SettingPersonDialog()
    settingPersonDialog.show()

    exit(application.exec())

# ******************************************************************************
