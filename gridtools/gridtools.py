"""
gridtools.py, part of gridtools
---
A small Python library to convert between maidenhead grid locators and lat/long coördinates.

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Union, Tuple
import re
import math


__all__ = ["Grid", "LatLong", "check_grid", "check_latlong", "grid_distance"]


# matches any valid 2-8 character grid
GRID_RE: re.Pattern = re.compile(r"[A-R]{2}(?:\d{2}(?:[A-X]{2}(?:\d{2})?)?)?", flags=re.IGNORECASE)

# grid squares are offset of the equator and prime meridian
OFFSET_LON = 180
OFFSET_LAT = 90
# fields are 20° by 10°
FLD_LON = 20
FLD_LAT = 10
# squares are 2° by 1°
SQ_LON = 2
SQ_LAT = 1
# subsquares are 5' by 2.5'
SSQ_LON = 5 / 60
SSQ_LAT = 2.5 / 60
# extended squares are 30" by 15"
ESQ_LON = 30 / 3600
ESQ_LAT = 15 / 3600
# fields and subsquares can be defined as an offset of A or a in ASCII
# because the characters A or a are the "zero" of those parts of a grid.
# this fact is very handy for converting numbers to letters.
FLD_ZERO = ord("A")
SSQ_ZERO = ord("a")


class LatLong:
    """Represents a latitude/longitude pair.

    :param lat: the latitude
    :type lat: Union[float, int]
    :param long: the longitude
    :type long: Union[float, int]
    """
    def __init__(self, lat: Union[float, int], long: Union[float, int]) -> None:
        self._lat: float = 0
        self._long: float = 0
        self.lat = float(lat)
        self.long = float(long)

    @property
    def lat(self) -> float:
        """
        :getter: gets the latitude of the object
        :rtype: float

        :setter: sets the latitude of the object
        :type: Union[float, int]
        :raises ValueError: if given an invalid latitude
        """
        return self._lat

    @lat.setter
    def lat(self, new_val: Union[float, int]) -> None:
        if check_latlong(new_val, self._long):
            self._lat = float(new_val)
        else:
            raise ValueError("Invalid latitude given. Must be between -90 and 90 degrees.")

    @property
    def long(self) -> float:
        """
        :getter: gets the longitude of the object
        :rtype: float

        :setter: sets the longitude of the object
        :type: Union[float, int]
        :raises ValueError: if given an invalid longitude
        """
        return self._long

    @long.setter
    def long(self, new_val: Union[float, int]) -> None:
        if check_latlong(self._lat, new_val):
            self._long = float(new_val)
        else:
            raise ValueError("Invalid longitude given. Must be between -180 and 180 degrees.")

    def __str__(self) -> str:
        return f"{self._lat:.6f}°, {self._long:.6f}°"

    def __repr__(self) -> str:
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__
        return f"<{module}.{qualname} object at {hex(id(self))}, lat={self.lat:.6f}, long={self.long:.6f}>"


class Grid:
    """Represents a maidenhead grid locator.

    :param input: the grid locator or a :class:`LatLong` object
    :type: Union[str, LatLong]
    """
    def __init__(self, input: Union[str, LatLong]):
        self._grid = ""
        self._latlong = LatLong(0, 0)
        if isinstance(input, str):
            self.grid = input
        else:
            self.latlong = input

    @property
    def grid(self) -> str:
        """
        :getter: gets the grid locator of the object
        :rtype: str

        :setter: sets the grid locator of the object
        :type: str
        :raises ValueError: if given an invalid grid locator
        """
        return self._grid

    @grid.setter
    def grid(self, new_val: str) -> None:
        if check_grid(new_val):
            self._grid = self.__format_grid(new_val)
            self._latlong = self.__calc_latlong(self._grid)
        else:
            raise ValueError("Invalid grid locator given. Must be in the format 'AA##aa##' (1-4 pairs).")

    @property
    def elements(self) -> Tuple[str, ...]:
        """
        :getter: gets the grid locator of the object, divided into each pair.
        :rtype: Tuple[str, `...`]
        """
        return tuple([self.grid[i:i + 2] for i in range(0, len(self.grid), 2)])

    @property
    def field(self) -> str:
        """
        :getter: gets the field of the grid locator of the object, e.g. ``FN``
        :rtype: str
        """
        return self._grid[:2]

    @property
    def square(self) -> str:
        """
        :getter: gets the square of the grid locator of the object, e.g. ``FN01``
        :rtype: str
        """
        return self._grid[:4]

    @property
    def subsquare(self) -> str:
        """
        :getter: gets the subsquare of the grid locator of the object, e.g. ``FN01ce``
        :rtype: str
        """
        return self._grid[:6]

    @property
    def extended_square(self) -> str:
        """This is a read-only alias to :attr:`.grid`.

        :getter: gets the extended square of the grid locator of the object, e.g. ``FN01ce24``
        :rtype: str
        """
        return self._grid

    @property
    def latlong(self) -> LatLong:
        """
        :getter: gets the lat/long pair of the center of the grid locator of the object
        :rtype: LatLong

        :setter: sets the lat/long pair of the object
        :type: LatLong
        """
        return self._latlong

    @latlong.setter
    def latlong(self, new_val: LatLong) -> None:
        self._latlong = new_val
        self._grid = self.__calc_grid(self._latlong)

    @property
    def lat(self) -> float:
        """
        :getter: gets the latitude of the object
        :rtype: float

        :setter: sets the latitude of the object
        :type: Union[float, int]
        :raises ValueError: if given an invalid latitude
        """
        return self.latlong.lat

    @lat.setter
    def lat(self, new_val: Union[float, int]) -> None:
        self._latlong.lat = new_val
        self._grid = self.__calc_grid(self._latlong)

    @property
    def long(self) -> float:
        """
        :getter: gets the longitude of the object
        :rtype: float

        :setter: sets the longitude of the object
        :type: Union[float, int]
        :raises ValueError: if given an invalid longitude
        """
        return self.latlong.long

    @long.setter
    def long(self, new_val: Union[float, int]) -> None:
        self._latlong.long = new_val
        self._grid = self.__calc_grid(self._latlong)

    def __calc_grid(self, latlong: LatLong):
        grid = ""
        lon = latlong.long + OFFSET_LON
        lat = latlong.lat + OFFSET_LAT

        # TODO: precision?
        # noqa - algo from: https://web.archive.org/web/20190613135648/http://n1sv.com/PROJECTS/How%20to%20calculate%20your%208-digit%20grid%20square.pdf
        grid = ""
        grid += chr(FLD_ZERO + int(lon // FLD_LON))
        grid += chr(FLD_ZERO + int(lat // FLD_LAT))
        grid += str(int(lon % FLD_LON // SQ_LON))
        grid += str(int(lat % FLD_LAT // SQ_LAT))
        grid += chr(SSQ_ZERO + int(lon % FLD_LON % SQ_LON // SSQ_LON))
        grid += chr(SSQ_ZERO + int(lat % FLD_LAT % SQ_LAT // SSQ_LAT))
        grid += str(int(lon % FLD_LON % SQ_LON % SSQ_LON // ESQ_LON))
        grid += str(int(lat % FLD_LAT % SQ_LAT % SSQ_LAT // ESQ_LAT))

        # no need to run __format_grid() because the algo for calculation formats it properly
        return grid

    def __calc_latlong(self, grid: str):
        grid_len = len(grid)

        # noqa - algo (in reverse) from: https://web.archive.org/web/20190613135648/http://n1sv.com/PROJECTS/How%20to%20calculate%20your%208-digit%20grid%20square.pdf
        # field
        lon: float = (ord(grid[0]) - FLD_ZERO) * FLD_LON - OFFSET_LON
        lat: float = (ord(grid[1]) - FLD_ZERO) * FLD_LAT - OFFSET_LAT

        if grid_len > 2:
            # square
            lon += int(grid[2]) * SQ_LON
            lat += int(grid[3]) * SQ_LAT

            if grid_len > 4:
                # subsqare
                lon += (ord(grid[4]) - SSQ_ZERO) * SSQ_LON
                lat += (ord(grid[5]) - SSQ_ZERO) * SSQ_LAT

                if grid_len == 8:
                    # extended square
                    lon += int(grid[6]) * ESQ_LON
                    lat += int(grid[7]) * ESQ_LAT

                    # move to center of extended square
                    lon += ESQ_LON / 2
                    lat += ESQ_LAT / 2
                    return LatLong(lat, lon)
                # move to center of subsquare
                lon += SSQ_LON / 2
                lat += SSQ_LAT / 2
                return LatLong(lat, lon)
            # move to center of square
            lon += SQ_LON / 2
            lat += SQ_LAT / 2
            return LatLong(lat, lon)
        # move to the center of field
        lon += FLD_LON / 2
        lat += FLD_LAT / 2
        return LatLong(lat, lon)

    def __format_grid(self, grid: str) -> str:
        return grid[:2].upper() + grid[2:].lower()

    def __str__(self) -> str:
        return self.grid

    def __repr__(self) -> str:
        type_ = type(self)
        module = type_.__module__
        qualname = type_.__qualname__
        return f"<{module}.{qualname} object at {hex(id(self))}, grid={self.grid}, latlong={self.latlong}>"


def check_grid(input: str) -> bool:
    """Check if a string is a valid 2-8 character maidenhead grid.

    :param input: the string to check
    :type input: str
    :return: ``True`` if valid, ``False`` if not.
    :rtype: bool
    """
    return True if re.match(GRID_RE, input) else False


def check_latlong(lat: Union[float, int], long: Union[float, int]) -> bool:
    """Check if a pair of 2 float or ints is a valid lat/long pair.

    :param lat: the latitude value to check
    :type lat: Union[float, int]
    :param long: the longitude value to check
    :type long: Union[float, int]
    :return: ``True`` if valid, ``False`` if not.
    :rtype: bool
    """
    return True if -90 <= lat <= 90 and -180 <= long <= 180 else False


def grid_distance(location1: Union[Grid, LatLong], location2: Union[Grid, LatLong]) -> Tuple[float, float]:
    """Finds the great circle distance and bearing between two Grid or LatLong objects.

    :param location1: the location **from** which to measure
    :type location1: Union[Grid, LatLong]
    :param location2: the location **to** which to measure
    :type location2: Union[Grid, LatLong]
    :return: the great circle distance (in kilometres) and the bearing (in degrees) from location1 to location2
    :rtype: Tuple[float, float]
    """
    RADIUS = 6371
    dist: float = 0
    bearing: float = 0
    loc1 = location1.latlong if isinstance(location1, Grid) else location1
    loc2 = location2.latlong if isinstance(location2, Grid) else location2

    # Using the Haversine formula
    d_lat = math.radians(loc2.lat - loc1.lat)
    d_lon = math.radians(loc2.long - loc1.long)

    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(loc1.lat))
         * math.cos(math.radians(loc2.lat))
         * math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist = RADIUS * c

    # bearing
    y_dist = math.sin(math.radians(loc2.long - loc1.long)) * math.cos(math.radians(loc2.lat))
    x_dist = (math.cos(math.radians(loc1.lat))
              * math.sin(math.radians(loc2.lat))
              - math.sin(math.radians(loc1.lat))
              * math.cos(math.radians(loc2.lat))
              * math.cos(math.radians(loc2.long - loc1.long)))
    bearing = (math.degrees(math.atan2(y_dist, x_dist)) + 360) % 360

    return dist, bearing
