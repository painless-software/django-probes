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
    TimeoutError = RuntimeError  # noqa, pylint: disable=redefined-builtin


def wait_for_database(**opts):
    """
    The main loop waiting for the database connection to come up.
    """
    wait_for_db_seconds = opts['wait_when_down']
    alive_check_delay = opts['wait_when_alive']
    stable_for_seconds = opts['stable']
    timeout_seconds = opts['timeout']

    conn_alive_start = None
    start = time()

    while True:
        # loop until we have a database connection or we run into a timeout
        while True:
            try:
                connection.cursor().execute('SELECT')
                if not conn_alive_start:
                    conn_alive_start = time()
                break
            except OperationalError as err:
                conn_alive_start = None

                elapsed_time = int(time() - start)
                if elapsed_time >= timeout_seconds:
                    raise TimeoutError(
                        'Could not establish database connection.')

                err_message = str(err).strip()
                print('Waiting for database (cause: {msg}) ... {elapsed}s'.
                      format(msg=err_message, elapsed=elapsed_time))
                sleep(wait_for_db_seconds)

        uptime = int(time() - conn_alive_start)
        print('Connection alive for > {}s'.format(uptime))

        if uptime >= stable_for_seconds:
            break

        sleep(alive_check_delay)


class Command(BaseCommand):
    """
    A readiness probe you can use for Kubernetes.

    If the default database is ready, i.e. willing to accept connections
    and handling requests, then this call will exit successfully. Otherwise
    the command exits with an error status after reaching a timeout.
    """
    help = 'Probes for database availability'

    def add_arguments(self, parser):
        parser.add_argument('--timeout', '-t', default=180, type=int,
                            metavar='SECONDS', action='store',
                            help='how long to wait (seconds), default: 180')
        parser.add_argument('--stable', '-s', default=5, type=int,
                            metavar='SECONDS', action='store',
                            help='how long to observe whether '
                                 'connection is stable (seconds), default: 5')
        parser.add_argument('--wait-when-down', '-d', default=2, type=int,
                            metavar='SECONDS', action='store',
                            help='delay between checks when database is '
                                 'down (seconds), default: 2')
        parser.add_argument('--wait-when-alive', '-a', default=1, type=int,
                            metavar='SECONDS', action='store',
                            help='delay between checks when database is '
                                 'up (seconds), default: 1')

    def handle(self, *args, **options):
        """
        Wait for a database connection to come up. Exit with error
        status when a timeout threshold is surpassed.
        """
        try:
            wait_for_database(**options)
        except TimeoutError as err:
            raise SystemExit(err)
