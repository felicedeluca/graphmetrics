##
# EU corresponds to the normalized standard deviation of the edge length.
##


import pygraphviz as pgv
import networkx as nx
import math

def compute_edge_length(edge):

    s1,t1 = edge

    x_source1 = float(s1.attr['pos'].split(",")[0])
    x_target1 = float(t1.attr['pos'].split(",")[0])

    y_source1 = float(s1.attr['pos'].split(",")[1])
    y_target1 = float(t1.attr['pos'].split(",")[1])

    curr_length = math.sqrt((x_source1 - x_target1)**2 + (y_source1 - y_target1)**2)

    return curr_length


def avg_edge_length(edges):

    sum_edge_length = 0.0
    edge_count = len(edges)

    for curr_id in range(0, edge_count):
        curr_edge = edges[curr_id]
        curr_length = compute_edge_length(curr_edge)
        sum_edge_length += curr_length

    avg_edge_len = sum_edge_length/edge_count
    return avg_edge_len

def uniformity_edge_length(G):

    edges = G.edges()
    edge_count = len(edges)
    avgEdgeLength = avg_edge_length(edges)
    tot_sum = 0.0

    for curr_id in range(0, len(edges)):

        curr_edge = edges[curr_id]
        curr_length = compute_edge_length(curr_edge)

        num = (curr_length-avgEdgeLength)**2
        den = edge_count*(avgEdgeLength**2)

        currValue = num/den
        tot_sum += currValue

    uniformity_e_len = math.sqrt(tot_sum)

    result = round(uniformity_e_len, 3)

    return result
