"""
Verify that ``python manage.py wait_for_database`` works fine.
"""
import pytest

# from django.core.management import call_command
from django.db.utils import OperationalError

try:
    from unittest.mock import patch
except ImportError:  # Python 2.7
    from mock import patch
    TimeoutError = RuntimeError  # noqa, pylint: disable=redefined-builtin

from django_probes.management.commands.wait_for_database \
    import wait_for_database

CLI_PARAMS = {
    'wait_when_down': 1,
    'wait_when_alive': 1,
    'stable': 999,
    'timeout': 1,
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
    with pytest.raises(TimeoutError):
        wait_for_database(**CLI_PARAMS)

    assert mock_db_cursor.call_count == 1  # CLI_PARAMS['stable']
