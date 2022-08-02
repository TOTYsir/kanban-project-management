#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Yue Wang
# Created Date: 29/04/2022
# version = '1.0'
# ---------------------------------------------------------------------------
""" Preference Dialog for the Setting of Column Names and WIP limits """

# ---------------------------------------------------------------------------

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox


# ******************************************************************************

class PreferencesDialog(QDialog):
    def __init__(self, column_list, wip_limit_list, current_wip_list, blocked_flag):
        super().__init__()  # Invoke __init__ of QDialog base class

        self.column_list = column_list
        self.wip_limit_list = wip_limit_list
        self.current_wip_list = current_wip_list
        self.blocked_flag = blocked_flag

        self.resize(960, 400)
        dialog_layout = QVBoxLayout(self)

        self.preference_table = QTableWidget(2, len(column_list))

        row_headings = ["Column Name", "WIP Limit"]
        self.preference_table.setVerticalHeaderLabels(row_headings)

        for i in range(len(column_list)):
            self.preference_table.setItem(0, i, QTableWidgetItem(column_list[i]))

        # No WIP limit for to-do tasks or completed tasks, and they are not allowed to edit
        self.preference_table.setItem(1, 0, QTableWidgetItem())
        if blocked_flag == 1:
            for i in range(1, len(column_list) - 2):
                self.preference_table.setItem(1, i, QTableWidgetItem(str(wip_limit_list[i - 1])))
        else:
            for i in range(1, len(column_list) - 1):
                self.preference_table.setItem(1, i, QTableWidgetItem(str(wip_limit_list[i - 1])))

        if blocked_flag == 1:
            self.preference_table.setItem(1, self.preference_table.columnCount() - 2, QTableWidgetItem())
            self.preference_table.setItem(1, self.preference_table.columnCount() - 1, QTableWidgetItem())
            self.preference_table.item(1, self.preference_table.columnCount() - 2).setFlags(~Qt.ItemIsEditable)
            self.preference_table.item(1, self.preference_table.columnCount() - 1).setFlags(~Qt.ItemIsEditable)
            self.preference_table.item(0, self.preference_table.columnCount() - 1).setFlags(~Qt.ItemIsEditable)
        else:
            self.preference_table.setItem(1, self.preference_table.columnCount() - 1, QTableWidgetItem())
            self.preference_table.item(1, self.preference_table.columnCount() - 1).setFlags(~Qt.ItemIsEditable)

        self.preference_table.item(1, 0).setFlags(~Qt.ItemIsEditable)

        dialog_layout.addWidget(self.preference_table)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.on_confirm_action)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)

        dialog_layout.addLayout(button_layout)

        self.setLayout(dialog_layout)

    def get_column_name(self):
        """ Return a list of new column names """
        for i in range(self.preference_table.columnCount()):
            self.column_list[i] = self.preference_table.item(0, i).text()

        return self.column_list

    def get_wip_limit(self):
        """ Return a list of new WIP limits """
        if self.blocked_flag == 1:
            for i in range(1, self.preference_table.columnCount() - 2):
                self.wip_limit_list[i - 1] = int(self.preference_table.item(1, i).text())
        else:
            for i in range(1, self.preference_table.columnCount() - 1):
                self.wip_limit_list[i - 1] = int(self.preference_table.item(1, i).text())

        return self.wip_limit_list

    def on_confirm_action(self):
        """ Examine if new preferences are valid """
        illegal_flag = 0
        if self.blocked_flag == 0:
            for i in range(1, self.preference_table.columnCount() - 1):
                if illegal_flag == 0:
                    current_item = self.preference_table.item(1, i)
                    if (not current_item.text().isdigit()) or (
                            int(current_item.text()) < self.current_wip_list[i - 1]):  # Examine if input WIP is integer
                        illegal_wip_msg()
                        illegal_flag = 1

            if illegal_flag == 0:
                self.accept()

        else:
            for i in range(1, self.preference_table.columnCount() - 2):
                if illegal_flag == 0:
                    current_item = self.preference_table.item(1, i)
                    if (not current_item.text().isdigit()) or (
                            int(current_item.text()) < self.current_wip_list[i - 1]):  # Examine if input WIP is integer
                        illegal_wip_msg()
                        illegal_flag = 1

            if illegal_flag == 0:
                self.accept()

        return illegal_flag


# ******************************************************************************

def illegal_wip_msg():
    """ Report the error when trying to drag the blank item """
    invalid_msg = QMessageBox()

    invalid_msg.setText("Illegal input WIP values")
    invalid_msg.setFixedSize(400, 200)
    invalid_msg.exec()

# # Main program
# if __name__ == "__main__":
#     application = QApplication([])
#
#     # Create and show the dialog
#     preferencesDialog = PreferencesDialog(["aa", "ss", "coco", "222", "11"], [5, 5, 5], [6, 6, 6], 0)
#     preferencesDialog.show()
#
#     exit(application.exec())

# ******************************************************************************
