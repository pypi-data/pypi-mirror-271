import time
from typing import NamedTuple

from .enumerations import Symbol, Color, RouteType

class DecimalDegreeCoord(NamedTuple):
    lat: float
    lon: float

class DecimalMinuteCoord(NamedTuple):
    lat: float
    lon: float

def decimal_degrees_to_decimal_minutes(DecimalDegreeCoord, precision=7):
    # Check input validity
    if -90 < DecimalDegreeCoord.lat < 90:
        pass
    else:
        raise ValueError('DD Lat invalid, must be between -90 and 90. It was', DecimalDegreeCoord.lat)

    # Check input validity
    if -180 < DecimalDegreeCoord.lon < 180:
        pass
    else:
        raise ValueError('DD Lon invalid, must be between -180 and 180. It was', DecimalDegreeCoord.lon)

    min_lat = DecimalDegreeCoord.lat*60
    min_lon = DecimalDegreeCoord.lon*60
    min_lat_rounded = round(min_lat, precision)
    min_lon_rounded = round(min_lon, precision)
    return DecimalMinuteCoord(min_lat_rounded, min_lon_rounded)

def decimal_minutes_to_decimal_degrees(DecimalMinuteCoord, precision=7):
    # Check input validity
    if -5400 < DecimalMinuteCoord.lat < 5400:
        pass
    else:
        raise ValueError('MIN Lat invalid, must be between -5400 and 5400. It was', DecimalMinuteCoord.lat)

    # Check input validity
    if -10800 < DecimalMinuteCoord.lon < 10800:
        pass
    else:
        raise ValueError('MIN Lon invalid, must be between -10800 and 10800. It was', DecimalMinuteCoord.lon)

    dd_lat = DecimalMinuteCoord.lat/60
    dd_lon = DecimalMinuteCoord.lon/60
    dd_lat_rounded = round(dd_lat, precision)
    dd_lon_rounded = round(dd_lon, precision)
    return DecimalDegreeCoord(dd_lat_rounded, dd_lon_rounded)

class Waypoint:
    def __init__(self, lat, lon, precision=7, creation_time=time.time(), symbol=Symbol.BROWNCIRCLE):
        self._dd_coord = DecimalDegreeCoord(lat, lon)
        self._display_precision = precision
        self._creation_time = int(creation_time)
        self._symbol = symbol

        self._min_coord = decimal_degrees_to_decimal_minutes(self._dd_coord, self._display_precision)
    
    def __str__(self):
        return '{0._min_coord.lat!s} {0._min_coord.lon!s} {0._creation_time!s} {0._symbol.value!s}'.format(self)

class NamedWaypoint(Waypoint):
    def __init__(self, lat, lon, name, precision=7, creation_time=time.time(), symbol=Symbol.BROWNCIRCLE):
        super().__init__(lat, lon, precision=7, creation_time=time.time(), symbol=Symbol.BROWNCIRCLE)
        self._name = name

    def __str__(self):
        return '{0}\nNavn {1._name!s}'.format(super().__str__(), self)

class PlotlayerObject:
    def __init__(self, plotset=1):
        self._plotset = plotset

    def __str__(self):
        return 'Plottsett {0._plotset!s}'.format(self)

class RouteObject(PlotlayerObject):
    def __init__(self, plotset=1):
        super().__init__(plotset=1)
        self._routetype = RouteType.DEFAULT

    def __str__(self): # Optional arguments: Rutetype, Linjefarge
        return 'Rute {1._routetype.value!s}{0}'.format(super().__str__(), self)

class TowlineObject(PlotlayerObject): # A towline can have more than two waypoints!
    def __init__(self, plotset=1, linecolor=Color.RED, tow_start_dd=DecimalDegreeCoord, tow_middle_section="", tow_stop_dd=DecimalDegreeCoord):
        super().__init__(plotset=1)
        self._routetype = RouteType.TOWLINE
        self._linecolor = linecolor

        self._tow_start_waypoint = Waypoint(tow_start_dd.lat, tow_start_dd.lon, precision=7, symbol=Symbol.FISHINGNET_START)
        self._tow_stop_waypoint = Waypoint(tow_stop_dd.lat, tow_stop_dd.lon, precision=7, symbol=Symbol.FISHINGNET_STOP)

    def __str__(self):
        return 'Rute {1._routetype.value!s}\nRutetype Strek\nLinjefarge {1._linecolor.value!s}\n{0}\n{1._tow_start_waypoint!s}\n{1._tow_stop_waypoint!s}'.format(super().__str__(), self)