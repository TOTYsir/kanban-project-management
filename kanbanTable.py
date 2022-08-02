#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Yue Wang
# Created Date: 03/04/2022
# version = '2.0'
# ---------------------------------------------------------------------------
""" Kanban board for Kanban Project Management Application """

# ---------------------------------------------------------------------------

import time

from PySide6.QtCore import Qt
from PySide6.QtGui import QDropEvent, QDragEnterEvent
from PySide6.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QMessageBox, QMenu

from settingPersonDialog import SettingPersonDialog
# ---------------------------------------------------------------------------
from task import Task

drag_pos = []
drop_pos = []


class KanbanTable(QTableWidget):
    def __init__(self, rows, columns, blocked_flag=0):
        super().__init__(rows, columns)

        self.blocked_flag = blocked_flag

        self.task_list = []
        self.wip_limit_list = [5 for i in range(self.columnCount() - 2)]

        # Initialise the task list of the KanbanTable
        for i in range(self.rowCount()):
            task = Task(None, self.columnCount())
            self.task_list.append(task)

        print(self.task_list)

        self.cellDoubleClicked.connect(self.on_double_click_action)

        # Specify the setting of drag and drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        # Specify the setting of selection mode
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setDragDropMode(QAbstractItemView.InternalMove)  # Accept move (not copy) operations only from itself

        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Redefine the right click
        self.customContextMenuRequested.connect(self.right_clicked_menu)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """ Record the starting point of the drag operation """
        drag_pos.clear()
        drop_pos.clear()

        event.accept()

        drag_pos.append(event.pos().x())
        drag_pos.append(event.pos().y())
        print(drag_pos)

    def dropEvent(self, event: QDropEvent):
        """ Restrict the drop operation due to the mechanism of the Kanban Project """
        selected_item = self.currentItem()
        selected_row = self.currentRow()
        selected_col = self.currentColumn()

        drop_pos.append(event.pos().x())
        drop_pos.append(event.pos().y())
        print(drop_pos)
        direction = self.move_direction()
        print(direction)
        # print(self.check_column(selected_col))
        # print(self.check_wip(selected_col, direction))
        # print(self.time_list)

        if direction == 0:  # Not allowed to move
            if self.currentItem() is None:
                blank_msg()
            else:
                selected_content = selected_item.text()
                if len(selected_content) == 0:
                    blank_msg()

                else:
                    selected_content = selected_item.text()
                    current_task = self.task_list[selected_row]
                    current_task.name = selected_content
                    current_task.column = selected_col
                    self.setItem(selected_row, selected_col, QTableWidgetItem(current_task.name))

        else:
            if self.currentItem() is not None:
                selected_content = selected_item.text()
                print(selected_content)

                if len(selected_content) != 0:
                    if direction == 1:  # Right move
                        if self.check_wip(selected_col, direction):
                            self.setItem(selected_row, selected_col,
                                         QTableWidgetItem(None))
                            current_task = self.task_list[selected_row]
                            current_task.name = selected_content
                            print(current_task.name)
                            current_task.column = selected_col + 1
                            current_task.time_list[selected_col] = time.asctime(time.localtime(time.time()))
                            self.setItem(selected_row, selected_col + 1, QTableWidgetItem(current_task.name))
                        else:
                            wip_msg()

                    if direction == -1:  # Left move
                        if self.check_wip(selected_col, direction):
                            self.setItem(selected_row, selected_col,
                                         QTableWidgetItem(None))  # Clear the content of the initial item
                            current_task = self.task_list[selected_row]
                            current_task.name = selected_content
                            print(current_task.name)
                            current_task.column = selected_col - 1

                            for i in range(selected_col):
                                # if i == selected_col - 2:
                                #     current_task.time_list[i] = time.asctime(time.localtime(time.time()))
                                if i > selected_col - 2:  # Clear the record in the following state
                                    current_task.time_list[i] = ''

                            self.setItem(selected_row, selected_col - 1, QTableWidgetItem(current_task.name))
                        else:
                            wip_msg()
                else:
                    blank_msg()

            else:
                blank_msg()

    def move_direction(self):
        """ Return the destination of the drop operation """
        selected_col = self.currentColumn()
        if selected_col == self.columnCount() - 1 and self.blocked_flag == 1:
            return 0
        # First consider those items not in the last column
        if (selected_col < self.columnCount() - 1 and self.blocked_flag == 0) or (
                selected_col < self.columnCount() - 2 and self.blocked_flag == 1):
            if abs(drop_pos[1] - drag_pos[1]) < 15:  # Compare the y-values to restrict up and down drag and drop
                if drag_pos[0] < drop_pos[0]:  # Compare the x-values
                    return 1  # Right
                elif drag_pos[0] > drop_pos[0]:
                    return -1  # Left
                else:
                    return 0  # Cannot move
            else:
                return 0
        # Consider the item in the last column
        else:
            if self.blocked_flag == 0:
                if abs(drop_pos[1] - drag_pos[1]) < 15 and drag_pos[0] > drop_pos[0]:
                    return -1
                else:
                    return 0
            else:
                if abs(drop_pos[1] - drag_pos[1]) < 15 and drag_pos[0] > drop_pos[0]:
                    return -1
                else:
                    return 0

    def right_clicked_menu(self, pos):
        """ Right-clicked menu of the view in Kanban board """
        menu = QMenu()

        item_1 = menu.addAction("Mark the task as Blocked")
        item_2 = menu.addAction("Remove the task from Blocked")
        item_3 = menu.addAction("Person Settings")
        item_4 = menu.addAction("Details")
        item_5 = menu.addAction("Insert Row")
        item_6 = menu.addAction("Delete Row")
        action = menu.exec(self.mapToGlobal(pos))

        sel_row = self.currentRow()

        if action == item_1:  # Add to Blocked
            self.add_to_blocked(sel_row)

        if action == item_2:  # Release the task from Blocked
            self.remove_from_blocked(sel_row)

        if action == item_3:  # Person name settings
            self.person_setting(sel_row)

        if action == item_4:  # Detailed information about the task in the selected row
            self.detail_msg()

        if action == item_5:  # Insert a row
            self.insert_row(sel_row)

        if action == item_6:  # Delete a row
            self.delete_row(sel_row)

    def on_double_click_action(self):
        """ Restrict the edit operation """
        selected_row = self.currentRow()
        selected_col = self.currentColumn()
        selected_item = self.currentItem()

        if selected_col == 0:  # the selected item is in the first column
            flag = 0  # Figure out if the selected column consists of the task
            for i in range(1, self.columnCount()):
                item = self.item(selected_row, i)
                if item is not None:
                    content = item.text()
                    if len(content) != 0:
                        flag = 1
                        break
            if flag:  # already had an item in the row
                self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # The edit operation is not allowed
            else:
                self.setEditTriggers(
                    QAbstractItemView.DoubleClicked)  # The edit operation is allowed

        else:
            if self.currentItem() is None:
                self.setEditTriggers(QAbstractItemView.NoEditTriggers)
            else:
                selected_content = selected_item.text()
                if len(selected_content) == 0:
                    self.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:  # If the selected item has a task
                    self.setEditTriggers(QAbstractItemView.DoubleClicked)

    def check_wip(self, sel_col, move_direction):
        """ Check the limitations of WIP """
        # self.test_wip_actual(sel_col)  # Raise an error if WIP conflicts
        if move_direction == 1:  # Right move
            # WIP exists in the 2nd, 3rd, 4th column
            if (sel_col < self.columnCount() - 2 and self.blocked_flag == 0) or (
                    sel_col < self.columnCount() - 3 and self.blocked_flag == 1):
                if int(self.wip_limit_list[sel_col]) > self.check_column(sel_col + 1):
                    return True  # Current workload do not exceed WIP
                else:
                    return False
            else:
                return True

        if move_direction == -1:  # Left move
            if (sel_col < self.columnCount() and self.blocked_flag == 0) or (
                    sel_col < self.columnCount() - 1 and self.blocked_flag == 1):
                if int(self.wip_limit_list[sel_col - 2]) > self.check_column(sel_col - 1):
                    return True
                else:
                    return False
            else:
                return True

    def check_column(self, sel_col):
        """ Counter for the number of items in the selected column """
        blank_item = 0

        for i in range(self.rowCount()):
            current_item = self.item(i, sel_col)

            if current_item is None:
                blank_item = blank_item + 1
            else:
                content = current_item.text()
                if len(content) == 0:
                    blank_item = blank_item + 1

        return self.rowCount() - blank_item

    def insert_row(self, sel_row):
        """ Insert one row above the selected row """
        self.task_list.insert(sel_row, Task(None, self.columnCount()))
        self.insertRow(sel_row)

    def delete_row(self, sel_row):
        """ Delete the selected row """
        self.task_list.pop(sel_row)
        self.removeRow(sel_row)

    def add_to_blocked(self, sel_row):
        """ Put the task in this row to Blocked """
        if self.blocked_flag == 1:
            exist_flag = False  # Examine if a task exists in the selected row
            for i in range(1, self.columnCount() - 2):
                if self.item(sel_row, i) is not None:
                    # If there is a task in the row, the task will move to blocked
                    if len(self.item(sel_row, i).text()) != 0:
                        exist_flag = True
                        current_task = self.task_list[sel_row]
                        current_task.time_list[-1] = time.asctime(
                            time.localtime(time.time()))

                        current_task.previous_state = i
                        current_task.column = self.columnCount() - 1
                        self.setItem(sel_row, self.columnCount() - 1,
                                     QTableWidgetItem(current_task.name))
                        self.setItem(sel_row, i, QTableWidgetItem(None))
                        break

            if not exist_flag:
                no_blocked_msg()

    def remove_from_blocked(self, sel_row):
        """ Remove the task of this row from Blocked """
        if self.blocked_flag == 1:
            if self.item(sel_row, self.columnCount() - 1) is not None:
                # If there is a task in Blocked
                if len(self.item(sel_row, self.columnCount() - 1).text()) != 0:
                    current_task = self.task_list[sel_row]
                    if self.wip_limit_list[current_task.previous_state - 1] > self.check_column(
                            current_task.previous_state):  # Check WIP limit
                        self.setItem(sel_row, current_task.previous_state,
                                     QTableWidgetItem(current_task.name))
                        self.setItem(sel_row, self.columnCount() - 1, QTableWidgetItem(None))

                        current_task.column = current_task.previous_state
                        # Reset the information about Blocked
                        current_task.previous_state = 0
                        current_task.time_list[-1] = ""

                    else:
                        wip_msg()

            else:
                no_blocked_msg()

    def person_setting(self, sel_row):
        """ Setting person for the task """
        exist_flag = False  # Examine if a task exists in the selected row
        for i in range(self.columnCount()):
            if self.item(sel_row, i) is not None:
                # When there is a task in the row, the person setting is allowed to pop up
                if len(self.item(sel_row, i).text()) != 0:
                    exist_flag = True
                    setting_person_dialog = SettingPersonDialog()
                    setting_person_dialog.exec()
                    print(setting_person_dialog.person_name)

                    current_task = self.task_list[sel_row]
                    current_task.update_person(setting_person_dialog.person_name)

        if not exist_flag:
            no_task_msg()

    def new_column(self):
        """ Initialise the column """
        column_headings = ["1"]
        for i in range(1, self.columnCount() - 1):
            column_headings.append(str(i + 1) + " (" + str(self.wip_limit_list[i - 1]) + ")")
        column_headings.append(str(self.columnCount()))

        self.setHorizontalHeaderLabels(column_headings)

    def get_column(self):
        """ Return the current column information """
        column_list = []

        for i in range(self.columnCount()):
            col_name = (self.horizontalHeaderItem(i).text().split())[0]
            column_list.append(col_name)

        return column_list

    def update_preference(self, new_column, new_wip_limit):
        """ Update the column and wip from new preference """
        self.wip_limit_list = new_wip_limit
        if self.blocked_flag == 1:
            for i in range(1, self.columnCount() - 2):
                new_column[i] = new_column[i] + " (" + str(new_wip_limit[i - 1]) + ")"
                # Process updated column names
                self.setHorizontalHeaderLabels(new_column)
        else:
            for i in range(1, self.columnCount() - 1):
                new_column[i] = new_column[i] + " (" + str(new_wip_limit[i - 1]) + ")"
                # Process updated column names
                self.setHorizontalHeaderLabels(new_column)

    def add_blocked(self):
        """ Add Blocked column """
        self.blocked_flag = 1
        self.insertColumn(self.columnCount())
        self.setHorizontalHeaderItem(self.columnCount() - 1, QTableWidgetItem("Blocked"))

    def update_task(self):
        """ Update the row number and content of the task """
        for i in range(len(self.task_list)):
            current_task = self.task_list[i]
            current_task.update_row(i)
            if self.item(i, current_task.column) is not None:
                content = self.item(i, current_task.column).text()
                current_task.update_name(content)

    # def get_all_tasks(self):
    #     task_list = [['' for i in range(3)] for j in range(self.rowCount())]  # [row, column, task_name]
    #
    #     for i in range(self.rowCount()):
    #         for j in range(self.columnCount()):
    #             item = self.item(i, j)
    #             if item is not None:
    #                 if len(item.text()) != 0:
    #                     task_list[i] = [i, j, item.text()]
    #
    #     print(task_list)
    #     return task_list
    #
    # def read_tasks(self, task_list):
    #     for i in range(self.rowCount()):
    #         if task_list[i][0] != '':
    #             self.setItem(int(task_list[i][0]), int(task_list[i][1]), QTableWidgetItem(task_list[i][2]))

    def detail_msg(self):
        """ Pop up a message box about details of this task """
        detail_msg = QMessageBox()

        flag = False
        sel_row = self.currentRow()
        current_task = self.task_list[sel_row]

        col_num = self.columnCount()
        column_list = []
        detail = ""

        if self.blocked_flag == 1:
            for i in range(col_num - 1):
                col_name = (self.horizontalHeaderItem(i).text().split())[0]  # Ignore the content of WIP limits
                column_list.append(col_name)
        else:
            for i in range(col_num):
                col_name = (self.horizontalHeaderItem(i).text().split())[0]  # Ignore the content of WIP limits
                column_list.append(col_name)

        print(column_list)

        for i in range(col_num):
            if self.item(sel_row, i) is not None:
                if len(self.item(sel_row, i).text()) != 0:
                    flag = True
                    self.update_task()
                    detail = "Task: " + current_task.name + "\nPerson Name: " + current_task.person + "\n\n"

        if flag:
            for i in range(1, len(column_list)):
                detail = detail + "To " + column_list[i] + ": " + current_task.time_list[i - 1] + "\n"

            if self.blocked_flag == 1 and current_task.column == col_num - 1:
                detail = detail + "\n" + "To Blocked: " + current_task.time_list[-1] + "\nPrevious state: " + \
                         (self.horizontalHeaderItem(int(current_task.previous_state)).text().split())[0]

            detail_msg.setText(detail)
            detail_msg.exec()
            print(detail)

        else:
            no_task_msg()

    # ******************************************************************************
    def test_wip_actual(self, current_col):
        """ Test if WIP limit works in the actual scenario """
        if self.blocked_flag == 0:
            if 1 < current_col < self.columnCount() - 1:
                if self.check_column(current_col) > self.wip_limit_list[current_col - 1]:
                    raise Exception("Exceed the WIP limit")

        elif self.blocked_flag == 1:
            if 1 < current_col < self.columnCount() - 2:
                if self.check_column(current_col) > self.wip_limit_list[current_col - 1]:
                    raise Exception("Exceed the WIP limit")


# ******************************************************************************
def no_blocked_msg():
    """ Pop up a message box about which no task is in progress """
    invalid_msg = QMessageBox()
    invalid_msg.setText("No task in the selected row can be blocked")
    invalid_msg.exec()


def no_task_msg():
    """ Pop up a message box about which no task is in the row """
    invalid_msg = QMessageBox()
    invalid_msg.setText("No task in the selected row")
    invalid_msg.exec()


def wip_msg():
    """ Warn the restriction of WIP """
    invalid_msg = QMessageBox()

    invalid_msg.setText("Work-in-progress has reached the limit")
    invalid_msg.setFixedSize(400, 200)
    invalid_msg.exec()


def blank_msg():
    """ Report the error when trying to drag the blank item """
    invalid_msg = QMessageBox()

    invalid_msg.setText("The selected item is blank")
    invalid_msg.setFixedSize(400, 200)
    invalid_msg.exec()
