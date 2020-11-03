gridtools
============

A small Python library to convert between maidenhead grid locators and lat/long coördinates.

Installation
------------

``gridtools`` requires Python 3.8 at minimum. Install by running::

    $ pip install gridtools

License
-------

Copyright 2020 classabbyamp, 0x5c

Released under the BSD 3-Clause License. See `LICENSE`_ for the full license text.

.. _LICENSE: https://github.com/miaowware/gridtools/blob/master/LICENSE

API
---

.. module:: gridtools

.. autoclass:: LatLong

.. autoclass:: Grid

.. autofunction:: check_latlong

.. autofunction:: check_grid

.. autofunction:: distance


CLI Usage
---------

``gridtools`` has a basic CLI interface, which can be run using::

    $ python3 -m gridtools

It can be used with the following arguments::

    usage: gridtools [-h] [-g GRID] [-l LATLONG] [-d LOC LOC]

    arguments:
      -h, --help            show this help message and exit
      -g GRID, --cg GRID, --convgrid GRID
                            convert a grid locator to a lat/long pair
      -l LATLONG, --cl LATLONG, --convlatlong LATLONG
                            convert a lat/long pair to a grid locator
      -d LOC LOC, --dist LOC LOC, --distance LOC LOC
                            find the distance and bearing from one location to
                            another, specified with grid locator or lat/long
                            pair

.. NOTE:: if you get an error about ``expected 1 argument`` when you give a lat/long pair,
    try replacing the preceding space with an ``=``.
    For example: ``--cl=-12.123,43.21``.

