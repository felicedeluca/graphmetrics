#!/bin/bash

for file in "/Users/felicedeluca/Desktop/ogdfsugyama"/*.dot
do
  echo "$file"
  python3 metricscomputer.py "$file"  "/Users/felicedeluca/Desktop/ogdfsugyama/measures.txt"
done
