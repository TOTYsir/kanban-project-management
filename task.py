#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Yue Wang
# Created Date: 11/05/2022
# version = '1.0'
# ---------------------------------------------------------------------------
""" Single Task in the Kanban Board """

# ---------------------------------------------------------------------------

from PySide6.QtWidgets import QTableWidgetItem


# ---------------------------------------------------------------------------

class Task(QTableWidgetItem):
    def __init__(self, name, total_col_num):
        super().__init__(name)

        self.name = name
        self.total_col_num = total_col_num

        self.row = 0
        self.column = 0
        self.person = ""
        self.time_list = []
        self.previous_state = 0

        self.time_list = ["" for i in range(total_col_num)]

    def update_row(self, current_row):
        """ Update the row of the task because the row is not recorded continuously """
        self.row = current_row

    def update_name(self, current_content):
        """ Update the content of the task to solve no content for the task in the first column """
        self.name = current_content

    def update_person(self, new_person):
        """ Update the person name of the task """
        self.person = new_person
