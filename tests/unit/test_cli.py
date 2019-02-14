"""
Verify that ``python manage.py wait_for_database`` works fine.
"""
# import pytest

from django.core.management import call_command

try:
    from unittest.mock import patch
except ImportError:  # Python 2.7
    from mock import patch


# @pytest.mark.django_db
# @patch('django.db.utils.OperationalError')
# def test_exception_caught_when_connection_absent(mock_db_exception):
#     """
#     When database connection is absent related errors are caught.
#     """
#     call_command('wait_for_database')
#     assert mock_db_exception.called


@patch('django.db.connection.cursor')
def test_loops_stable_times(mock_db_cursor):
    """
    Database connection must be stable 4 consecutive times in a row.
    """
    call_command('wait_for_database')
    assert mock_db_cursor.call_count == 4
