import os
import re

'''
------------------------------- SWITCHES_SUBSETS folding method --------------------------------------

A list of switch ids is stored such that
The switches of every node are a subset of the larger list

Example:
Switch List = 00111112222222
Subset #1 = 01111 (starts at Switch List index 1)
Subset #2 = 11222 (starts at Switch List index 5)
Subset #3 = 122   (starts at Switch List index 6)

Additional data stored for each NODE:
s_idx // switch index into Switch List


</node>
<node capacity="1" direction="DEC_DIR" id="15051" type="CHANY" s_idx="1"><loc ptc="99" xhigh="9" xlow="9" yhigh="9" ylow="9"/>
<timing C="3.02100027e-14" R="101"/>
<segment segment_id="0"/>
</node>

<rr_switches>
<rr_switch id="0"/>
<rr_switch id="0"/>
<rr_switch id="3"/>
<rr_switch id="0"/>
<rr_switch id="2"/>
<rr_switch id="0"/>
</rr_switches>



------------------------------- NODES_ALL_ATTR folding method --------------------------------------

'''



# Indices into flat_graph object
NODE = 0
EDGE = 1
EDGE_COUNT = 2

XLOW = 0
YLOW = 1
XHIGH = 2
YHIGH = 3
TYPE = 4
R = 5
C = 6
CAPACITY = 7
SIDE = 8
PTC = 9
DIRECTION = 10
SEGMENT = 11

# Indices into folded_graph object
F_NODE_TO_PTN = 0
F_EDGE_PTN = 1
F_FIRST_DEST = 2

# Size constants
FLAT_NODE_BYTES = 16 # bytes per node
FLAT_EDGE_BYTES = 10 # bytes per edge
FOLDED_DEST_BYTES = 4
FOLDED_SWITCH_BYTES = 2
FOLDED_NODE_BYTES = 20 # also storing switch idx

def subsequence_idx(a, b):
    if not len(a):
        return True
    first = a[0]
    length = len(a)
    idx = 0
    for i, val in enumerate(b):
        if val == first and a == b[idx:idx+length]:
            return idx
        idx += 1
    return -1

def is_subsequence(a, b):
    if not len(a):
        return True
    first = a[0]
    length = len(a)
    idx = 0
    for i, val in enumerate(b):
        if val == first and a == b[idx:idx+length]:
            return True
        idx += 1
    return False

def fold_save_metrics(flat_graph, graph_name):
    folded_graph = fold(flat_graph)
    save(folded_graph, graph_name)
    # metrics(flat_graph, folded_graph, graph_name)
    verify(flat_graph, folded_graph)



def fold(graph):
    edge_node_patterns = {}
    node_to_edges_idx = []
    shared_switches = []
    edge_pattern_idx = 0
    edge_switch_count = 0
    node_to_edge_patterns = []
    node_first_dest = []
    all_edge_patterns = {} # all edges of a given pattern share the same switch
    for i, node in enumerate(graph[NODE]): # for every node
        node_to_edge_patterns.append([])
        node_first_dest.append(0)
        edges = []
        edges_string = []
        cur_patterns = []
        if len(graph[EDGE][i]):
            first_dest = graph[EDGE][i][0][0]
            node_first_dest[i] = first_dest
            prev_switch = -1
            for edge in graph[EDGE][i]:
                dest_diff = edge[0] - first_dest
                switch = edge[1]
                if prev_switch != switch:
                    if len(cur_patterns):
                        ptn = tuple(cur_patterns)
                        if ptn not in all_edge_patterns:
                            all_edge_patterns[ptn] = edge_pattern_idx
                            edge_switch_count += len(ptn)
                            edge_pattern_idx += 1
                        node_to_edge_patterns[i].append(all_edge_patterns[ptn])


                    prev_switch = switch
                    cur_patterns = [switch] # first value is the switch
                cur_patterns.append(dest_diff)

                edges_string.append(f'{switch}')
                edges.append(switch)
            if len(cur_patterns): # last set of edges
                ptn = tuple(cur_patterns)
                if ptn not in all_edge_patterns:
                    all_edge_patterns[ptn] = edge_pattern_idx
                    edge_switch_count += len(ptn)
                    edge_pattern_idx += 1
                node_to_edge_patterns[i].append(all_edge_patterns[ptn])

    node_to_ptn_count = 0
    for node in node_to_edge_patterns:
        node_to_ptn_count += len(node)

    all_edge_patterns = {v: k for k, v in all_edge_patterns.items()}
    node_count = len(graph[NODE])
    flat_size = graph[EDGE_COUNT]*6/1024/1024
    flat_size_on_disk = graph[EDGE_COUNT]*10/1024/1024
    folded_size = (node_count * 4 +
                  node_to_ptn_count * 4 +
                  len(all_edge_patterns) * 8 + 
                  (edge_switch_count - len(all_edge_patterns)) * 4) / 1024 / 1024
    print(f'\n{node_to_ptn_count} node to patterns\n{len(all_edge_patterns)} patterns\n{edge_switch_count} edge and switches [{edge_switch_count / graph[EDGE_COUNT]:.2f}]')
    print(f'Original Size: {graph[EDGE_COUNT]} edges {flat_size:.2f} MiB')
    print(f'Folded Size: {folded_size:.2f} MiB [{folded_size / flat_size:.2f}] or [{folded_size / flat_size_on_disk:.2f}] on disk')

    folded_graph = [node_to_edge_patterns, all_edge_patterns, node_first_dest]
    return folded_graph


# <rr_node_to_ptns>
# <node_to_ptn id="1" dest="25">
# <ptn id="0"/>
# </node_to_ptn>
# <node_to_ptn id="4" dest="28">
# <ptn id="0"/>
# </node_to_ptn>
# <rr_edge_ptns>
# </edge_ptn>
# <edge_ptn id="7938" switch_id="1">
# <ddiff id="0">
# <ddiff id="498">
# </edge_ptn>
# <edge_ptn id="7939" switch_id="2">
# <ddiff id="3155">
# <ddiff id="6409">
# </edge_ptn>
# </rr_edge_ptns>


def save(graph, graph_name):
    '''
    Saves the folded graph into an xml file with switch indices and switch master list
    '''
    # folded_graph = [node_to_edge_patterns, all_edge_patterns, node_first_dest]
# F_NODE_TO_PTN = 0
# F_EDGE_PTN = 1
# F_FIRST_DEST = 2
    save_file = f'{os.getcwd()}/folded_graphs/{name()}_{graph_name}.xml'
    flat_file = f'{os.getcwd()}/flat_graphs/{graph_name}.xml'
    print(f'Saving graph to {save_file}')
    with open(save_file, 'w') as folded_file:
        with open(flat_file, 'r') as file:
            for line in file:
                write_line = line
                # everything until rr_edges remains the same as before
                if '<rr_edges' in line:

                    folded_file.write(f'<rr_edge_ptns>\n')
                    ptn_idx = 0
                    for key in graph[F_EDGE_PTN]:
                        ptn = graph[F_EDGE_PTN][key]
                        folded_file.write(f'<edge_ptn id="{ptn_idx}" switch_id="{ptn[0]}">\n')
                        for dest_diff in ptn[1:]:
                            folded_file.write(f'<ddiff id="{dest_diff}"/>\n')
                        folded_file.write(f'</edge_ptn>\n')
                        ptn_idx += 1
                    folded_file.write(f'</rr_edge_ptns>\n')


                    folded_file.write(f'<rr_node_e_ptns>\n')
                    for i, node in enumerate(graph[F_NODE_TO_PTN]):
                        if len(node):
                            folded_file.write(f'<node_e_ptn id="{i}" dest="{graph[F_FIRST_DEST][i]}">\n')
                            for ptn in node:
                                folded_file.write(f'<e_ptn id="{ptn}"/>\n')
                            folded_file.write(f'</node_e_ptn>\n')
                    folded_file.write(f'</rr_node_e_ptns>\n')

                    folded_file.write(f'</rr_graph>\n')
                    return
                folded_file.write(write_line)



def metrics(flat_graph, folded_graph, graph_name):
    print('metrics')
    MiB = 1024*1024
    flat_nodes_size = len(flat_graph[NODE])*FLAT_NODE_BYTES/MiB
    edge_count = flat_graph[EDGE_COUNT]
    flat_size = (len(flat_graph[NODE])*FLAT_NODE_BYTES + edge_count*FLAT_EDGE_BYTES)/MiB
    flat_switches = edge_count * FOLDED_SWITCH_BYTES/MiB
    
    switch_count = len(folded_graph[F_MASTER_LIST])
    folded_size = (len(flat_graph[NODE])*FOLDED_NODE_BYTES + edge_count*FOLDED_DEST_BYTES + switch_count*FOLDED_SWITCH_BYTES)/MiB
    folded_switches = (switch_count*FOLDED_SWITCH_BYTES+len(flat_graph[NODE])*4)/MiB

    print(f'\n{graph_name} metrics [{name()}]:\n\t' \
          f'Switches Stored: {switch_count} ({flat_switches:.2f} -> {folded_switches:.2f} MiB) [{100*folded_switches/flat_switches:.1f}%]\n\t' \
          f'Total Size: {flat_size:.2f} -> {folded_size:.2f} MiB [{100*folded_size/flat_size:.1f}%]')

def verify(flat_graph, folded_graph):
    for node, _ in enumerate(flat_graph[EDGE]):
        ptns = folded_graph[F_NODE_TO_PTN][node]
        if len(ptns):
            first_dest = folded_graph[F_FIRST_DEST][node]
            all_dests = [] 
            all_switches = []
            for ptn in ptns:
                cur_switch = folded_graph[F_EDGE_PTN][ptn][0]
                for dest in folded_graph[F_EDGE_PTN][ptn][1:]:
                    all_switches.append(cur_switch)
                    all_dests.append(first_dest + dest)
        for i, edge in enumerate(flat_graph[EDGE][node]):
            assert(edge[1] == all_switches[i])
            assert(edge[0] == all_dests[i])
            


def name():
    return 'edge_switch_subsets'

if __name__ == '__main__':
    print(f"This folding method is '{name()}'")
    print(f"To fold an rr_graph with this method, run the following command from the directory one level up")
    print(f"\tpython fold_rr_graph.py {name()} <flat_graph_name>")




