#!/bin/bash

for file in "/Users/felicedeluca/Developer/UofA/gdcontest/dags_med/drawings/dotalgorithm"/*.dot
do
  echo "$file"
  python3 metricscomputer.py "$file"  "upflow,st" "/Users/felicedeluca/Developer/UofA/gdcontest/dags_med/drawings/dotalgorithm/measures.txt"
done
