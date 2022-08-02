import os
from xml.dom import minidom

from PySide6.QtWidgets import QTableWidgetItem

from kanbanTable import KanbanTable


class XmlHandler:
    def create_xml(self, file_name, kanban_board):
        col_num = kanban_board.columnCount()
        row_num = kanban_board.rowCount()

        column_list = []
        for i in range(kanban_board.columnCount()):
            col_name = kanban_board.horizontalHeaderItem(i).text()
            column_list.append(col_name)

        print(column_list)

        xml = minidom.Document()
        include = xml.createElement('project')
        xml.appendChild(include)

        info = xml.createElement('kanban_board')
        info.setAttribute('directory', file_name)
        info.setAttribute('column', str(col_num))
        info.setAttribute('row', str(row_num))
        info.setAttribute('is_blocked', str(kanban_board.blocked_flag))
        include.appendChild(info)

        preference = xml.createElement('preference')
        info.appendChild(preference)  # Input name of the column

        for i in range(1, col_num + 1):
            column_name = "col_" + str(i)
            column_set = xml.createElement(column_name)
            column_set.appendChild(xml.createTextNode((column_list[i - 1].split())[0]))
            preference.appendChild(column_set)

        if kanban_board.blocked_flag == 0:
            for i in range(2, col_num):
                wip_name = "wip_" + str(i)
                wip_set = xml.createElement(wip_name)
                wip_set.appendChild(xml.createTextNode((column_list[i - 1].split())[1]))
                preference.appendChild(wip_set)

        if kanban_board.blocked_flag == 1:
            for i in range(2, col_num - 1):
                wip_name = "wip_" + str(i)
                wip_set = xml.createElement(wip_name)
                wip_set.appendChild(xml.createTextNode((column_list[i - 1].split())[1]))
                preference.appendChild(wip_set)

        for i in range(1, row_num + 1):
            task = kanban_board.task_list[i - 1]
            task_num = "task_" + str(i)
            task_set = xml.createElement(task_num)
            info.appendChild(task_set)
            if task.name is None:
                none_flag = 1
            else:
                none_flag = 0

            name = xml.createElement('name')
            if none_flag:
                content = ""
            else:
                content = task.name
            name.appendChild(xml.createTextNode(content))
            task_set.appendChild(name)

            row = xml.createElement('row')
            if none_flag:
                row_val = ""
            else:
                row_val = str(task.row)
            row.appendChild(xml.createTextNode(row_val))
            task_set.appendChild(row)

            column = xml.createElement('column')
            if none_flag:
                col_val = ""
            else:
                col_val = str(task.column)
            column.appendChild(xml.createTextNode(col_val))
            task_set.appendChild(column)

            if kanban_board.blocked_flag == 0:
                for i in range(2, col_num + 1):
                    column_name = "to_col_" + str(i)
                    column_set = xml.createElement(column_name)
                    column_set.appendChild(xml.createTextNode(task.time_list[i - 2]))
                    task_set.appendChild(column_set)

            if kanban_board.blocked_flag == 1:
                for i in range(2, col_num):
                    column_name = "to_col_" + str(i)
                    column_set = xml.createElement(column_name)
                    column_set.appendChild(xml.createTextNode(task.time_list[i - 2]))
                    task_set.appendChild(column_set)

            person = xml.createElement("person")
            person.appendChild(xml.createTextNode(task.person))
            task_set.appendChild(person)

            to_blocked = xml.createElement("to_blocked")
            to_blocked.appendChild(xml.createTextNode(task.time_list[-1]))
            task_set.appendChild(to_blocked)

            previous_state = xml.createElement("previous_state")
            if task.previous_state == 0:
                prev = ""
            else:
                prev = str(task.previous_state)
            previous_state.appendChild(xml.createTextNode(prev))
            task_set.appendChild(previous_state)

        f = open(file_name, 'w')
        f.write(xml.toprettyxml())
        f.close()

    def open_xml(self, file_name):
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
            open_board = KanbanTable(row, column - 1)
            open_board.add_blocked()

        column_name_list = []
        wip_limit_list = []
        preference = kanban_board.getElementsByTagName("preference")[0]
        for i in range(1, column + 1):
            column_num = "col_" + str(i)
            column_name = preference.getElementsByTagName(column_num)[0]
            column_name_list.append(column_name.firstChild.data)

        if is_blocked == 0:
            for i in range(2, column):
                column_num = "wip_" + str(i)
                wip_limit = preference.getElementsByTagName(column_num)[0]
                # wip_limit_number_with_brackets = wip_limit.firstChild.data
                # wip_limit_number = int(wip_limit_number_with_brackets.replace("(", "").replace(")", ""))
                wip_limit_list.append(int(wip_limit.firstChild.data.replace("(", "").replace(")", "")))
        else:
            for i in range(2, column - 1):
                column_num = "wip_" + str(i)
                wip_limit = preference.getElementsByTagName(column_num)[0]

                wip_limit_list.append(int(wip_limit.firstChild.data.replace("(", "").replace(")", "")))

        print(wip_limit_list)
        open_board.update_preference(column_name_list, wip_limit_list)

        for i in range(1, row + 1):  # Read the all tasks exist in current xml file
            task_num = "task_" + str(i)
            task = kanban_board.getElementsByTagName(task_num)[0]

            name_node = task.getElementsByTagName("name")[0]
            if name_node.firstChild is None:
                pass
            else:
                task_name = name_node.firstChild.data

            row_node = task.getElementsByTagName("row")[0]
            if row_node.firstChild is None:
                pass
            else:
                task_row = row_node.firstChild.data

            column_node = task.getElementsByTagName("column")[0]
            if column_node.firstChild is None:
                pass
            else:
                task_column = column_node.firstChild.data

            if name_node.firstChild is None or row_node.firstChild is None or column_node.firstChild is None:
                pass
            else:
                open_board.setItem(int(task_row), int(task_column), QTableWidgetItem(task_name))

                current_task = open_board.task_list[i - 1]
                current_task.name = task_name
                current_task.row = int(task_row)
                current_task.column = int(task_column)

            if open_board.blocked_flag == 0:
                for j in range(2, column + 1):  # Read all drag out times existed in the current task.
                    to_col_num = "to_col_" + str(j)
                    to_col_node = task.getElementsByTagName(to_col_num)[0]
                    if to_col_node.firstChild is None:
                        pass
                    else:
                        current_task.time_list[j - 2] = to_col_node.firstChild.data

                person = task.getElementsByTagName("person")[0]
                if person.firstChild is None:
                    pass
                else:
                    current_task.person = person.firstChild.data

            elif open_board.blocked_flag == 1:
                for j in range(2, column):  # Read all drag out times existed in the current task.
                    to_col_num = "to_col_" + str(j)
                    to_col_node = task.getElementsByTagName(to_col_num)[0]
                    if to_col_node.firstChild is None:
                        pass
                    else:
                        current_task.time_list[j - 2] = to_col_node.firstChild.data

                person = task.getElementsByTagName("person")[0]
                if person.firstChild is None:
                    pass
                else:
                    current_task.person = person.firstChild.data

                to_blocked = task.getElementsByTagName("to_blocked")[0]
                if to_blocked.firstChild is None:
                    pass
                else:
                    current_task.time_list[-1] = to_blocked.firstChild.data

                previous_state = task.getElementsByTagName("previous_state")[0]
                if previous_state.firstChild is None:
                    pass
                else:
                    current_task.previous_state = int(previous_state.firstChild.data)

        project_name = os.path.splitext(os.path.split(file_name)[1])[0]  # Leave the actual name of the document

        return open_board
