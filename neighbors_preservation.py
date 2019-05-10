import pygraphviz as pgv
import networkx as nx
import math


def euclidean_distance(source, target):
    x_source1 = float(source['pos'].split(",")[0])
    x_target1 = float(target['pos'].split(",")[0])

    y_source1 = float(source['pos'].split(",")[1])
    y_target1 = float(target['pos'].split(",")[1])

    geomDistance = math.sqrt((x_source1 - x_target1)**2 + (y_source1 - y_target1)**2)

    return geomDistance


def find_graph_closest_nodes(Gnx, r_g, sourceStr):

    closest = []

    vertices = list(nx.nodes(Gnx))
    source = Gnx.node[sourceStr]

    for i in range(0, len(vertices)):

        targetStr = vertices[i]
        target = Gnx.node[targetStr]

        if(target == source):
            continue

        graph_theoretic_distance = len(nx.shortest_path(Gnx, sourceStr, targetStr, weight="weight"))

        if(graph_theoretic_distance <= r_g):
            closest.append(targetStr)

    return closest


def find_space_closest_nodes(Gnx, k_i, sourceStr):

    closest = []
    vertices = list(nx.nodes(Gnx))
    source = Gnx.node[sourceStr]

    closest_dict = dict()

    for i in range(0, len(vertices)):

        targetStr = vertices[i]
        target = Gnx.node[targetStr]

        if(target == source):
            continue

        space_distance = euclidean_distance(source, target)

        closest_dict[targetStr] = space_distance


    res = list(sorted(closest_dict, key=closest_dict.__getitem__, reverse=False))

    closest = res[:k_i+1]

    return closest




def compute_neig_preservation(G, weighted=True):

    # converting weights in float
    all_weights_n = nx.get_node_attributes(G, "weight")
    for nk in all_weights_n.keys():
        all_weights_n[nk] = float(all_weights_n[nk])
    nx.set_node_attributes(G, all_weights_n, "weight")

    all_weights_e = nx.get_edge_attributes(G, "weight")
    for ek in all_weights_e.keys():
        all_weights_e[ek] = float(all_weights_e[ek])
    nx.set_edge_attributes(G, all_weights_e, "weight")

    all_sp = None
    if(weighted):
        all_sp = nx.shortest_path(G, weight="weight")
    else:
        all_sp = nx.shortest_path(G)

    r_g = 3


    vertices = list(nx.nodes(G))

    sum = 0

    for i in range(0, len(vertices)):

        sourceStr = vertices[i]
        source = G.node[sourceStr]

        graph_neighbors = find_graph_closest_nodes(G, r_g, sourceStr)

        k_i = len(graph_neighbors)

        space_neigobors = find_space_closest_nodes(G, k_i, sourceStr)


        vertices_intersection = set(graph_neighbors).intersection(set(space_neigobors))


        vertices_union = set(graph_neighbors).union(set(space_neigobors))

        sum  += len(vertices_intersection)/len(vertices_union)

    pres = (1/len(vertices))*sum

    pres = round(pres, 3)

    return pres


def neig_preservation_multilevel_ratio(GD_prev, GD_curr):

    GD_curr_with_old_positions = GD_curr.copy()

    vertices_old_pos = nx.get_node_attributes(GD_prev, 'pos')

    nx.set_node_attributes(GD_curr_with_old_positions, vertices_old_pos, 'pos')

    neig_pres_curr = compute_neig_preservation(GD_curr)
    neig_pres_curr_old_pos = compute_neig_preservation(GD_curr_with_old_positions)

    return neig_pres_curr/neig_pres_curr_old_pos
