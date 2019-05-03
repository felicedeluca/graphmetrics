#!/bin/bash

for file in "/Users/felicedeluca/Developer/UofA/gdcontest/dags_med/drawings/dotalgorithm"/*.dot
do
  echo "$file"
  python3 metricscomputer.py "$file"  "/Users/felicedeluca/Developer/UofA/gdcontest/dags_med/drawings/dotalgorithm/measures.txt" "upflow,st"
done
