"""
Verify that ``python manage.py wait_for_database`` works fine.
"""
from unittest.mock import patch
from django.db.utils import OperationalError

import pytest

from django_probes.management.commands.wait_for_database \
    import wait_for_database

CLI_PARAMS = {
    'wait_when_down': 1,
    'wait_when_alive': 1,
    'stable': 3,
    'timeout': 1,
    'database': 'default',
}


@patch('django.db.connection.cursor', side_effect=OperationalError())
def test_exception_caught_when_connection_absent(mock_db_cursor):
    """
    When database connection is absent related errors are caught.
    """
    with pytest.raises(TimeoutError):
        wait_for_database(**CLI_PARAMS)

    assert mock_db_cursor.called


@patch('django.db.connection.cursor')
def test_loops_stable_times(mock_db_cursor):
    """
    Database connection must be stable some consecutive times in a row.
    """
    wait_for_database(**CLI_PARAMS)

    assert mock_db_cursor.call_count == CLI_PARAMS['stable'] + 1
