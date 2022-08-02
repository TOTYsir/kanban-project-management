from PySide6.QtWidgets import (QApplication, QDialog, QPushButton,
                               QLabel)


class CloseSavingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Save File...")
        self.setFixedSize(400, 100)

        self.promptLabel = QLabel(self)
        self.promptLabel.setText("File Untitle is Modified...\nDo you want to save the changes?")
        self.promptLabel.move(10, 10)

        saveButton = QPushButton('Save', self)
        saveButton.clicked.connect(self.accept)
        saveButton.move(150, 60)
        discardButton = QPushButton('Discard', self)
        discardButton.clicked.connect(self.reject)
        discardButton.move(230, 60)
        # cancelButton = QPushButton('Cancel', self)
        # cancelButton.clicked.connect(self.cancel_action)
        # cancelButton.move(310, 60)


if __name__ == "__main__":
    application = QApplication([])

    # Create and show the dialog
    settingCloseSavingDialog = CloseSavingDialog()
    settingCloseSavingDialog.show()

    exit(application.exec())
