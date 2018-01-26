import unittest
import unittest.mock as mock

from peewee import *

import worklog_db
from worklog_db import Entry


TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([Entry], safe=True)

DATA = {
    "employee": "test_name",
    "task_name": "test_task",
    "duration": 120,
    "notes": "test_notes",
    "timestamp": "datetime.datetime(2018, 1, 16, 0, 14, 18, 27397)"
}


class WorkLogTests(unittest.TestCase):
    @staticmethod
    def create_entries():
        Entry.create(
            employee=DATA["employee"],
            duration=DATA["duration"],
            task_name=DATA["task_name"],
            notes=DATA["notes"],
            timestamp=DATA["timestamp"]
        )

    def test_get_employee_name(self):
        with mock.patch('builtins.input', side_effect=["", "test_name"],
                        return_value=DATA["employee"]):
            assert worklog_db.get_employee_name() == DATA["employee"]

    def test_get_task_name(self):
        with mock.patch('builtins.input', side_effect=["", "test_task"],
                        return_value=DATA["task_name"]):
            assert worklog_db.get_task_name() == DATA["task_name"]

    def test_get_time_spent(self):
        with mock.patch('builtins.input', side_effect=["1s", 120],
                        return_value=DATA["duration"]):
            self.assertRaises(ValueError)
            assert worklog_db.get_time_spent() == DATA["duration"]

    def test_get_notes(self):
        with mock.patch('builtins.input', return_value=DATA["notes"]):
            assert worklog_db.get_notes() == DATA["notes"]

    def test_test(self):
        with mock.patch('builtins.input', side_effect=[0]):
            self.assertEqual(worklog_db.test(10), 0)

    def test_find_by_employee(self):
        with mock.patch('builtins.input', side_effect=[0],
                        return_value=DATA['employee']):
            self.assertNotEqual(worklog_db.find_by_employee(), None)

    def test_find_by_date(self):
        with mock.patch('builtins.input', side_effect=[0],
                        return_value=DATA['timestamp']):
            self.assertNotEqual(worklog_db.find_by_date(), None)

    def test_find_by_time_spent(self):
        with mock.patch('builtins.input', side_effect=[0],
                        return_value=DATA['duration']):
            self.assertNotEqual(worklog_db.find_by_time_spent(), None)


if __name__ == '__main__':
    unittest.main()
