from collections import OrderedDict
import datetime
import os
import re

from peewee import *

db = SqliteDatabase('worklog.db')


class Entry(Model):
    employee = CharField(max_length=255, unique=False)
    task_name = CharField(max_length=255, unique=False)
    duration = CharField(max_length=255, unique=False)
    notes = CharField(max_length=255, unique=False)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def main_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("""Welcome to project 4: Worklog with a database.
Select the following options or press 'q' to quit.""")
        for key, value in directory_main.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in directory_main:
            clear()
            directory_main[choice]()


def view_loop():
    """View an entry"""
    choice = None

    while choice != 'q':
        clear()
        print("View an entry:\nSelect the following options or press 'q' to g\
o back.")
        for key, value in directory_view.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in directory_view:
            clear()
            entries = directory_view[choice]()
            view_entry(entries)


def view_entry(entries):
    """print out entry"""
    for entry in entries:
        clear()
        print("Here are your selected logs:")
        print("""
    Date: {}
    Employee: {}
    Task: {}
    duration: {}
    Notes: {}
        """.format(entry.timestamp.strftime('%A %B %d, %Y %I:%Mp'),
                   entry.employee,
                   entry.task_name,
                   entry.duration,
                   entry.notes
                   ))
        print('n) next entry')
        print('d) delete entry')

        next_action = None

        while next_action is None:
            next_action = input('Action: ').lower().strip()

            if next_action == 'd':
                delete_entry(entry)

            elif next_action != 'n':
                next_action = None


def add_entry():
    """Add entry"""
    print("Create an entry:")
    data1 = get_employee_name()
    clear()

    print("Create an entry:")
    data2 = get_task_name()
    clear()

    print("Create an entry:")
    data3 = get_time_spent()
    clear()

    print("Create an entry:")
    data4 = get_notes()
    clear()

    Entry.create(employee=data1, task_name=data2, duration=data3, notes=data4)

    print("Saved successfully!")
    input('Press ENTER to continue.')


def get_employee_name():
    """Prompt the employee for their name."""
    while True:
        employee = input("Enter employee name: ")
        if len(employee) == 0:
            print("\nYou must enter your name!\n")
            continue
        else:
            return employee


def get_task_name():
    """Prompt the employee for the task name."""
    while True:
        task_name = input("Enter a task name: ")
        if len(task_name) == 0:
            print("\nYou must enter a task name!\n")
            continue
        else:
            return task_name


def get_time_spent():
    """Prompt the employee for the time spent on their task."""
    while True:
        duration = input("Enter number of minutes spent working on the task: \
")
        try:
            int(duration)
        except ValueError:
            print("\nNot a valid time entry! Enter time as a whole integer.\n\
")
            continue
        else:
            return duration


def get_notes():
    """Prompt employee to provide any additional notes."""
    notes = input("Notes for this task (ENTER if None): ")
    return notes


def find_by_employee():
    """Find by employee"""
    entries = Entry.select().order_by(Entry.employee.desc())
    print("Find by employee:\nSelect an employee from the list below:")
    employees = []

    for entry in entries:
        if entry.employee not in employees:
            employees.append(entry.employee)

    for entry in employees:
        print("{}) {}".format(employees.index(entry), str(entry)))

    selection = test_input(len(employees))
    return entries.where(Entry.employee.contains(employees[selection]))


def find_by_date():
    """Find by date"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    print("Find by date:\nSelect a date from the list below:")
    date = []

    for entry in entries:
        if entry.timestamp not in date:
            date.append(entry.timestamp)

    for entry in date:
        print("{}) {}".format(date.index(entry),
                              entry.strftime('%A %B %d, %Y %I:%Mp')))

    selection = test_input(len(date))
    return entries.where(Entry.timestamp.contains(date[selection]))


def find_by_time_spent():
    """Find by time spent"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    print("Find by date:\nSelect a date from the list below:")
    duration = []

    for entry in entries:
        if entry.duration not in duration:
            duration.append(entry.duration)

    for entry in duration:
        print("{}) {}".format(duration.index(entry), entry))

    selection = test_input(len(duration))
    return entries.where(Entry.duration.contains(duration[selection]))


def find_by_search_term():
    """Find by search term"""
    search_query = input("Enter a term to search database:\n> ")
    entries = Entry.select().order_by(Entry.timestamp.desc())
    logs = entries.where(Entry.employee.contains(search_query)|
                         Entry.task_name.contains(search_query)|
                         Entry.notes.contains(search_query))

    return logs
    

def delete_entry(entry):
    """Delete entry"""
    if input("Are you sure? [yN] ").lower() == 'y':
        entry.delete_instance()
        print('Entry deleted!')
        input('Press ENTER to continue.')


def test_input(length):
    selection = None
    while selection is None:
        try:
            selection = int(input("> "))
        except ValueError:
            print("Invalid selection. Please select a number.")
            selection = None

        if selection not in range(0, length):
            selection = None

    return selection


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


directory_main = OrderedDict([
    ('1', add_entry),
    ('2', view_loop),
    ])

directory_view = OrderedDict([
    ('1', find_by_employee),
    ('2', find_by_date),
    ('3', find_by_time_spent),
    ('4', find_by_search_term)
    ])


if __name__ == '__main__':
    initialize()
    main_loop()
