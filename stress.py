import networkx as nx
import math


def nodesArray(Gnx):

    nodes = []

    for sourceStr in nx.nodes(Gnx):

        nodes.append(sourceStr)

    return nodes

def euclidean_distance(source, target):

    x_source1 = float(source['pos'].split(",")[0])
    x_target1 = float(target['pos'].split(",")[0])

    y_source1 = float(source['pos'].split(",")[1])
    y_target1 = float(target['pos'].split(",")[1])

    geomDistance = math.sqrt((x_source1 - x_target1)**2 + (y_source1 - y_target1)**2)

    return geomDistance




def scale_graph(GD, alpha):

    H = GD.copy()

    for currVStr in nx.nodes(H):

        currV = H.node[currVStr]

        x = float(currV['pos'].split(",")[0])
        y = float(currV['pos'].split(",")[1])

        x = x * alpha
        y = y * alpha

        currV['pos'] = str(x)+","+str(y)

    return H


def computeScalingFactor(S, G=None):

    num = 0
    den = 0

    nodes = nodesArray(S)

    for i in range(0, len(nodes)):

        sourceStr = nodes[i]
        source = S.node[sourceStr]

        for j in range(i+1, len(nodes)):

            targetStr = nodes[j]

            if(sourceStr == targetStr):
                continue

            target = S.nodes[targetStr]

            graph_theoretic_distance = 0

            if(G is None):
                graph_theoretic_distance = nx.shortest_path_length(S, sourceStr, targetStr)
            else:
                graph_theoretic_distance = nx.shortest_path_length(G, sourceStr, targetStr)

            geomDistance = euclidean_distance(source, target)

            if (graph_theoretic_distance <= 0):
                continue

            weight = 1/(graph_theoretic_distance**2)

            num = num + (graph_theoretic_distance * geomDistance * weight)
            den = den + (weight * (geomDistance**2))

    scale = num/den

    return scale


def stress(S, G=None):
    '''Computes the strees of the layout <tt>S</tt> if the parameter <tt>G</tt>
    is passed it computes the stress of the layout <tt>S</tt>
    with respect the graph distances on <tt>G</tt>'''

    S_original = S.copy()

    alpha = 1

    if(G is None):
        alpha = computeScalingFactor(S_original)
    else:
        alpha = computeScalingFactor(S, G)


    S = scale_graph(S_original, alpha)

    vertices = nodesArray(S)

    stress = 0

    for i in range(0, len(vertices)):

        sourceStr = vertices[i]
        source = S.node[sourceStr]

        for j in range(i+1, len(vertices)):

            targetStr =  vertices[j]
            target = S.nodes[targetStr]

            graph_theoretic_distance = 0

            if(G is None):
                graph_theoretic_distance = nx.shortest_path_length(S, sourceStr, targetStr)
            else:
                graph_theoretic_distance = nx.shortest_path_length(G, sourceStr, targetStr)

            eu_dist = euclidean_distance(source, target)

            if (graph_theoretic_distance <= 0):
                continue

            delta_squared = (eu_dist - graph_theoretic_distance)**2
            weight = 1/(graph_theoretic_distance**2)
            stress = stress +  (weight * delta_squared)

    scale_graph(S, 1/alpha)


    stress = round(stress, 3)

    return stress
