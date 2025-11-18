"""
Verify that ``python manage.py wait_for_database`` works fine.
"""

import os
import tempfile
from unittest.mock import patch

import pytest
from django.core.management import CommandError, call_command
from django.db import OperationalError

from django_probes.management.commands.wait_for_database import wait_for_database

CLI_PARAMS = {
    "wait_when_down": 1,
    "wait_when_alive": 1,
    "stable": 3,
    "timeout": 1,
    "database": "default",
}


@patch("django.db.connection.is_usable", return_value=True)
@patch("django.db.connection.ensure_connection")
def test_loops_stable_times(mock_ensure_conn, mock_is_usable):
    """
    Database connection must be stable some consecutive times in a row.
    """
    wait_for_database(**CLI_PARAMS)

    assert mock_ensure_conn.call_count == CLI_PARAMS["stable"] + 1
    assert mock_is_usable.call_count == CLI_PARAMS["stable"] + 1


@patch("django.db.connection.is_usable", return_value=True)
@patch("django.db.connection.ensure_connection")
def test_can_call_through_management(mock_ensure_conn, mock_is_usable):
    """
    Executing the management command works (w/o operational errors).
    """
    call_command("wait_for_database", stable=0, timeout=0)

    assert mock_ensure_conn.called
    assert mock_is_usable.called


@patch("django.db.connection.is_usable")
@patch("django.db.connection.ensure_connection", side_effect=OperationalError())
def test_exception_caught_when_connection_absent(mock_ensure_conn, mock_is_usable):
    """
    When database connection is absent related errors are caught.
    """
    with pytest.raises(TimeoutError):
        wait_for_database(**CLI_PARAMS)

    assert mock_ensure_conn.called
    assert not mock_is_usable.called


@patch("django.db.connection.is_usable", return_value=False)
@patch("django.db.connection.ensure_connection")
def test_exception_caught_when_unusable(mock_ensure_conn, mock_is_usable):
    """
    When database connection unusable related errors are caught.
    """
    with pytest.raises(TimeoutError):
        wait_for_database(**CLI_PARAMS)

    assert mock_ensure_conn.called
    assert mock_is_usable.called


@patch("django.db.connection.ensure_connection", side_effect=OperationalError())
def test_command_error_raised_when_connection_absent(mock_ensure_conn):
    """
    When database connection is absent the management command aborts.
    """
    with pytest.raises(CommandError):
        call_command("wait_for_database", stable=0, timeout=0)

    assert mock_ensure_conn.called


@patch("django.db.connection.is_usable", return_value=True)
@patch("django.db.connection.ensure_connection")
def test_can_call_through_management_with_commands(mock_ensure_conn, mock_is_usable):
    """
    Executing the management command works (w/o operational errors).
    """
    with tempfile.TemporaryDirectory() as dirname:
        call_command(
            "wait_for_database",
            "--stable=0",
            "--timeout=0",
            "-c",
            f'shell -c \'open("{dirname}/0", "w").close()\'',
            "-c",
            f'shell -c \'open("{dirname}/1", "w").close()\'',
        )
        created_objects = set(os.listdir(dirname))

    assert created_objects == {"0", "1"}
    assert mock_ensure_conn.called
    assert mock_is_usable.called
