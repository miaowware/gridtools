"""
gridtools commandline interface
---
Copyright 2020 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


import argparse
from typing import List, Union

import gridtools


parser = argparse.ArgumentParser(prog="gridtools",
                                 description=("Convert between maidenhead grid locators and latitude/longitude, "
                                              "as well as compute the great circle distance and bearing "
                                              "between two grid locators or lat/long pairs."
                                              "\n\nNOTE: if you get an error about 'expected 1 argument' "
                                              "when you give a lat/long pair, try replacing the preceding space with "
                                              "an '='. For example: --cl=-12.123,43.21"))
parser.add_argument("-g", "--cg", "--convgrid", required=False, type=gridtools.Grid, dest="grid", nargs=1,
                    help="convert a grid locator to a lat/long pair")
parser.add_argument("-l", "--cl", "--convlatlong", required=False, type=str, dest="latlong", nargs=1,
                    help="convert a lat/long pair to a grid locator")
parser.add_argument("-d", "--dist", "--distance", required=False, type=str, metavar="LOC", dest="distance", nargs=2,
                    help=("find the distance and bearing from one location to another, "
                          "specified with grid locator or lat/long pair"))
args = parser.parse_args()

if args.grid:
    grid = args.grid[0]
    print(f"{grid} = {grid.latlong}")

if args.latlong:
    latlong = args.latlong[0]
    try:
        latlong_sp = latlong.split(",")
        lat = float(latlong_sp[0])
        long = float(latlong_sp[1])
    except ValueError:
        print(f"Could not parse {latlong}.\nUse the format [lat],[long].\nExample: -43.267,23.829")
    else:
        latlong = gridtools.LatLong(lat, long)
        grid = gridtools.Grid(latlong)
        print(f"{latlong} = {grid}")

if args.distance and len(args.distance) == 2:
    loc_objs: List[Union[gridtools.Grid, gridtools.LatLong]] = []
    for loc in args.distance:
        try:
            loc_objs.append(gridtools.Grid(loc))
        except ValueError:
            try:
                latlong_sp = loc.split(",")
                lat = float(latlong_sp[0])
                long = float(latlong_sp[1])
                loc_objs.append(gridtools.LatLong(lat, long))
            except ValueError:
                print(f"Could not parse {loc}.\nFor grids, use the AA00aa00 format (2-8 characters).\n"
                      "For lat/long pairs, use the format [lat],[long].\nExamples: FM19al -43.267,23.829")
                break

    if len(loc_objs) == 2:
        dist, bearing = gridtools.grid_distance(*loc_objs)
        print(f"The distance from {loc_objs[0]} to {loc_objs[1]} is {dist:.1f} km at bearing {bearing:.1f}°")
