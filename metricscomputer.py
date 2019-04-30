import sys
import os

import pygraphviz as pgv
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
from networkx.drawing.nx_agraph import read_dot as nx_read_dot

import math

import stress as st
import neighbors_preservation as neigpres
import crossings as cr
import uniformity_edge_length as uniedgelen
import other_measures as othermeas
import labelsmeas

# import betametrics/zigzagness as zigzag
# import betametrics/continuity as continuity
# import betametrics/drawing_highwayness
# import betametrics/speed_on_network as speed_on_network
# import betametrics/vertexangularresolution as vertexangularresolution


graphpath = sys.argv[1]
outputTxtFile = sys.argv[2]

input_file_name = os.path.basename(graphpath)
graph_name = input_file_name.split(".")[0]



Gpgv = pgv.AGraph(graphpath)
G = nx_read_dot(graphpath)
G = nx.Graph(G)

crossings_val = -1#cr.count_crossings(G)
uniedgelen_val = -1 #uniedgelen.uniformity_edge_length(Gpgv)
stress_val = -1 #st.stress(G)
neigpres_val = -1 #neigpres.compute_neig_preservation(G)
labelsBBRatio_val = labelsmeas.labelsBBRatio(G)
totLabelsArea_val = labelsmeas.totLabelsArea(G)
bbox_val = othermeas.boundingBox(G)


crossings_str = "crossings: " + str(crossings_val)
uniformity_str = "uniformity edge length: "+  str(uniedgelen_val)
stress_str = "stress: "+ str(stress_val)
neigh_str = "neighbors preservation: " + str(neigpres_val)
bb_str = "bounding box: " + str(bbox_val)
labelsBBRatio_str = "lbls ratio: " +  str(labelsBBRatio_val)
totLabelsArea_str = "lbls area: " +  str(totLabelsArea_val)

# angular_str = "vertex angular resolution: "+ str(vertexangularresolution.compute(G))
#angular_avg_str = "vertex angular resolution (avg): "+ str(angres.avg_angular_resolution(G))
#vertex_degree_str = "max vertex degree: "+ str(othermeas.vertex_degree(G))

#aspect_ratio_str = "aspectRatio: "+ str(othermeas.aspectRatio(G))
#zigzagness_str = "zigzagness: " + str(zigzag.compute_zigzagness(G))
#continuity_str = "continuity: " + str(continuity.continuity(G))
#diameter_str = "diameter: " + str(othermeas.diameter(G))
#highway_coverage_str = "highway coverage: " + str(drawing_highwayness.highwayDrawingCoverage(G))
#highwayness_str = "highwayness: " + str(speed_on_network.highwayness(G))
#zigzagness_angle_str = "zigzagness angle: " + str(zigzag.compute_zigzagness_angle(G))


# multilevelstress_ratio_str = "multilevel stress ratio: "+ str(st.stress_multilevel_ratio(G, G))
# highwayness_ratio_str = "multilevel highwayness ratio: "+ str(speed_on_network.highwayness_multilevel_ratio(G, G))


output_txt = "Metrics for " + graph_name + "\n"
output_txt = nx.info(G) + "\n"
output_txt += crossings_str + "\n"
output_txt += uniformity_str + "\n"
output_txt += stress_str + "\n"
output_txt += neigh_str + "\n"
output_txt += bb_str + "\n"
output_txt += labelsBBRatio_str + "\n"
output_txt += totLabelsArea_str + "\n"

#output_txt += zigzagness_str + "\n"
#output_txt += highway_coverage_str + "\n"
#output_txt += highwayness_str + "\n"
#output_txt += multilevelstress_ratio_str + "\n"
#output_txt += highwayness_ratio_str + "\n"
#output_txt += zigzagness_angle_str + "\n"
# output_txt += angular_str + "\n"
# output_txt += vertex_degree_str + "\n"
# output_txt += diameter_str + "\n"
#output_txt += aspect_ratio_str + "\n"
#output_txt += longest_shortest_path_str + "\n"

print(output_txt)

csv_head_line = "filename;crossings;uniformity_edge_length;stress;neighbors_preservation;labelsratio;totLabelsArea;bbox\n"
csv_line = graph_name+";"+ str(crossings_val) + ";" + str(uniedgelen_val)+ ";" + str(stress_val) + ";" + str(neigpres_val) + ";" +  str(labelsBBRatio_val)+ ";" + str(totLabelsArea_val)+";"+str(bbox_val) + "\n"

exists = os.path.isfile(outputTxtFile)
if not exists:
    fh = open(outputTxtFile, 'w')
    fh.write(csv_head_line)

fh = open(outputTxtFile, 'a')
fh.write(csv_line)
