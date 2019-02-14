"""
FILE: django_probes/management/commands/wait_for_database.py
"""
from time import sleep, time
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError
try:
    TimeoutError
except NameError:  # Python 2.7
    TimeoutError = SystemExit  # noqa, pylint: disable=redefined-builtin


class Command(BaseCommand):
    """
    A readiness probe you can use for Kubernetes.

    If the default database is ready, i.e. willing to accept connections
    and handling requests, then this call will succeed silently. Otherwise
    it will throw an exception.
    """
    help = 'Probes for database availability'

    def handle(self, *args, **options):
        """Throw an exception if database is not (yet) available."""
        wait_for_db_seconds = 1
        stable_for_seconds = 4
        timeout_seconds = 3

        conn_alive_start = None
        start = time()

        while time() - start < stable_for_seconds:

            # loop until we have a database connection or we run into a timeout
            while True:
                elapsed_time = int(time() - start)
                if elapsed_time >= timeout_seconds:
                    raise TimeoutError(
                        'Could not establish database connection.')
                try:
                    connection.cursor().execute('SELECT')
                    if not conn_alive_start:
                        conn_alive_start = time()
                    break
                except OperationalError as err:
                    err_message = str(err).strip()
                    print('Waiting for database (cause: {msg}) ... {elapsed}s'.
                          format(msg=err_message, elapsed=elapsed_time))
                    sleep(wait_for_db_seconds)

            print('Connection alive for > {uptime}s'.format(
                uptime=int(time() - conn_alive_start)))
            sleep(1)
