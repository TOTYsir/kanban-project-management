#! /usr/bin/env python3

# Example PySide6 program -- pir -- 22.3.2021; 6.4.2021

# ******************************************************************************
# Insert licence here!


# ******************************************************************************

from sys import exit

from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtWidgets import QToolBar, QStatusBar
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QBrush, QColor

from preferencesDialog import PreferencesDialog

# ******************************************************************************


class MainWindow(QMainWindow):
    """ Main window of appliaction"""

    def __init__(self):
        super().__init__()  # Invoke __init__ of QMainWindow base class

        self.setWindowTitle("EEE231 pir's Example")

        self.mainLayout = QVBoxLayout()

        # Setup menu bar & File menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.openMenuAction = self.fileMenu.addAction("&Open")
        self.openMenuAction.triggered.connect(
            self.on_open_action)    # New-style connect!
        self.fileMenu.addSeparator()
        self.quitMenuAction = self.fileMenu.addAction("&Quit")
        self.quitMenuAction.triggered.connect(self.on_quit_action)

        # Setup Tools menu
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.preferencesMenuAction = self.toolsMenu.addAction("&Preferences")
        self.preferencesMenuAction.triggered.connect(self.on_preferences_action)

        # Setup About menu
        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenuAction = self.aboutMenu.addAction("&About")
        self.aboutMenuAction.triggered.connect(self.on_about_action)

        # Create main toolbar
        self.mainToolBar = QToolBar()
        self.mainToolBar.setMovable(False)
        self.newToolButton = self.mainToolBar.addAction("New")
        self.openToolButton = self.mainToolBar.addAction("Open")
        self.openToolButton.triggered.connect(self.on_open_action)
        self.saveToolButton = self.mainToolBar.addAction("Save")
        self.saveAsToolButton = self.mainToolBar.addAction("Save As")
        self.addToolBar(self.mainToolBar)
        self.mainLayout.addWidget(self.mainToolBar)

        # Is a status bar needed in this application?
        self.statusBar = QStatusBar()
        self.mainLayout.addWidget(self.statusBar)

        # Create tabbed widget
        self.tabbedWidget = QTabWidget()
        self.tabbedWidget.currentChanged.connect(self.on_tab_changed)

        self.boardWidget_1 = QTableWidget(15, 4, self.tabbedWidget)

        # Turn off row numbering
        headerView = self.boardWidget_1.verticalHeader
        headerView().setVisible(False)

        # Set column headers
        columnHeadings = ["Backlog", "In progress", "Blocked", "Completed"]
        self.boardWidget_1.setHorizontalHeaderLabels(columnHeadings)

        # Set Kanban board title
        self.tabbedWidget.addTab(self.boardWidget_1, "my project")

        tableItem = QTableWidgetItem("feed the ferrets!")
        brushColour = QColor("lightblue")
        brush = QBrush(brushColour)
        tableItem.setBackground(brush)
        tableItem.setText("the rain in Spain falls mainly on the plain")
        tableItem.setToolTip("the rain in Spain falls mainly on the plain")
        self.boardWidget_1.setItem(0, 0, tableItem)

        self.boardWidget_2 = QTableWidget(1, 5, self.tabbedWidget)
        self.tabbedWidget.addTab(self.boardWidget_2, "dave's project")

        self.boardWidget_3 = QTableWidget(5, 5, self.tabbedWidget)
        self.tabbedWidget.addTab(self.boardWidget_3, "project X")

        self.mainLayout.addWidget(self.tabbedWidget)

        # Set mainLayout as the central widget
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        # Set attributes
        self.randomString = "my first string"

    # --------------------------------------------------------------------------

    def on_open_action(self):
        """Handler for 'Open' action"""
        fileName = QFileDialog.getOpenFileName(self, "Open File", ".", ("*.md"))
        print("opening ", fileName[0])
        return

    # --------------------------------------------------------------------------

    def on_quit_action(self):
        """Handler for 'Quit' action"""
        print("quitting application")
        self.close()
        return
    # --------------------------------------------------------------------------

    def on_preferences_action(self):
        """Handler for 'Preferences' action"""
        print("running preferences")

        # Create dialog instance
        preferencesDialog = PreferencesDialog()

        # Initialise dialog controls
        preferencesDialog.lineEditControl.setText(self.randomString)

        result = preferencesDialog.exec()
        if(result == QDialog.Accepted):
            print("You pressed OK")

            # Process updated preferences
            self.randomString = preferencesDialog.lineEditControl.text()
        else:
            print("You must have pressed Cancel")
            # Ignore any updated preferences

        return

    # --------------------------------------------------------------------------

    def on_about_action(self):
        """Handler for 'About' action"""
        QMessageBox.about(self, "About this program",
                          "Some text crediting the\npeople who wrote this")
        return

    # --------------------------------------------------------------------------

    def on_tab_changed(self):
        """Handler for currentChanged signal of tabbedWidget object"""
        print("you just changed to tab ", self.tabbedWidget.currentIndex())
        return

# ******************************************************************************


# Main program
if __name__ == "__main__":
    application = QApplication([])

    mainWindow = MainWindow()
    mainWindow.show()

    exit(application.exec())

# ******************************************************************************
