import sys
import os

import pygraphviz as pgv
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
from networkx.drawing.nx_agraph import read_dot as nx_read_dot

g_path = sys.argv[1]
outputpath = sys.argv[2]
g_name = os.path.basename(g_path).split(".")[0]


# Reading graph and subgraph
G = nx_read_dot(g_path)
# Remove Multiple Edges
if nx.is_directed(G):
    G = nx.DiGraph(G)
else:
    G = nx.Graph(G)

pos = nx.get_node_attributes(G, "pos")
labels = nx.get_node_attributes(G, "label")
fontSize = nx.get_node_attributes(G, "fontsize")
fontname = nx.get_node_attributes(G, 'fontname')

for v in nx.nodes(G):
    graphics = {'x' : float(pos[v].split(",")[0]),
                'y' : float(pos[v].split(",")[1]),
                'label' : labels[v],
                'type': 'rectangle',
                'raisedBorder':'0'}


    lblgraphics = {'text' : labels[v], 'fontSize':fontSize[v], 'fontName':fontname[v]}
    nx.set_node_attributes(G, {v:graphics}, "graphics")
    # nx.set_node_attributes(G, {v:labels[v]}, "label")
    # nx.set_node_attributes(G, {v:labels[v]}, "text")
    nx.set_node_attributes(G, {v:lblgraphics}, "LabelGraphics")

print(nx.info(G))
# G = set_graph_properties(G)
# print(nx.info(G))
nx.write_gml(G, outputpath)
# print(nx.info(G))
