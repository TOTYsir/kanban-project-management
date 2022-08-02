import os

from PySide6.QtCore import (Slot, Qt)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QDialog, QFileDialog,
                               QMainWindow, QMessageBox,
                               QTabWidget, QToolBar,
                               QVBoxLayout, QWidget)

from columnNumDialog import ColumnNumDialog
from kanbanTable import KanbanTable
from preferencesDialog import PreferencesDialog
from settingSearchDialog import SettingSearchDialog
# ******************************************************************************
from xmlHandler import XmlHandler

board_dic = {}
saving_cache = {}  # Used for memorising the saving location


class MainWindow(QMainWindow):
    """ Main window of application"""

    def __init__(self):
        super().__init__()  # Invoke __init__ of QMainWindow base class

        self.setWindowTitle("Kanban Project Management")
        self.setGeometry(100, 100, 1080, 600)

        self.setup()

    def setup(self):
        self.mainLayout = QVBoxLayout()

        # Setup menu bar & File menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.newMenuAction = self.fileMenu.addAction("&New File...")
        self.openMenuAction = self.fileMenu.addAction("&Open File...")
        self.saveMenuAction = self.fileMenu.addAction("&Save File...")
        self.saveasMenuAction = self.fileMenu.addAction("&Save As...")
        self.fileMenu.addSeparator()
        self.quitMenuAction = self.fileMenu.addAction("&Quit")

        # Setup functions for File manu
        self.newMenuAction.triggered.connect(self.on_new_action)
        self.openMenuAction.triggered.connect(self.on_open_action)  # Connect method with the action
        self.saveMenuAction.triggered.connect(self.on_save_action)
        self.saveasMenuAction.triggered.connect(self.on_save_as_action)
        self.quitMenuAction.triggered.connect(self.on_quit_action)

        # Setup Icons for File manu
        filemenu_icon = QIcon("icons/file-add-line.svg")
        self.newMenuAction.setIcon(filemenu_icon)
        filemenu_icon1 = QIcon("icons/folder-open-fill.svg")
        self.openMenuAction.setIcon(filemenu_icon1)
        filemenu_icon2 = QIcon("icons/save-line.svg")
        self.saveMenuAction.setIcon(filemenu_icon2)
        filemenu_icon3 = QIcon("icons/save-2-line.svg")
        self.saveasMenuAction.setIcon(filemenu_icon3)
        filemenu_icon4 = QIcon("icons/close-line.svg")
        self.quitMenuAction.setIcon(filemenu_icon4)

        # Setup menu bar & Search menu
        self.searchMenu = self.menuBar().addMenu("&Search")
        self.searchMenuAction = self.searchMenu.addAction("&task")
        # Setup functions for Search menu
        self.searchMenuAction.triggered.connect(self.on_search_action)
        # Setup Icons for Search menu
        searchmenu_icon = QIcon("icons/question-line.svg")
        self.searchMenuAction.setIcon(searchmenu_icon)
        # Setup menu bar & Tools menu
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.preferencesMenuAction = self.toolsMenu.addAction("&Preferences")
        self.addBlockedAction = self.toolsMenu.addAction("&Add Blocked Column")

        self.preferencesMenuAction.triggered.connect(self.on_preferences_action)
        self.addBlockedAction.triggered.connect(self.on_add_blocked_action)

        # Setup Help menu
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenuAction = self.helpMenu.addAction("&Help")
        self.aboutMenuAction = self.helpMenu.addAction("&About")
        self.reportAction = self.helpMenu.addAction("&Report Bug")

        # Setup functions for Help manu
        self.helpMenuAction.triggered.connect(self.on_help_action)
        self.aboutMenuAction.triggered.connect(self.on_about_action)
        self.reportAction.triggered.connect(self.on_report_action)

        # Setup Icons for Help manu
        helpmenu_icon = QIcon("icons/question-line.svg")
        self.helpMenuAction.setIcon(helpmenu_icon)
        helpmenu_icon1 = QIcon("icons/information-line.svg")
        self.aboutMenuAction.setIcon(helpmenu_icon1)
        helpmenu_icon2 = QIcon("icons/error-warning-line.svg")
        self.reportAction.setIcon(helpmenu_icon2)

        # Create main toolbar
        self.mainToolBar = QToolBar()
        self.mainToolBar.setMovable(False)

        self.newToolButton = self.mainToolBar.addAction("New")
        self.openToolButton = self.mainToolBar.addAction("Open")
        self.saveToolButton = self.mainToolBar.addAction("Save")
        self.saveAsToolButton = self.mainToolBar.addAction("Save As")
        self.addToolBar(self.mainToolBar)
        self.mainLayout.addWidget(self.mainToolBar)

        # Create Function of main toolbar
        self.newToolButton.triggered.connect(self.on_new_action)
        self.openToolButton.triggered.connect(self.on_open_action)
        self.saveToolButton.triggered.connect(self.on_save_action)
        self.saveAsToolButton.triggered.connect(self.on_save_as_action)

        # Create Icons of main toolbar
        toolbar_icon = QIcon("icons/file-add-line.svg")
        self.newToolButton.setIcon(toolbar_icon)
        toolbar_icon1 = QIcon("icons/folder-open-line.svg")
        self.openToolButton.setIcon(toolbar_icon1)
        toolbar_icon2 = QIcon("icons/save-line.svg")
        self.saveToolButton.setIcon(toolbar_icon2)
        toolbar_icon3 = QIcon("icons/save-2-line.svg")
        self.saveAsToolButton.setIcon(toolbar_icon3)

        # Create tabbed widget
        self.tabbedWidget = QTabWidget()
        self.tabbedWidget.setObjectName(u"tabWidget")
        self.tabbedWidget.setDocumentMode(True)
        self.tabbedWidget.setTabsClosable(True)
        self.tabbedWidget.setMovable(True)
        self.tabbedWidget.currentChanged.connect(self.on_tab_changed)
        self.tabbedWidget.tabCloseRequested.connect(self.close_tab_action)

        self.mainLayout.addWidget(self.tabbedWidget)

        # Set mainLayout as the central widget
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Alert", "Are you sure to close the application?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # --------------------------------------------------------------------------

    @Slot()  # a decorator that identifies a function as a slot
    def on_new_action(self):
        """Handler for 'New' action"""
        file_name = QFileDialog.getSaveFileName(self, "New File", ".", "XML files (*.xml)")
        if file_name[1]:  # If the user clicks on cancel, the following code will no longer be executed.
            print(file_name)
            project_name = os.path.splitext(os.path.split(file_name[0])[1])[0]  # Leave the actual name of the document
            saving_cache[project_name] = file_name[0]
            print("new ", file_name[0])

            column_num_dialog = ColumnNumDialog()
            result = column_num_dialog.exec()
            if result == QDialog.Accepted:
                col_num = column_num_dialog.get_col_num()
                print(col_num)

                new_board = KanbanTable(30, col_num)
                new_board.new_column()

                board_dic[project_name] = new_board

                self.tabbedWidget.addTab(new_board, project_name)
                self.tabbedWidget.setCurrentIndex(self.tabbedWidget.count() - 1)
        return

    # --------------------------------------------------------------------------
    @Slot()  # a decorator that identifies a function as a slot
    def on_open_action(self):
        """Handler for 'Open' action"""
        file_name = QFileDialog.getOpenFileName(self, "Open File", ".", "XML files (*.xml)")
        if file_name[1]:  # If the user clicks on cancel, the following code will no longer be executed.
            print("opening ", file_name[0])
            project_name = os.path.splitext(os.path.split(file_name[0])[1])[0]
            saving_cache[project_name] = file_name[0]

            xml_handler = XmlHandler()
            open_board = xml_handler.open_xml(file_name[0])

            print(project_name)

            self.tabbedWidget.addTab(open_board, project_name)
            board_dic[project_name] = open_board

            print(board_dic)

        return

    # --------------------------------------------------------------------------
    @Slot()  # a decorator that identifies a function as a slot
    def on_save_action(self):
        """Handler for 'Save' action"""
        current_index = self.tabbedWidget.currentIndex()
        file_name = saving_cache[self.tabbedWidget.tabText(current_index)]
        saving_board = board_dic[self.tabbedWidget.tabText(current_index)]
        saving_board.update_task()
        xml_handler = XmlHandler()
        xml_handler.create_xml(file_name, saving_board)
        return

    # --------------------------------------------------------------------------
    @Slot()  # a decorator that identifies a function as a slot
    def on_save_as_action(self):
        """Handler for 'Save As' action"""
        current_index = self.tabbedWidget.currentIndex()
        saving_board = board_dic[self.tabbedWidget.tabText(current_index)]
        file_name = QFileDialog.getSaveFileName(self, "Save As", ".", "XML files (*.xml)")
        if file_name[1]:  # If the user clicks on cancel, the following code will no longer be executed.
            print("saving as ", file_name[0])
            saving_board.update_task()
            xml_handler = XmlHandler()
            xml_handler.create_xml(file_name[0], saving_board)

        return

    # --------------------------------------------------------------------------
    @Slot()
    def on_quit_action(self):
        """Handler for 'Quit' action"""
        print("quitting application")
        self.close()
        return

    # --------------------------------------------------------------------------
    @Slot()
    def on_preferences_action(self):
        """Handler for 'Preferences' action"""
        print("running preferences")

        current_list = []
        current_index = self.tabbedWidget.currentIndex()
        current_board = board_dic[self.tabbedWidget.tabText(current_index)]

        column_list = current_board.get_column()

        for i in range(1, current_board.columnCount() - 1):
            current_list.append(current_board.check_column(i))

        preferences_dialog = PreferencesDialog(column_list, current_board.wip_limit_list, current_list,
                                               current_board.blocked_flag)

        result = preferences_dialog.exec()

        if result == QDialog.Accepted:
            print("You pressed OK")
            new_column_list = preferences_dialog.get_column_name()
            print(new_column_list)

            new_wip_list = preferences_dialog.get_wip_limit()
            print(new_wip_list)

            current_board.update_preference(new_column_list, new_wip_list)

        else:
            print("You must have pressed Cancel")  # Ignore any updated preferences

        return

    @Slot()
    def on_add_blocked_action(self):
        current_index = self.tabbedWidget.currentIndex()
        current_board = board_dic[self.tabbedWidget.tabText(current_index)]

        if current_board.blocked_flag == 0:
            current_board.add_blocked()
        else:
            invalid_msg = QMessageBox()
            invalid_msg.setText("Blocked column has been existed")
            invalid_msg.exec()
        # new_header = QTableWidgetItem()
        # new_header.setText("Blocked")
        # currentBoard.horizontalHeaderItem(currentBoard.columnCount())

        # currentBoard.setHorizontalHeaderItem(currentBoard.columnCount() - 1, new_header)

    # --------------------------------------------------------------------------
    @Slot()
    def on_help_action(self):
        """Handler for 'Help' action"""
        msg_box = QMessageBox()
        msg_box.setTextFormat(Qt.RichText)  # this is what makes the links clickable
        msg_box.setText("<a href='https://github.com/pirlite2/EEE231-group-4'>Github</a>")
        msg_box.setWindowTitle("Help")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    @Slot()
    def on_about_action(self):
        """Handler for 'About' action"""

        QMessageBox.about(self, "About this program",
                          "Kanban Project Management (version 1.0.0)")
        return

    @Slot()
    def on_report_action(self):
        """Handler for 'Report Bug' action"""

        report_msg = QMessageBox()
        report_msg.setTextFormat(Qt.RichText)
        report_msg.setText("<a href='https://github.com/pirlite2/EEE231-group-4'>https://github.com/pirlite2/EEE231-group-4</a>")
        report_msg.setWindowTitle("Report Bug of this Program")
        report_msg.setStandardButtons(QMessageBox.Ok)
        report_msg.exec()

        return

    # --------------------------------------------------------------------------
    @Slot()
    def on_tab_changed(self):
        """Handler for currentChanged signal of tabbedWidget object"""
        print("you just changed to tab ", self.tabbedWidget.currentIndex())
        return

    # --------------------------------------------------------------------------
    @Slot()
    def close_tab_action(self, tab_index):
        """A message dialog to prompt the user to save the modified file before closing."""
        reply = QMessageBox.question(self, "Save file before close",
                                     "The file is modified.\nDo you want to save the changes?",
                                     QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if reply == QMessageBox.Save:
            self.on_save_action()
            self.tabbedWidget.removeTab(tab_index)
        elif reply == QMessageBox.Discard:
            self.tabbedWidget.removeTab(tab_index)
        else:
            pass

    @Slot()
    def on_search_action(self, ):
        settingsearch_dialog = SettingSearchDialog()
        settingsearch_dialog.exec()

        search = settingsearch_dialog.get_search()
        current_index = self.tabbedWidget.currentIndex()

        current_board = board_dic[self.tabbedWidget.tabText(current_index)]
        current_board.update_task()
        task_list = current_board.task_list
        search_flag = 0

        for i in range(len(task_list)):
            task = task_list[i]
            if task.name is not None:
                if task.name == search:
                    search_flag = 1
                    result_msg = QMessageBox()
                    result_msg.setWindowTitle("result")
                    result_msg.setText(" row:" + str(task.row + 1) + "   column:" + str(task.column + 1))
                    result_msg.exec()
                    break

        if search_flag == 0:
            result_msg = QMessageBox()
            result_msg.setWindowTitle("result")
            result_msg.setText("no match content")
            result_msg.exec()

# def new_xml(file_name, col_num):
#     row_num = 30
#
#     xml = minidom.Document()
#     include = xml.createElement('project')
#     xml.appendChild(include)
#
#     info = xml.createElement('kanban_board')
#     info.setAttribute('directory', file_name)
#     info.setAttribute('column', str(col_num))
#     info.setAttribute('row', str(row_num))
#     info.setAttribute('is_blocked', '')
#     include.appendChild(info)
#
#     preference = xml.createElement('preference')
#     info.appendChild(preference)  # Input name of the column
#
#     for i in range(1, col_num + 1):
#         column_name = "col_" + str(i)
#         column_set = xml.createElement(column_name)
#         column_set.appendChild(xml.createTextNode(""))
#         preference.appendChild(column_set)
#     for i in range(2, col_num):
#         wip_name = "wip_" + str(i)
#         wip_set = xml.createElement(wip_name)
#         wip_set.appendChild(xml.createTextNode(""))
#         preference.appendChild(wip_set)
#
#     for i in range(1, row_num + 1):
#         task_num = "task_" + str(i)
#         task_set = xml.createElement("")
#         info.appendChild(task_set)
#
#         name = xml.createElement('name')
#         name.appendChild(xml.createTextNode(""))
#         task_set.appendChild(name)
#
#         row = xml.createElement('row')
#         row.appendChild(xml.createTextNode(""))
#         task_set.appendChild(row)
#
#         column = xml.createElement('column')
#         column.appendChild(xml.createTextNode(""))
#         task_set.appendChild(column)
#
#         for i in range(2, col_num):
#             column_name = "to_col_" + str(i)
#             column_set = xml.createElement(column_name)
#             column_set.appendChild(xml.createTextNode(""))
#             task_set.appendChild(column_set)
#
#         person = xml.createElement("person")
#         person.appendChild(xml.createTextNode(""))
#         task_set.appendChild(person)
#
#         person = xml.createElement("previous_state")
#         person.appendChild(xml.createTextNode(""))
#         task_set.appendChild(person)
#
#         person = xml.createElement("blocked")
#         person.appendChild(xml.createTextNode(""))
#         task_set.appendChild(person)
#
#     f = open(file_name, 'w')
#     f.write(xml.toprettyxml())
#     f.close()
