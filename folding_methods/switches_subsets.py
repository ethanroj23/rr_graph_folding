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
F_NODE = 0
F_EDGES = 1
F_NODE_S_IDX = 2
F_MASTER_LIST = 3

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
    metrics(flat_graph, folded_graph, graph_name)
    verify(flat_graph, folded_graph)

def fold(graph):
    edge_node_patterns = {}
    node_to_edges_idx = []
    shared_switches = []
    edge_pattern_idx = 0
    for i, node in enumerate(graph[NODE]):

        edges = []
        edges_string = []
        if len(graph[EDGE][i]):
            for edge in graph[EDGE][i]:
                switch = edge[1]
                edges_string.append(f'{switch}')
                edges.append(switch)
        edge_pattern_string = ','.join(edges_string) # using just edges as pattern
        edge_pattern = edges

        # SWITCH
        if edge_pattern_string not in edge_node_patterns:
            edge_node_patterns[edge_pattern_string] = edge_pattern_idx
            shared_switches += [0] # prepare for next item
            shared_switches[edge_pattern_idx] = edge_pattern # actual data
            edge_pattern_idx += 1

        node_to_edges_idx.append(edge_node_patterns[edge_pattern_string])

    # create master list of which all shared_switches will be a subset of
    # also store the index into the master list for each 
    master_list = []
    shared_to_master_idx = []
    print(f"{len(shared_switches)} patterns to parse")
    for i, switches in enumerate(sorted(shared_switches, key=len, reverse=True)):
        if i % 1000 == 0:
            print(i)
        if not is_subsequence(switches, master_list):
            master_list += switches

    for i, switches in enumerate(shared_switches):
        if i % 1000 == 0:
            print(i)
        cur_idx = subsequence_idx(switches, master_list)
        if len(switches) == 0: # for empty subset instance
            cur_idx = 0
        shared_to_master_idx.append(cur_idx)
    # print(master_list)

    for i in range(len(node_to_edges_idx)):
        node_to_edges_idx[i] = shared_to_master_idx[node_to_edges_idx[i]]

    folded_graph = [graph[NODE], graph[EDGE], node_to_edges_idx, master_list]
    return folded_graph



# </node>
# <node capacity="1" direction="DEC_DIR" id="15051" type="CHANY" s_idx="1"><loc ptc="99" xhigh="9" xlow="9" yhigh="9" ylow="9"/>
# <timing C="3.02100027e-14" R="101"/>
# <segment segment_id="0"/>
# </node>

# <rr_switches>
# <rr_switch id="0"/>
# <rr_switch id="0"/>
# <rr_switch id="3"/>
# <rr_switch id="0"/>
# <rr_switch id="2"/>
# <rr_switch id="0"/>
# </rr_switches>


def save(graph, graph_name):
    '''
    Saves the folded graph into an xml file with switch indices and switch master list
    '''
    save_file = f'{os.getcwd()}/folded_graphs/{name()}_{graph_name}.xml'
    flat_file = f'{os.getcwd()}/flat_graphs/{graph_name}.xml'
    print(f'Saving graph to {save_file}')
    with open(save_file, 'w') as folded_file:
        with open(flat_file, 'r') as file:
            for line in file:
                write_line = line
                if '<node' in line:
                    node = int(re.findall('id="([0-9]+)"', line)[0])
                    s_idx = graph[F_NODE_S_IDX][node]
                    write_line = write_line.replace('><loc', f' s_idx="{s_idx}"><loc')
                if '<rr_nodes>' in line:
                    folded_file.write('<rr_switches>\n')
                    for switch in graph[F_MASTER_LIST]:
                        folded_file.write(f'<rr_switch id="{switch}"/>\n')
                    folded_file.write('</rr_switches>\n')
                if '<edge ' in line:
                    write_line = re.sub(' switch_id="[0-9]+"', '', write_line)
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
        i = 0
        for edge in flat_graph[EDGE][node]:
            switch = edge[1]
            f_switch = folded_graph[F_MASTER_LIST][folded_graph[F_NODE_S_IDX][node]+i]
            if (switch != f_switch):
                print(f'didnt match {i}th edge of node {node} is {f_switch} but should be {switch}')
            i += 1


def name():
    return 'switches_subsets'

if __name__ == '__main__':
    print(f"This folding method is '{name()}'")
    print(f"To fold an rr_graph with this method, run the following command from the directory one level up")
    print(f"\tpython fold_rr_graph.py {name()} <flat_graph_name>")




