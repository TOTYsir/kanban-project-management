from task import Task


def test_init_name(qtbot):
    task = Task("write the report", 6)

    assert (task.name, "write the report")


def test_init_total_col(qtbot):
    task = Task("test", 10000)

    assert (task.total_col_num, 10000)


def test_init_time_list(qtbot):
    task = Task("test", 3)

    assert (len(task.time_list), 4)


def test_init_row(qtbot):
    task = Task("test", 4)

    assert (task.row, 0)


def test_init_column(qtbot):
    task = Task("test", 5)

    assert (task.column, 0)


def test_init_person(qtbot):
    task = Task("test", 6)

    assert (task.person, "")


def test_init_prev_state(qtbot):
    task = Task("test", 3)

    assert (task.previous_state, 0)


def test_update_row(qtbot):
    task = Task("test", 4)

    task.update_row(2)

    assert (task.row, 2)


def test_update_name(qtbot):
    task = Task("test", 4)

    task.update_name("set up the milestone")

    assert (task.name, "set up the milestone")


def test_update_person(qtbot):
    task = Task("test", 5)
    task.person = "Carl Williams"

    task.update_person("Paul Morgan")

    assert (task.person, "Paul Morgan")
