"""
FILE: django_probes/management/commands/wait_for_database.py
"""
from django.core.management.base import BaseCommand
from django.db import connection
from time import sleep


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

        for uptime in range(stable_for_seconds):

            # loop until we have a database connection
            while True:
                try:
                    connection.cursor().execute('SELECT')
                    break
                except:  # TODO: use appropriate exception type
                    print('Waiting for database')
                    sleep(wait_for_db_seconds)

            print('Connection alive for > {uptime}s'.format(uptime=uptime))
            sleep(1)
