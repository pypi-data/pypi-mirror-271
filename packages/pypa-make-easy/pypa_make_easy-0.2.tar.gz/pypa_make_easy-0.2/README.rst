PyPa Make Easy
==============

PyPa make easy is an Tool, for Create PyPi Lirrys utin Easy.

.. image:: https://img.shields.io/pypi/v/pypa-make-easy.svg
        :target: https://pypi.org/project/pypa-make-easy/

.. image:: https://img.shields.io/github/stars/DevMasterLinux/pypa-make-easy.svg?style=social
        :target: https://github.com/DevMasterLinux/pypa-make-easy

How Can i Use
-------------

The Using is really easy, you hae 2 Options

Over Commandline

.. code-block:: bash

    Usage: help [COMMAND]...
    Commands:
    create                        Display help for create command.
    init                          Display help for init command.
    yaml                          Display help for yaml command.
    error                         Display help for error handling.
    help                          Display this help and exit.

Or Configure a Yml File

.. code-block:: yaml

    ProjectName: my_modul
    Scripts: False
    Moduls:
    Modul1:
        name: example1.py
        source:
        Type: True
        Path: ./example1.py
    Modul2:
        name: example2.py
        source:
        Type: True
        Path: ./example2.py
    SubModuls:
    Modul1:
        name: sub_1
        source:
        Type: True
        Path: .
        Files:
        - sub1.py
        - sub2.py
    Readme:
        Exist: False
        Path: Skip
    Setup:
        Exist: False
        Path: Skip

If you configure The Project over Yaml, set under Path the Full Path and the File must be named pypa.yaml, pypa.yml, pypi.yaml or pypi.yml, other files are not supported.

Install
-------

.. code-block:: bash

    python3 -m pip install pypa-make-easy
