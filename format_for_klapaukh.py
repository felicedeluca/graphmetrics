# format_for_klapaukh.py
#
# Input: graphfile layoutfile scale [outfile]
#        Where the graph and layout are stored as SVGs
#
# Output: An SVG with an adjacency matrix and node locations
#         padded with a bunch of boilerplate for an experiment
#         on force-directed layout that Klapaukh was running,
#         but we are not.

import os
import sys

import networkx as nx

########
# MATH #
########

def scale_layout(layout, scale):
	out = []
	for pt in layout:
		out.append(map(lambda x: (x+1)/2*scale, pt))
	return out


###################
# STRING BUILDING #
###################

def generate_boilerplate(w=800,h=800):
	out = """<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
"http://www.w3.org/TR/2001/REC-SVG-2010904/DTD/svg10.dtd">
<svg xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve"
width="{0}"
height="{1}"
viewBox = "0 0 {0} {1}"
zoomAndPan="disable">
<!--
elapsed: 1
filename: test.xml
width: {0}
height: {1}
iterations: 1
forcemode: 1
ke: 0
kh: 0
kl: 0
kw: 0
mass: 0
time: 0
coefficientOfRestitution: 0
mus: 0
muk: 0
kg: 0
wellMass: 0
edgeCharge: 0
finalKineticEnergy: 0
nodeWidth: 0
nodeHeight: 0
nodeCharge: 0
-
Start Graph:
""".format(w,h)
	return out


def format_layout_data_networkx(G):

	nodes = sorted(nx.nodes(G))
	edges = nx.edges(G)
	all_pos = nx.get_node_attributes(G, 'pos')
	# print(all_pos)

	out = str(len(nodes)) + "\n"

	for i in range(0, len(nodes)):

		source = nodes[i]
		curr_node_x = all_pos[source].split(",")[0]
		curr_node_y = all_pos[source].split(",")[1]

		line = str(curr_node_x) + " " + str(curr_node_y)

		for j in range(0, len(nodes)):
			target = nodes[j]
			if i == j:
				line += " 0"
				continue

			if ((source,target) in edges) or ((target,source) in edges):
				line += " 1"
			else:
				line += " 0"

		out += line + "\n"
	return out


def build_svg_networkx(G, scale):
	svg = generate_boilerplate(scale, scale)
	svg += format_layout_data_networkx(G)
	svg += "</svg>"
	return svg

def write_svg(filename, svg):
	if filename != None:
		with open(filename, 'w') as f:
			f.write(svg)
	else:
		print(svg)
