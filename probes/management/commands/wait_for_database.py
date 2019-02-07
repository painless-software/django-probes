"""
FILE: probes/management/commands/wait_for_database.py
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand)

    """
    A readiness probe you can use for Kubernetes.

    If the default database is ready, i.e. willing to accept connections
    and handling requests, then this call will succeed silently. Otherwise
    it will throw an exception.
    """
    help = 'Probes for database availability'

    def handle(self, *args, **options):
        """Throw an exception if database is not (yet) available."""
        while True:
            for uptime in range(4):
                try:
                    connection.cursor().execute('SELECT')
                except:  # TODO: use appropriate exception type
                    print('Waiting for database')
                    sleep(2)
                    continue
                break
