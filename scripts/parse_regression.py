import os
import re
import sys

VTR1_DIR='/home/ethan/vtr_work/quickstart/vpr_tseng'
VTR3_DIR='/home/ethan/workspaces/ethanroj23/vtr/vtr_flow/tasks/regression_tests/vtr_reg_nightly_test3/vtr_reg_qor_chain/run001/k6_frac_N10_frac_chain_mem32K_40nm.xml/arm_core.v/common'
VTR4_DIR='/home/ethan/workspaces/ethanroj23/vtr/vtr_flow/tasks/regression_tests/vtr_reg_nightly/vtr_reg_qor_chain/run001/k6_frac_N10_frac_chain_mem32K_40nm.xml/LU32PEEng.v/common'
VTR6_DIR='/home/ethan/workspaces/ethanroj23/vtr/vtr_flow/tasks/regression_tests/vtr_reg_weekly/vtr_reg_titan/run001/stratixiv_arch.timing.xml/cholesky_mc_stratixiv_arch_timing.blif/common'
VTR5_DIR='/home/ethan/workspaces/ethanroj23/vtr/vtr_flow/tasks/regression_tests/vtr_reg_weekly/vtr_reg_titan/run001/stratixiv_arch.timing.xml/des90_stratixiv_arch_timing.blif/common'




vtr_runs = {'vtr1': VTR1_DIR,
            'vtr3': VTR3_DIR,
            'vtr4': VTR4_DIR,
            'vtr6': VTR6_DIR,
            'vtr5': VTR5_DIR
            }


'''
For a given directory, obtain results for all runs inside it
'''
def parse_results(cwd, write_file=False, printing=False):
    valid_runs = []
    stats = {}
    vtr_runs = []
    for file in os.listdir(cwd):
        if '.log' in file:
            vtr_runs.append(file.replace('.log', ''))
            if printing:
                print(file)


    for run in vtr_runs:
        if printing:
            print(run)
        stats[run] = {}
        fname = cwd+'/'+ run +'.log'
        if os.path.isfile(fname) :
            isfolded = False
            total_bytes = 0
            edges = 0
            with open(fname, 'r') as file:
                for line in file:
                    if 'Build FoldedPerTileRRGraph took ' in line:
                        isfolded = True
                    if 'took' in line:
                        # print(line, end='')
                        if 'entire flow' in line:
                            value = float(re.findall('took ([0-9]+\.[0-9]+)', line)[0])
                            memory = float(re.findall('max_rss ([0-9]+\.[0-9]+)', line)[0])
                            stats[run]['entire flow'] = value
                            stats[run]['max_rss'] = memory
                        elif 'Routing' in line:
                            value = float(re.findall('took ([0-9]+\.[0-9]+)', line)[0])
                            stats[run]['routing'] = value
                        elif 'Computing router lookahead map' in line:
                            value = float(re.findall('took ([0-9]+\.[0-9]+)', line)[0])
                            stats[run]['lookahead'] = value
                        elif 'Packing' in line:
                            value = float(re.findall('took ([0-9]+\.[0-9]+)', line)[0])
                            stats[run]['packing'] = value
                        elif 'Placement' in line:
                            value = float(re.findall('took ([0-9]+\.[0-9]+)', line)[0])
                            stats[run]['placement'] = value
                        elif 'Loading routing resource graph' in line:
                            value = float(re.findall('delta_rss \+([0-9]+\.[0-9]+)', line)[0])
                            stats[run]['rr_graph delta_rss'] = value

                        ## Loading routing resource graph took 0.07 seconds (max_rss 48.1 MiB, delta_rss +12.7 MiB)

                    elif 'edges represented out of' in line:
                        edge_patterns = int(re.findall('([0-9]+) edges', line)[0])
                        total_bytes += edge_patterns*8
                    elif 'Time to iterate over' in line and edges==0:
                        edges = int(re.findall('over ([0-9]+)', line)[0])
                    elif 'RR Graph Nodes, Edges, Chan Width' in line:
                        nodes = int(re.findall('([0-9]+), ([0-9]+)', line)[0][0])
                        # edges = int(re.findall('([0-9]+), ([0-9]+)', line)[0][1])
                        if printing:
                            print('nodes: ', nodes)
                        stats[run]['nodes'] = nodes
                        if isfolded:
                            stats[run]['edges'] = edge_patterns
                        else:
                            stats[run]['edges'] = edges
                        if isfolded:
                            total_bytes += nodes*24
                        else:
                            total_bytes += (nodes*16+edges*10)
                stats[run]['size'] = total_bytes/1024/1024

                        # ### Build FoldedPerTileRRGraph
                        # Total patterns: 3948085 of 7260478 nodes 0.54
                        # ### Build FoldedPerTileRRGraph took 13.01 seconds (max_rss 4479.3 MiB, delta_rss +202.1 MiB)
                        # ### clear_node_storage()
                        # ### clear_node_storage() took 0.00 seconds (max_rss 4479.3 MiB, delta_rss +0.0 MiB)
                        # ## Build routing resource graph took 114.05 seconds (max_rss 4479.3 MiB, delta_rss +2338.2 MiB)
                        # Time to iterate over 91152197 edges: 1.900342 seconds (0.000000s per edge) [FoldedPerTileRRGraph]
                        # There are 65750765 edges represented out of 0 total edges
                        # RRGraph[FoldedPerTileRRGraph] is using 480.090820 MiB of memory'
                        # RRGraph[rr_graph_storage] would use 980.081055 MiB of memory'
                        # RR Graph Nodes, Edges, Chan Width: 7260478, 91152197, 400

                        

    # iterate over cache misses and obtain useful information

    using_perf = False
    select_runs = False

    for run in vtr_runs:
        if select_runs and run not in ['EArch_tseng', 'k6_arm_core', 'stratixiv_cholesky', 'linux_arty']:
            continue
        if using_perf:
            with open(cwd+'/'+ run +'_perf.out', 'r') as file:
                line_count = 0
                for line in file:
                    line_count +=1
                    if 'of all' in line:
                        miss_rate = re.findall('([0-9]+\.[0-9]+[ ]*%) of all', line)[0]
                        miss_rate = float(miss_rate.replace(' ', '').replace('%', ''))
                        miss_type = re.findall('of all ([\w-]+ \w+)', line)[0]
                        stats[run][miss_type] = miss_rate
                        # print(line, end='')
                if line_count!=0:
                    valid_runs.append(run)     
        else:
            valid_runs.append(run)       
            


    out = f'# Results for {cwd.split("/")[-1]}\n'
    miss_types = ['vtr', 'cache refs', 'L1-dcache accesses', 'LL-cache accesses', 'routing', 'lookahead',
     'packing', 'placement', 'max_rss','entire flow', 'nodes', 'edges', 'rr_graph delta_rss']
    out += '| category '.ljust(21)+'|  '
    for miss_type in miss_types:
        if miss_type=='vtr':
                out += '  |  '.join(valid_runs)
                out += '  |\n'
                out += '|'+'-'*20+('|'+'-'*8)*len(valid_runs)+'|\n'
        else:
            out += f'| {miss_type}'.ljust(21)+'|'
            for run in valid_runs:
                if miss_type in stats[run]:
                    if miss_type=='size':
                        out += f'{stats[run][miss_type]:.2f}'.ljust(8)+'|'
                    else:
                        out += f'{stats[run][miss_type]}'.ljust(8)+'|'
                else:
                    out += ''.ljust(8)+'|'

            out += '\n'


    if printing:
        print()
        print(out)
    if write_file:
        with open(cwd+'/reg_results.md', 'w') as file:
            file.write(out)
    return stats



if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('Please include the directory you would like to parse...')
        exit()

    cur_dir = sys.argv[1]

    if len(sys.argv) > 2: # parse each subdirectory
        print("trying")
        for subdirectory in os.listdir(cur_dir):
            print(subdirectory)
            cur = f'{cur_dir}/{subdirectory}'
            if os.path.isdir(cur):
                print(f"Working on {cur}")
                parse_results(cur, True, True)
    else:
        cur_stats = parse_results(cur_dir, True, True)








