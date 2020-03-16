#!/bin/bash

for file in "/Users/felicedeluca/Desktop/forestsDA"/*.dot
do
  echo "$file"
  python3 metricscomputer.py "$file"  "/Users/felicedeluca/Desktop/forestsDA/measures_sym.txt" "ue"
done
