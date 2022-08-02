#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ******************************************************************************
# Insert licence here!


# ******************************************************************************

"""
Created on Thu Mar 24 16:47:16 2022

pir -- %-%-2021
"""

# ******************************************************************************

from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout
from PySide6.QtWidgets import QLineEdit, QComboBox
from PySide6.QtWidgets import QDialog, QPushButton, QListWidget, QListWidgetItem, QDoubleSpinBox, QSlider

# ******************************************************************************


class PreferencesDialog(QDialog):
    """ Example modal dialog window """

    def __init__(self):
        super().__init__()  # Invoke __init__ of QDialog base class

        self.setWindowTitle("Set Preferences Dialog")

        dialogLayout = QVBoxLayout()

        # Add some random widgets to the dialog box
        layout_1 = QHBoxLayout()
        self.lineEditControl = QLineEdit(self)
        comboBoxControl = QComboBox()
        comboBoxControl.SizeAdjustPolicy(QComboBox.AdjustToContents)
        comboBoxControl.addItem("first item")
        comboBoxControl.addItem("second item")
        comboBoxControl.addItem("third item")
        layout_1.addWidget(self.lineEditControl)
        layout_1.addWidget(comboBoxControl)
        dialogLayout.addLayout(layout_1)

        # Add some more random controls...
        layout_2 = QHBoxLayout()
        listWidget = QListWidget(self)
        newItem = QListWidgetItem()
        newItem.setText("list widget item")
        listWidget.insertItem(0, newItem)
        layout_2.addWidget(listWidget)
        doubleSpinBox = QDoubleSpinBox(self)
        doubleSpinBox.setValue(23.786)
        layout_2.addWidget(doubleSpinBox)
        slider = QSlider(self)
        layout_2.addWidget(slider)
        dialogLayout.addLayout(layout_2)

        # Add 'OK' and 'Cancel' buttons
        okButton = QPushButton("OK", self)
        okButton.clicked.connect(self.accept)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(cancelButton)
        buttonLayout.addWidget(okButton)

        dialogLayout.addLayout(buttonLayout)

        self.setLayout(dialogLayout)


# ******************************************************************************

# Main program
if __name__ == "__main__":
    application = QApplication([])

    # Create and show the dialog
    preferencesDialog = PreferencesDialog()
    preferencesDialog.show()

    exit(application.exec())

# ******************************************************************************
