"""
Verify that ``python manage.py wait_for_database`` works fine.
"""
from unittest import TestCase
from unittest.mock import patch

from django.core.management import call_command, CommandError
from django.db import OperationalError

CLI_PARAMS = {
    'timeout': 0,
    'stable': 0
}


class WaitForDatabaseManagementCommandTest(TestCase):
    @patch('django.db.connection.cursor', side_effect=OperationalError())
    def test_command_exception_raised_when_connection_absent(self, mock_db_cursor):
        with self.assertRaises(CommandError):
            call_command('wait_for_database', **CLI_PARAMS)

    @patch('django.db.connection.cursor')
    def test_can_call_through_management(self, mock_db_cursor):
        call_command('wait_for_database', **CLI_PARAMS)
        self.assertTrue(mock_db_cursor.called)
