from enum import Enum

class Symbol(Enum):
    BROWNCIRCLE = "Brunsirkel"
    YELLOWDANGER = "Gulfare"
    FISHINGNET_START = "Garnstart"
    FISHINGNET_STOP = "Garnstopp"

class Color(Enum):
    RED = "Rød"
    BLUE = "Blå"
    GREEN = "Grønn"
    PURPLE = "Lilla"
    BROWN = "Brun"
    BLACK = "Svart"

class RouteType(Enum):
    DEFAULT = "uten navn"
    QUICKCROSS = "Hurtigkryss"
    TOWLINE = "Slepestrek"