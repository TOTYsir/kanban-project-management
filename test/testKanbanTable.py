from random import randint

from PySide6.QtWidgets import QTableWidgetItem

from kanbanTable import KanbanTable


def test_init_row(qtbot):
    kanban_table = KanbanTable(30, 5)
    qtbot.addWidget(kanban_table)

    assert kanban_table.rowCount() == 30


def test_init_col(qtbot):
    kanban_table = KanbanTable(30, 5)
    qtbot.addWidget(kanban_table)

    assert kanban_table.columnCount() == 5


def test_init_limit(qtbot):
    kanban_table = KanbanTable(30, 5)
    qtbot.addWidget(kanban_table)

    assert len(kanban_table.wip_limit_list) == kanban_table.columnCount() - 2


def test_init_blocked_flag(qtbot):
    kanban_table = KanbanTable(30, 5)
    qtbot.addWidget(kanban_table)

    assert kanban_table.blocked_flag == 0


def test_column_check(qtbot):
    kanban_table = KanbanTable(30, 5)
    qtbot.addWidget(kanban_table)

    rand_col = randint(1, 4)
    rand_task_num = randint(1, 30)
    for j in range(rand_task_num):
        kanban_table.setItem(j, rand_col, QTableWidgetItem("TEST_WIP"))

    task_num = kanban_table.check_column(rand_col)
    assert (task_num, rand_task_num)


def test_insert(qtbot):
    kanban_table = KanbanTable(30, 5)
    qtbot.addWidget(kanban_table)

    rand_row = randint(0, 29)
    kanban_table.setItem(rand_row, 0, QTableWidgetItem("TEST_INSERT_A"))
    kanban_table.setItem(rand_row + 1, 0, QTableWidgetItem("TEST_INSERT_B"))
    kanban_table.insert_row(rand_row)

    assert (kanban_table.rowCount(), 31)

    assert (kanban_table.item(rand_row - 1, 0), "TEST_INSERT_A")
    assert (kanban_table.item(rand_row, 0), None)
    assert (kanban_table.item(rand_row + 1, 0).text(), "TEST_INSERT_B")


def test_delete(qtbot):
    kanban_table = KanbanTable(30, 5)
    qtbot.addWidget(kanban_table)

    rand_row = randint(0, 30)
    kanban_table.setItem(rand_row, 0, QTableWidgetItem("TEST_DELETE_A"))
    kanban_table.setItem(rand_row + 1, 0, QTableWidgetItem("TEST_DELETE_B"))
    kanban_table.delete_row(rand_row)

    assert (kanban_table.rowCount(), 29)

    assert (kanban_table.item(rand_row, 0), "TEST_DELETE_B")
