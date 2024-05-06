from pyolex import *

def test_pyolex_utilities_decimal_degrees_to_decimal_minutes():
    assert decimal_degrees_to_decimal_minutes(DecimalDegreeCoord(61.6296187, 5.01738467), precision=7) == DecimalMinuteCoord(lat=3697.777122, lon=301.0430802)
    assert decimal_degrees_to_decimal_minutes(DecimalDegreeCoord(61.6296187, 5.01738467), precision=4) != DecimalMinuteCoord(lat=3697.777122, lon=301.0431)
    assert decimal_degrees_to_decimal_minutes(DecimalDegreeCoord(61.6296187, 5.01738467), precision=4) == DecimalMinuteCoord(lat=3697.7771, lon=301.0431)

def test_pyolex_utilities_decimal_minutes_to_decimal_degrees():
    assert decimal_minutes_to_decimal_degrees(DecimalMinuteCoord(lat=3697.777122, lon=301.0430802), precision=7) != DecimalDegreeCoord(61.6296187, 5.01738467)
    assert decimal_minutes_to_decimal_degrees(DecimalMinuteCoord(lat=3697.777122, lon=301.0430802), precision=7) == DecimalDegreeCoord(61.6296187, 5.0173847)