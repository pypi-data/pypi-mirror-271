#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
FILES="./data/*"
for f in $FILES 
do
  echo "Processing $f file..."
  python3 example_csv2towlines.py --inputfile "$f" --gearcondition_less_than 2
done