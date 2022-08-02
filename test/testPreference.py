from random import randint

from PySide6 import QtCore

from preferencesDialog import PreferencesDialog


def test_init_col_name(qtbot):
    column_list = []
    for i in range(5):
        column_name = "col_" + str(i + 1)
        column_list.append(column_name)

    wip_limit_list = [3, 3, 3]
    current_list = [1, 1, 1]
    blocked_flag = 0

    preferences_dialog = PreferencesDialog(column_list, wip_limit_list, current_list, blocked_flag)
    qtbot.addWidget(preferences_dialog)

    assert (preferences_dialog.column_list, column_list)


def test_init_wip_limit(qtbot):
    column_list = []
    wip_limit_list = []
    for i in range(5):
        column_name = "col_" + str(i + 1)
        column_list.append(column_name)

    for j in range(3):
        rand_val = randint(1, 30)
        wip_limit_list.append(rand_val)

    current_list = [1, 1, 1]
    blocked_flag = 0

    preferences_dialog = PreferencesDialog(column_list, wip_limit_list, current_list, blocked_flag)
    qtbot.addWidget(preferences_dialog)

    assert (preferences_dialog.wip_limit_list, wip_limit_list)


def test_init_no_wip(qtbot):
    column_list = []
    wip_limit_list = []
    for i in range(5):
        column_name = "col_" + str(i + 1)
        column_list.append(column_name)

    for j in range(3):
        rand_val = randint(1, 30)
        wip_limit_list.append(rand_val)

    current_list = [1, 1, 1]
    blocked_flag = 0

    preferences_dialog = PreferencesDialog(column_list, wip_limit_list, current_list, blocked_flag)
    qtbot.addWidget(preferences_dialog)

    assert (preferences_dialog.preference_table.item(0, 1), None)
    assert (preferences_dialog.preference_table.item(4, 1), None)


def test_init_current(qtbot):
    column_list = []
    current_list = []

    for i in range(5):
        column_name = "col_" + str(i + 1)
        column_list.append(column_name)

    wip_limit_list = [5, 5, 5]

    for j in range(3):
        rand_val = randint(0, 5)
        current_list.append(rand_val)

    blocked_flag = 0

    preferences_dialog = PreferencesDialog(column_list, wip_limit_list, current_list, blocked_flag)
    qtbot.addWidget(preferences_dialog)

    assert (preferences_dialog.current_wip_list, current_list)


def test_col_name_blocked(qtbot):
    column_list = []

    for i in range(5):
        column_name = "col_" + str(i + 1)
        column_list.append(column_name)

    column_list.append("Blocked")

    wip_limit_list = [5, 5, 5]
    current_list = [3, 3, 3]

    blocked_flag = 1

    preferences_dialog = PreferencesDialog(column_list, wip_limit_list, current_list, blocked_flag)
    qtbot.addWidget(preferences_dialog)

    assert (preferences_dialog.preference_table.item(0, 5).text(), "Blocked")
    assert (preferences_dialog.preference_table.item(0, 4).text(), "col_5")


def test_col_wip_blocked(qtbot):
    column_list = []

    for i in range(5):
        column_name = "col_" + str(i + 1)
        column_list.append(column_name)

    column_list.append("Blocked")

    wip_limit_list = [5, 5, 5]
    current_list = [3, 3, 3]

    blocked_flag = 1

    preferences_dialog = PreferencesDialog(column_list, wip_limit_list, current_list, blocked_flag)
    qtbot.addWidget(preferences_dialog)

    assert (preferences_dialog.preference_table.item(1, 1), None)
    assert (preferences_dialog.preference_table.item(1, 4), None)
    assert (preferences_dialog.preference_table.item(1, 5), None)


def test_confirm_exceed_limit(qtbot):
    column_list = []

    for i in range(5):
        column_name = "col_" + str(i + 1)
        column_list.append(column_name)

    wip_limit_list = [5, 5, 5]
    current_list = [3, 6, 3]

    blocked_flag = 1

    preferences_dialog = PreferencesDialog(column_list, wip_limit_list, current_list, blocked_flag)
    qtbot.addWidget(preferences_dialog)

    flag = qtbot.mouseClick(preferences_dialog.ok_button, QtCore.Qt.LeftButton)

    assert (flag, 1)


def test_confirm_follow_limit(qtbot):
    column_list = []

    for i in range(5):
        column_name = "col_" + str(i + 1)
        column_list.append(column_name)

    wip_limit_list = [5, 5, 5]
    current_list = [4, 4, 4]

    blocked_flag = 1

    preferences_dialog = PreferencesDialog(column_list, wip_limit_list, current_list, blocked_flag)
    qtbot.addWidget(preferences_dialog)

    flag = qtbot.mouseClick(preferences_dialog.ok_button, QtCore.Qt.LeftButton)

    assert (flag, 0)
