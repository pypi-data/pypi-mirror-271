#!/usr/bin/env python
# try out the pyolex module and make a list of towlines

import pyolex
import pandas as pd
import os
import argparse

def make_towline(start_lat, start_lon, stop_lat, stop_lon):
    print("start", start_lat)
    start_coord = pyolex.DecimalDegreeCoord(start_lat, start_lon)
    stop_coord = pyolex.DecimalDegreeCoord(stop_lat, stop_lon)
    
    print(start_coord)

    return pyolex.TowlineObject(plotset=1,linecolor=pyolex.Color.RED, tow_start_dd=start_coord, tow_stop_dd=stop_coord)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputfile', type=str, required=True)
    parser.add_argument('--gearcondition_less_than', type=int, required=True)
    args = parser.parse_args()
    print('Input biotic file:,', args.inputfile)
    print('Selected gearcondition:,', args.gearcondition_less_than)

    input_filename = args.inputfile #'fishstation-HH20.txt'
    gearcondition_less_than = args.gearcondition_less_than # Select gearcondition 1 and 2 - 3 and up is damaged

    bottomtrawl_gear_codes = [3270, 3271] # These are bottom-trawl-codes
    bottomtrawl_gear_condition = [1, 2, 3, 4, 5, 6] # These are conditions after trawling, 3 and above indicates damage

    base = os.path.splitext(input_filename)[0]
    output_filename = base + '.rte'

    output_olex_file = open(output_filename, 'w', encoding = "ISO-8859-1", newline='\r\n')
    output_olex_file.write("Ferdig forenklet")

    df = pd.read_csv(input_filename, index_col=0, sep='\t', encoding = "ISO-8859-1")


    rslt_df = df.loc[(df['gearcondition'] < gearcondition_less_than) & (df['gear'].isin(bottomtrawl_gear_codes))] # Select rows with gear-condition below 3 and is a bottom-trawl
    rslt_df = rslt_df.reset_index() # Reset indexes
    print(rslt_df[['latitudestart',	'longitudestart',	'latitudeend',	'longitudeend', 'gearcondition', 'gear']]) # , 'stationcomment'

    for index, row in rslt_df.iterrows():
        print(index, row['latitudestart'],	row['longitudestart'],	row['latitudeend'],	row['longitudeend'], row['gearcondition'], row['gear']) # , row['stationcomment']
        towstr = make_towline(row['latitudestart'],row['longitudestart'],row['latitudeend'],row['longitudeend'])
        output_olex_file.write("\r\n")
        output_olex_file.write(str(towstr))
        print(f'Wrote towline {index} to file')
    output_olex_file.close()

if __name__=='__main__':
    main()