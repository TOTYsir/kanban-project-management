#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Yue Wang
# Created Date: 04/05/2022
# version = '1.0'
# ---------------------------------------------------------------------------
""" Preference Dialog for the Setting of Column Names and WIP limits """

# ---------------------------------------------------------------------------

from PySide6 import QtGui
from PySide6.QtCore import QRegularExpression
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QLineEdit


# ******************************************************************************


class ColumnNumDialog(QDialog):

    def __init__(self, col_num=0):
        super().__init__()  # Invoke __init__ of QDialog base class

        self.col_num = col_num

        dialog_layout = QVBoxLayout()

        line_layout = QHBoxLayout()

        self.setWindowTitle("Setting Column Numbers")
        self.setMinimumSize(230, 80)

        self.columnLabel_1 = QLabel(self)
        self.columnLabel_1.setText('Column numbers: ')
        self.columnLine = QLineEdit(self)

        # Restrict the input of column numbers
        regexp = QRegularExpression('^[1-9][0-9]*$')  # Regular expression for >0 integers
        validator = QtGui.QRegularExpressionValidator(regexp)
        self.columnLine.setValidator(validator)

        line_layout.addWidget(self.columnLabel_1)
        line_layout.addWidget(self.columnLine)

        dialog_layout.addLayout(line_layout)

        confirm_button = QPushButton('OK', self)
        confirm_button.clicked.connect(self.on_clicked_action)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(confirm_button)

        dialog_layout.addLayout(button_layout)

        self.setLayout(dialog_layout)

    def on_clicked_action(self):
        """ Record the number of columns when clicking OK """
        self.col_num = self.columnLine.text()
        if int(self.col_num) >= 3:
            self.accept()
        else:
            self.invalid_msg()

    def get_col_num(self):
        """ Return the input value of column numbers """
        return int(self.col_num)

    def invalid_msg(self):
        """ Report the error when trying to drag the blank item """
        QMessageBox.warning(self, "Invalid value", "The number of columns cannot be smaller than 3", QMessageBox.Ok)


# Main program
if __name__ == "__main__":
    application = QApplication([])

    # Create and show the dialog
    columnNumDialog = ColumnNumDialog()
    columnNumDialog.show()

    exit(application.exec())
