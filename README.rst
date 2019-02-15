Django-probes |latest-version|
==============================

|build-status| |python-support| |license|

This python package provides a management to check whether the database is ready

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

Installation
============

The easiest way to install django-probes is with pip

.. code:: console

    $ pip install django-probes

Basic Usage
===========

Add django-probes to your Django application:

.. code:: python

    INSTALLED_APPS = [
        ...
        'django_probes',
    ]

Add an ``initContainer`` to your Kubernetes/OpenShift deployment configuration,
which calls the ``wait_for_database`` management command:

.. code:: yaml

    - kind: Deployment
      apiVersion: apps/v1
      spec:
        template:
          spec:
            initContainers:
            - name: check-db-ready
              image: my-django-app:latest
              envFrom:
              - secretRef:
                name: django
              command: ['python', 'manage.py', 'wait_for_database']

Command Line Options
--------------------

The management command has sane default, which you can override to your liking.

:--timeout, -t:
    how long to wait (seconds), default: 180
:--stable, -s:
    how long to observe whether connection is stable (seconds), default: 4
:--wait-when-alive, -a:
    delay between checks when database is up (seconds), default: 1
:--wait-when-down, -d:
    delay between checks when database is down (seconds), default: 1
