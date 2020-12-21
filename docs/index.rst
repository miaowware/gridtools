=========
gridtools
=========

A small Python library to convert between maidenhead grid locators and lat/long coördinates.

.. highlight:: none

.. toctree::
    :hidden:

    index

Installation
============

``gridtools`` requires Python 3.8 at minimum. Install by running::

    $ pip install gridtools

License
=======

Copyright 2020 classabbyamp, 0x5c

Released under the BSD 3-Clause License. See `LICENSE`_ for the full license text.

.. _LICENSE: https://github.com/miaowware/gridtools/blob/master/LICENSE

CLI Usage
=========

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

API
===

.. module:: gridtools

.. autoclass:: LatLong

.. autoclass:: Grid

.. autofunction:: check_latlong

.. autofunction:: check_grid

.. autofunction:: grid_distance

A Note on Precision
===================

Although this library outputs grid locators in extended square form by default, that is not always the best choice to use.
On HF, the most precision needed for most applications is a grid square (e.g. FN01).
On VHF and UHF, the most precision needed is usually a subsquare (e.g. FN01ca).
On microwave, you might need more precision, so one could use the extended square (FN01ca34).

Choose the format that best suits your needs when using this library.
Attributes :attr:`~.Grid.field`, :attr:`~.Grid.square`, :attr:`~.Grid.subsquare`, and :attr:`~.Grid.extended_square` are included to make that easier.
If you don't want to choose right away, :attr:`~.Grid.grid_elements` can give the grid locator in a handy tuple format.

For latitude and longitude, ``gridtools`` stores values as floats internally, and when providing strings, uses 6 digits of precision.
This is precise enough to recognise individual humans (`see here <https://en.wikipedia.org/wiki/Decimal_degrees#Precision>`_),
so it is probably overkill for the scale of a grid locator.
