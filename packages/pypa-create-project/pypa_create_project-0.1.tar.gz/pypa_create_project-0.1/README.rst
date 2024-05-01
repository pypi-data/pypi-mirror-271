pypa-create-project
===================

This is a Modul and a Script to Create a PyPa Modul

.. image:: https://img.shields.io/pypi/v/pypa-create-project.svg
    :target: https://pypi.org/project/pypa-create-project/
    :alt: PyPI version badge

Installation
------------

.. code-block:: bash

   python3 -m pip install pypa-create-project

How do Use (Script)
-------------------

Following Commands are available:

.. code-block:: text

   pypa-create-project [command] <subcommand>
   Commands:
   - init               ==> Init if the Project Ready
   - add                ==> Add Modul, Script to Project
   - create             ==> Create Project by Name
   - test               ==> Test Project

Install Depends
---------------

Linux

.. code-block:: bash

   python3 -m pip install twine

Termux

.. code-block:: bash

   curl -OL https://github.com/termuxdev314/termuxdev314.github.io/releases/download/v.1.0/python-repo.deb
   dpkg -i python-repo.deb
   rm -rf python-repo.deb
   pkg up
   pkg in python-twine


