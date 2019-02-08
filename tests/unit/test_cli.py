"""
Verify that ``python manage.py wait_for_database`` works fine.
"""
import pytest

from django.core.management import call_command
from django.test import override_settings

from django_probes.management.commands import wait_for_database


@pytest.mark.django_db
def test_no_exception_when_connection_absent():
    """
    Blah ...
    """
    management_command = wait_for_database.__name__.split('.')[-1]

    with pytest.raises(SystemExit):
        call_command(management_command)
