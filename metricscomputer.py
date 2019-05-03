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


graphpath = sys.argv[1]
outputTxtFile = sys.argv[2]

input_file_name = os.path.basename(graphpath)
graph_name = input_file_name.split(".")[0]

G = nx_read_dot(graphpath)
G = nx.Graph(G)


cmds=[]
all = False

if len(sys.argv) > 3 :
    cmds = sys.argv[3].split(",")
else:
    # Compute all measures
    all = True


cr = ('cr' in cmds) # crossings
ue =  ('ue' in cmds) # edge length uniformity
st =  ('st' in cmds) # stress
np =  ('np' in cmds) # neighbors_preservation
lblbb =  ('lblbb' in cmds) #label to boundingBox ratio
lblarea =  ('lblarea' in cmds) #labels total area
bb =  ('bb' in cmds) #bounding box
upflow =  ('upflow' in cmds) #upward flow

output_txt = "Metrics for " + graph_name + "\n"
output_txt = nx.info(G) + "\n"

csv_head_line = "filename;"
csv_line = graph_name+";"


if cr or all:
    crossings_val = crossings.count_crossings(G)
    output_txt +=  "CR: " + str(crossings_val) + "\n"
    csv_head_line += "CR;"
    csv_line += str(crossings_val) + ";"

if ue or all::
    uniedgelen_val = uniedgelen.uniformity_edge_length(G)
    output_txt += "UE: " + str(uniedgelen_val) + "\n"
    csv_head_line += "UE;"
    csv_line += str(uniedgelen_val) + ";"

if st or all::
    stress_val = stress.stress(G)
    output_txt += "ST: " + str(stress_val) + "\n"
    csv_head_line += "ST;"
    csv_line += str(stress_val) + ";"


if np or all::
    neigpres_val = neigpres.compute_neig_preservation(G)
    output_txt += "NP: " + str(neigpres_val) + "\n"
    csv_head_line += "NP;"
    csv_line += str(neigpres_val) + ";"

if lblbb or all::
    labelsBBRatio_val = labelsmeas.labelsBBRatio(G)
    output_txt += "lblbb: " + str(labelsBBRatio_val) + "\n"
    csv_head_line += "lblbb;"
    csv_line += str(labelsBBRatio_val) + ";"

if lblarea or all::
    totLabelsArea_val = labelsmeas.totLabelsArea(G)
    output_txt += "lblarea: " + str(totLabelsArea_val) + "\n"
    csv_head_line += "lblarea;"
    csv_line += str(totLabelsArea_val) + ";"

if bb or all::
    bbox_val = othermeas.boundingBox(G)
    output_txt += "BB: " + str(bbox_val) + "\n"
    csv_head_line += "BB;"
    csv_line += str(bbox_val) + ";"

if upflow:
    upflow_val = upwardflow.compute_upwardflow(G)
    output_txt += "upflow: " + str(upflow_val) + "\n"
    csv_head_line += "upflow;"
    csv_line += str(upflow_val) + ";"


csv_head_line += "\n"
csv_line += "\n"


print(output_txt)

exists = os.path.isfile(outputTxtFile)
if not exists:
    fh = open(outputTxtFile, 'w')
    fh.write(csv_head_line)

fh = open(outputTxtFile, 'a')
fh.write(csv_line)
