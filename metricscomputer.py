import sys
import os

import networkx as nx
from networkx.drawing.nx_agraph import write_dot
from networkx.drawing.nx_agraph import read_dot as nx_read_dot

import math

import stress
import neighbors_preservation as neigpres
import crossings
import uniformity_edge_length as uniedgelen
import other_measures as othermeas
import labelsmeas
import upwardflow
import ksymmetry


graphpath = sys.argv[1]
outputTxtFile = sys.argv[2]

input_file_name = os.path.basename(graphpath)
graph_name = input_file_name.split(".")[0]

G = nx_read_dot(graphpath)


largest_cc = max(nx.connected_components(G), key=len)

G = G.subgraph(largest_cc)



# Remove Multiple Edges
if nx.is_directed(G):
    G = nx.DiGraph(G)
else:
    G = nx.Graph(G)

G = nx.Graph(G)
cmds=[]
all = False

print(sys.argv)

if len(sys.argv) > 3 :
    cmds = sys.argv[3].split(",")
else:
    # Compute all measures
    all = True


cr = ('cr' in cmds) # crossings
ang_res = ('ar' in cmds) # crossings angular resolution
ue =  ('ue' in cmds) # edge length uniformity
st =  ('st' in cmds) # stress
np =  ('np' in cmds) # neighbors_preservation
lblbb =  ('lblbb' in cmds) #label to boundingBox ratio
lblarea =  ('lblarea' in cmds) #labels total area
bb =  ('bb' in cmds) #bounding box
lblo = ('lblo' in cmds) #labels overlaping area
upflow =  ('upflow' in cmds) #upward flow
area =  ('area' in cmds) #upward flow
symmetry = ('sym' in cmds) # reflectional symmetry

output_txt = "Metrics for " + graph_name + "\n"
output_txt = nx.info(G) + "\n"
print(output_txt)

csv_head_line = "filename;"
csv_line = graph_name+";"

if cr or ang_res or all:
    crss = crossings.count_crossings(G, ignore_label_edge_cr=False)

    if cr or all:
        crossings_val = len(crss)
        output_line = "CR: " + str(crossings_val)
        output_txt += output_line + "\n"
        csv_head_line += "CR;"
        csv_line += str(crossings_val) + ";"
        print(output_line)

    if ang_res or all:

        min_angle = float('inf')
        for crossing in crss:
            (edge1, edge2, intersection_point, crossing_angle) = crossing
            min_angle = min(min_angle, crossing_angle)

        value = min_angle
        output_line =  "AR: " + str(value)
        output_txt += output_line + "\n"
        csv_head_line += "AR;"
        csv_line += str(value) + ";"
        print(output_line)


if ue or all:
    uniedgelen_val = uniedgelen.uniformity_edge_length(G)
    output_line =  "UE: " + str(uniedgelen_val)
    output_txt += output_line + "\n"
    csv_head_line += "UE;"
    csv_line += str(uniedgelen_val) + ";"
    print(output_line)


if st or all:
    stress_val = stress.stress(G, weighted=False)
    output_line =  "ST: " + str(stress_val)
    output_txt += output_line + "\n"
    csv_head_line += "ST;"
    csv_line += str(stress_val) + ";"
    print(output_line)



if np or all:
    neigpres_val = neigpres.compute_neig_preservation(G, weighted=False)
    output_line =  "NP: " + str(neigpres_val)
    output_txt += output_line + "\n"
    csv_head_line += "NP;"
    csv_line += str(neigpres_val) + ";"
    print(output_line)

if lblbb:
    labelsBBRatio_val = labelsmeas.labelsBBRatio(G)
    output_line =  "lblbb: " + str(labelsBBRatio_val)
    output_txt += output_line + "\n"
    csv_head_line += "lblbb;"
    csv_line += str(labelsBBRatio_val) + ";"
    print(output_line)


if lblarea:
    totLabelsArea_val = labelsmeas.totLabelsArea(G)
    output_line =  "lblarea: " + str(totLabelsArea_val)
    output_txt += output_line + "\n"
    csv_head_line += "lblarea;"
    csv_line += str(totLabelsArea_val) + ";"
    print(output_line)


if bb or all:
    bbox_val = othermeas.boundingBox(G)
    output_line =  "BB: " + str(bbox_val)
    output_txt += output_line + "\n"
    csv_head_line += "BB;"
    csv_line += str(bbox_val) + ";"
    print(output_line)

if area or all:
    # G = normalize_grid.normalize_grid(G)
    # G = normalize_grid.normalize_grid(G)
    (width, height) = othermeas.boundingBox(G)
    value = width*height
    output_line =  "area: " + str(value)
    output_txt += output_line + "\n"
    csv_head_line += "area;"
    csv_line += str(value) + ";"
    print(output_line)

if lblo:
    value = labelsmeas.totLabelsOverlappingArea(G)
    output_line =  "lblo: " + str(value)
    output_txt += output_line + "\n"
    csv_head_line += "lblo;"
    csv_line += str(value) + ";"
    print(output_line)

if upflow:
    upflow_val = upwardflow.compute_upwardflow(G)
    output_line =  "upflow: " + str(upflow_val)
    output_txt += output_line + "\n"
    csv_head_line += "upflow;"
    csv_line += str(upflow_val) + ";"
    print(output_line)

if symmetry:
    value = ksymmetry.get_symmetric_score(G)
    output_line =  "symmetry: " + str(value)
    output_txt += output_line + "\n"
    csv_head_line += "symmetry;"
    csv_line += str(value) + ";"
    print(output_line)


csv_head_line += "\n"
csv_line += "\n"

exists = os.path.isfile(outputTxtFile)
if not exists:
    fh = open(outputTxtFile, 'w')
    fh.write(csv_head_line)

fh = open(outputTxtFile, 'a')
fh.write(csv_line)
