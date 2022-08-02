import os
from xml.dom import minidom

from PySide6.QtCore import (Slot, Qt)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QDialog, QFileDialog,
                               QMainWindow, QMessageBox,
                               QTabWidget, QToolBar,
                               QVBoxLayout, QWidget, QTableWidgetItem)

from columnNumDialog import ColumnNumDialog
from kanbanTable import KanbanTable
from preferencesDialog import PreferencesDialog
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

    def open_xml_test(self, file_name):
        file = minidom.parse(file_name)
        project = file.documentElement

        kanban_board = project.getElementsByTagName("kanban_board")[0]
        directory = kanban_board.getAttribute("directory")
        column = int(kanban_board.getAttribute("column"))
        row = int(kanban_board.getAttribute("row"))
        is_blocked = int(kanban_board.getAttribute("is_blocked"))

        if is_blocked == 0:
            open_board = KanbanTable(row, column)
        else:
            column = column - 1
            open_board = KanbanTable(row, column)
            open_board.add_blocked()

        column_name_list = []
        wip_limit_list = []
        print("The attributes of kanban_board are: ", directory, column, row, is_blocked)
        preference = kanban_board.getElementsByTagName("preference")[0]
        for i in range(column):
            column_num = "col_" + str(i+1)
            column_name = preference.getElementsByTagName(column_num)[0]
            print("The name of colmun", column_num, "is", column_name.firstChild.data)
            column_name_list.append(column_name.firstChild.data)
            print(column_name_list)

        for i in range(2, column):
            column_num = "wip_" + str(i)
            wip_limit = preference.getElementsByTagName(column_num)[0]
            wip_limit_number_with_brackets = wip_limit.firstChild.data
            wip_limit_number = int(wip_limit_number_with_brackets.replace("(", "").replace(")", ""))
            print("The wip limit", column_num, "is", wip_limit_number)
            wip_limit_list.append(wip_limit_number)
            print(wip_limit_list)

        open_board.update_preference(column_name_list, wip_limit_list)
        open_board.wip_limit_list = wip_limit_list
        # column_name_list.clear()
        # wip_limit_list.clear()

        for i in range(0, 6):  # row+1):  # Read the all tasks exist in current xml file.
            task_num = "task_" + str(i+1)
            task = kanban_board.getElementsByTagName(task_num)[0]
            print("-"*100)
            print(task.nodeName, "begins")

            name = task.getElementsByTagName("name")[0]
            if name.firstChild == None:
                pass
            else:
                print("Task name:", name.firstChild.data)

            task_row = task.getElementsByTagName("row")[0]
            if task_row.firstChild == None:
                pass
            else:
                print("Task row:", task_row.firstChild.data)

            task_column = task.getElementsByTagName("column")[0]
            if task_column.firstChild == None:
                pass
            else:
                print("Task column:", task_column.firstChild.data)

            for j in range(2, column):  # Read all drag out times existed in the current task.
                to_col_num = "to_col_" + str(j)
                to_col = task.getElementsByTagName(to_col_num)[0]
                if to_col.firstChild == None:
                    pass
                else:
                    print("The time record in column", to_col_num, ":", to_col.firstChild.data)

            person = task.getElementsByTagName("person")[0]
            if person.firstChild == None:
                pass
            else:
                print("Task person:", person.firstChild.data)

            to_blocked = task.getElementsByTagName("to_blocked")[0]
            if to_blocked.firstChild == None:
                pass
            else:
                print("Task to_blocked time:", to_blocked.firstChild.data)

            previous_state = task.getElementsByTagName("previous_state")[0]
            if previous_state.firstChild == None:
                pass
            else:
                print("Task previous_state:", previous_state.firstChild.data)
        project_name = os.path.splitext(os.path.split(file_name)[1])[0]  # Leave the actual name of the document
        self.tabbedWidget.addTab(open_board, project_name)
        self.tabbedWidget.setCurrentIndex(self.tabbedWidget.count() - 1)
        return open_board

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

        # Setup functions for Search menu

        # Setup Icons for Search menu

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

        # Setup functions for Help manu
        self.helpMenuAction.triggered.connect(self.on_help_action)
        self.aboutMenuAction.triggered.connect(self.on_about_action)

        # Setup Icons for Help manu
        helpmenu_icon = QIcon("icons/question-line.svg")
        self.helpMenuAction.setIcon(helpmenu_icon)
        helpmenu_icon1 = QIcon("icons/information-line.svg")
        self.aboutMenuAction.setIcon(helpmenu_icon1)

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

                new_xml(file_name[0], col_num)

                new_board = KanbanTable(30, col_num)
                new_board.new_column()
                # columnHeadings = []
                # columnHeadings.append("1")
                # for i in range(1, col_num - 1):
                #     columnHeadings.append(str(i + 1) + " (" + str(newBoard.wip_limit_list[i - 1]) + ")")
                # columnHeadings.append(str(col_num))
                #
                # newBoard.setHorizontalHeaderLabels(columnHeadings)

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

            open_board = self.open_xml_test(file_name[0])
            current_index = self.tabbedWidget.currentIndex()
            board_dic[project_name] = open_board
            # print(saving_cache)

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
            # if currentBoard.blocked_flag == 1:
            #     for i in range(1, col_num - 2):
            #         new_column_list[i] = new_column_list[i] + " (" + str(new_wip_list[i - 1]) + ")"
            #         # Process updated column names
            #         currentBoard.setHorizontalHeaderLabels(new_column_list)
            # else:
            #     for i in range(1, col_num - 1):
            #         new_column_list[i] = new_column_list[i] + " (" + str(new_wip_list[i - 1]) + ")"
            #         # Process updated column names
            #         currentBoard.setHorizontalHeaderLabels(new_column_list)

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


# ******************************************************************************

def new_xml(file_name, col_num):
    row_num = 30

    xml = minidom.Document()
    include = xml.createElement('project')
    xml.appendChild(include)

    info = xml.createElement('kanban_board')
    info.setAttribute('directory', file_name)
    info.setAttribute('column', str(col_num))
    info.setAttribute('row', str(row_num))
    info.setAttribute('is_blocked', '')
    include.appendChild(info)

    preference = xml.createElement('preference')
    info.appendChild(preference)  # Input name of the column

    for i in range(1, col_num + 1):
        column_name = "col_" + str(i)
        column_set = xml.createElement(column_name)
        column_set.appendChild(xml.createTextNode(""))
        preference.appendChild(column_set)
    for i in range(2, col_num):
        wip_name = "wip_" + str(i)
        wip_set = xml.createElement(wip_name)
        wip_set.appendChild(xml.createTextNode(""))
        preference.appendChild(wip_set)

    for i in range(1, row_num + 1):
        task_num = "task_" + str(i)
        task_set = xml.createElement("")
        info.appendChild(task_set)

        name = xml.createElement('name')
        name.appendChild(xml.createTextNode(""))
        task_set.appendChild(name)

        row = xml.createElement('row')
        row.appendChild(xml.createTextNode(""))
        task_set.appendChild(row)

        column = xml.createElement('column')
        column.appendChild(xml.createTextNode(""))
        task_set.appendChild(column)

        for i in range(2, col_num):
            column_name = "to_col_" + str(i)
            column_set = xml.createElement(column_name)
            column_set.appendChild(xml.createTextNode(""))
            task_set.appendChild(column_set)

        person = xml.createElement("person")
        person.appendChild(xml.createTextNode(""))
        task_set.appendChild(person)

        person = xml.createElement("previous_state")
        person.appendChild(xml.createTextNode(""))
        task_set.appendChild(person)

        person = xml.createElement("blocked")
        person.appendChild(xml.createTextNode(""))
        task_set.appendChild(person)

    f = open(file_name, 'w')
    f.write(xml.toprettyxml())
    f.close()
