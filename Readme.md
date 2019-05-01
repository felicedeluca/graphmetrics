# Intro
Compute the most popular aestethic criteria for a graph drawing.

The input format is a DOT file (see https://en.wikipedia.org/wiki/DOT_(graph_description_language) for more information). To covert a graph into a DOT file please check some graph converters in 'graphconverter' folder or use another tool like NetworkX to read and write a dot file.

This project uses NetworkX (https://networkx.github.io) to handle graphs and reading/writing files. Also it needs pygraphviz to manage the DOT format (https://pygraphviz.github.io).

The project is tested on python3 

# Computed Metrics
* Angular resolution
* Average angular resolution
* Crossings
* Edge length unifromity
* Bounding box
* Aspect ratio
* Stress
* Neighbors preservation

## Future improvements (needed)
Currently the crossing counting is rather slow, it checks each pair of edges. A better way to count the crossings, such as a sweep-line algorithm, would speed-up the computation.
