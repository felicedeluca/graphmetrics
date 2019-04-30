import networkx as nx

import math

def boundingBox(G):

    all_pos = nx.get_node_attributes(G, "pos").values()

    coo_x = sorted([float(p.split(",")[0]) for p in all_pos])
    coo_y = sorted([float(p.split(",")[1]) for p in all_pos])

    min_x = float(coo_x[0])
    max_x = float(coo_x[-1])

    min_y = float(coo_y[0])
    max_y = float(coo_y[-1])

    width = abs(max_x - min_x)
    height = abs(max_y - min_y)

    return (width, height)

def totLabelsArea(G, labelsscalingfactor=72):
    '''Computes the minimum area covered by non overlapping labels
    It requires width and height for each vertex. The labels are supposed to be
    rectangular. Before computing the value, each label is scaled by
    <tt>labelsscalingfactor</tt> in order to reflect the printed size of the label.
    The default value of <tt>labelsscalingfactor</tt> is <tt>72</tt>'''

    widths=nx.get_node_attributes(G, "width")
    heights=nx.get_node_attributes(G, "height")

    tot_area = 0

    for v in widths.keys():

        curr_area = (float(widths[v])*labelsscalingfactor)*(float(heights[v])*labelsscalingfactor)
        tot_area+=curr_area

    return tot_area



def labelsBBRatio(G):
    '''
    Computes the ratio between the minimum area occupied by non overlapping labels and
    the actual area of the drawings.
    '''

    bb = boundingBox(G)
    bb_area = bb[0]*bb[1]

    l_area = totLabelsArea(G)

    aspectRatio = l_area/bb_area

    return aspectRatio


def diameter(G):

    return nx.diameter(G)
