# Author:
# Felice De felicedeluca
# www.github.com/felicedeluca


import networkx as nx
import os
import math
import time

from subprocess import Popen, PIPE


import format_for_klapaukh

import sys
# from networkx.drawing.nx_agraph import write_dot
from networkx.drawing.nx_agraph import read_dot as nx_read_dot

def rotate(G, angle):
	angle = math.radians(angle)
	pos_dict = nx.get_node_attributes(G, "pos")
	for currVertex in nx.nodes(G):
		x = float(pos_dict[currVertex].split(",")[0])
		y = float(pos_dict[currVertex].split(",")[1])
		x_rot = x*math.cos(angle) - y*math.sin(angle)
		y_rot = x*math.sin(angle) + y*math.cos(angle)
		pos_dict[currVertex] = str(x_rot) + "," + str(y_rot)
	nx.set_node_attributes(G, pos_dict, "pos")
	return G

def rotate_to_ideal_symmetry(G):
	angle = compute_symmetry(G)[1]
	G = rotate(G, angle)
	angle = compute_symmetry(G)[1]
	return angle


def get_symmetric_score(G):
	score = compute_symmetry(G)
	return score[0]


def get_reflectional_score_string(metrics):

	s = [s.strip() for s in metrics.splitlines()]

	desired = [
		"Mirror Symmetry",
		# "Translational Symmetry",
		# "Rotational Symmetry",
		"Angle Deviation From Ideal"
	]

	labels = s[0].split(',')
	values = s[1].split(',')

	out = []
	results = []

	for prop in desired:
		idx = labels.index(prop)
		out.append(float(values[idx]))
	result = ",".join(map(str,out))

	return out

def compute_symmetry(G):
	'''
	Computes the symmetry of the given graph with respect K metric.
	G: the graph in networkx format
	returns: a list of two values:
	 		a score in the range [0, 1] of symmetricness
	        where
	        0 is non symmetric
	        1 is symmetric

			the `Angle Deviation From Ideal' symmetry computed by the metric
	'''

	ts = time.time()

	svgfullpath = "temp"+str(ts)+".svg"

	#  Remove files if exist
	if os.path.exists(svgfullpath):
	    os.remove(svgfullpath)

	scale = 1
	svg = format_for_klapaukh.build_svg_networkx(G, scale)
	format_for_klapaukh.write_svg(svgfullpath, svg)

	# invoke the java pachage
	p = Popen(['java', '-jar', 'kAnalyzer.jar', svgfullpath], stdout=PIPE)
	output = p.stdout.read()

	output_str = output.decode('utf-8')
	score = get_reflectional_score_string(output_str)

	 # Remove the created temp files if existf
	if os.path.exists(svgfullpath):
	    os.remove(svgfullpath)

	return score
