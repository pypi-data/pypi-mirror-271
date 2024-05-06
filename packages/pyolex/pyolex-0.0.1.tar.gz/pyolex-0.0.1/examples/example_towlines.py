#!/usr/bin/env python
# try out the pyolex module and make a list of towlines

import pyolex

def make_towline(start_lat, start_lon, stop_lat, stop_lon):
    print("start", start_lat)
    start_coord = pyolex.DecimalDegreeCoord(start_lat, start_lon)
    stop_coord = pyolex.DecimalDegreeCoord(stop_lat, stop_lon)
    
    print(start_coord)

    return pyolex.TowlineObject(plotset=1,linecolor=pyolex.Color.RED, tow_start_dd=start_coord, tow_stop_dd=stop_coord)

def main():
    towline_data = [
        [61.6296187, 5.01738467, 61.6297187, 5.01739467],
        [62.6396187, 5.11738467, 62.6397187, 5.12739467]
    ]

    print("Ferdig forenklet")
    for towline in towline_data:
        towstr = make_towline(towline[0],towline[1],towline[2],towline[3])
        print(towstr)
        print()

if __name__=='__main__':
    main()