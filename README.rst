Django-probes |latest-version|
==============================

|build-status| |python-support| |license|

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
.. |build-status| image:: https://img.shields.io/travis/vshn/django-probes/master.svg
   :alt: Build status
   :target: https://travis-ci.org/vshn/django-probes
.. |python-support| image:: https://img.shields.io/pypi/pyversions/django-probes.svg
   :alt: Python versions
   :target: https://pypi.org/project/django-probes
.. |license| image:: https://img.shields.io/pypi/l/django-probes.svg
   :alt: Software license
   :target: https://github.com/vshn/django-probes/blob/master/LICENSE

.. _Init Container: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/

Installation
============

The easiest way to install django-probes is with pip

.. code:: console

    $ pip install django-probes

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

Command Line Options
--------------------

The management command comes with sane defaults, which you can override
if needed:

:--timeout, -t:
    how long to wait for the database before timing out (seconds), default: 180
:--stable, -s:
    how long to observe whether connection is stable (seconds), default: 5
:--wait-when-down, -d:
    delay between checks when database is down (seconds), default: 2
:--wait-when-alive, -a:
    delay between checks when database is up (seconds), default: 1
