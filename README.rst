Django-probes |latest-version|
==============================

|checks-status| |tests-status| |publish-status| |download-stats| |python-support| |license|

Provides a Django management command to check whether the primary database
is ready to accept connections.

Run this command in a Kubernetes or OpenShift `Init Container`_ to make
your Django application wait until the database is available (e.g. to run
database migrations).

Why Should I Use This App?
--------------------------

``wait_for_database`` is a *single* command for *all* database engines
Django supports. It automatically checks the database you have configured
in your Django project settings. No need to code a specific wait command
for Postgres, MariaDB, Oracle, etc., no need to pull a database engine
specific container just for running the database readiness check.

.. |latest-version| image:: https://img.shields.io/pypi/v/django-probes.svg
   :alt: Latest version on PyPI
   :target: https://pypi.org/project/django-probes
.. |download-stats| image:: https://img.shields.io/pypi/dm/django-probes.svg
   :alt: Monthly downloads from PyPI
   :target: https://pypistats.org/packages/django-probes
.. |checks-status| image:: https://github.com/painless-software/django-probes/actions/workflows/check.yml/badge.svg
   :target: https://github.com/painless-software/django-probes/actions/workflows/check.yml
   :alt: GitHub Workflow Status
.. |tests-status| image:: https://github.com/painless-software/django-probes/actions/workflows/test.yml/badge.svg
   :target: https://github.com/painless-software/django-probes/actions/workflows/test.yml
   :alt: GitHub Workflow Status
.. |publish-status| image:: https://github.com/painless-software/django-probes/actions/workflows/publish.yml/badge.svg
   :target: https://github.com/painless-software/django-probes/actions/workflows/publish.yml
   :alt: GitHub Workflow Status
.. |python-support| image:: https://img.shields.io/pypi/pyversions/django-probes.svg
   :alt: Python versions
   :target: https://pypi.org/project/django-probes
.. |license| image:: https://img.shields.io/pypi/l/django-probes.svg
   :alt: Software license
   :target: https://github.com/painless-software/django-probes/blob/main/LICENSE

.. _Init Container: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/

Installation
============

The easiest way to install django-probes is with pip or uv, e.g.

.. code:: shell

    pip install django-probes

.. code:: shell

    uv add django-probes

Basic Usage
===========

1. Add django-probes to your Django application:

.. code:: python

    INSTALLED_APPS = [
        ...
        'django_probes',
    ]

2. Add an `Init Container`_ to your Kubernetes/OpenShift deployment
configuration, which calls the ``wait_for_database`` management command:

.. code:: yaml

    - kind: Deployment
      apiVersion: apps/v1
      spec:
        template:
          spec:
            initContainers:
            - name: wait-for-database
              image: my-django-app:latest
              envFrom:
              - secretRef:
                  name: django
              command: ['python', 'manage.py', 'wait_for_database']

Use with Your Own Command
-------------------------

Alternatively, you can integrate the ``wait_for_database`` command in your
own management command, and do things like database migration, load initial
data, etc. with roughly the same Kubernetes setup as above.

.. code:: python

    from django.core.management import call_command

    # ...
    call_command('wait_for_database')

Command Line Options
--------------------

The management command comes with sane defaults, which you can override
if needed:

:--command, -c:
    execute Django management command(s) when the database is ready.
    This option can be used multiple times, e.g.
    ``wait_for_database -c 'migrate' -c 'runserver --skip-checks'``
:--database:
    which database of ``settings.DATABASES`` to wait for, default: ``default``
:--stable, -s:
    how long to observe whether connection is stable (seconds), default: ``5``
:--timeout, -t:
    how long to wait for the database before timing out (seconds), default: ``180``
:--wait-when-alive, -a:
    delay between checks when database is up (seconds), default: ``1``
:--wait-when-down, -d:
    delay between checks when database is down (seconds), default: ``2``
