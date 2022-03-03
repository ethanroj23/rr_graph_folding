import sys
import os
from parse_regression import parse_results

# this will be filled in later
valid_runs = []
    

    # miss_types = ['cache refs', 'L1-dcache accesses', 'LL-cache accesses', 'routing', 'lookahead', 'packing', 'placement', 'max_rss','entire flow', 'nodes', 'edges', 'size']

miss_types = ['cache refs', 'L1-dcache accesses', 'LL-cache accesses', 'routing', 'lookahead', 'packing', 'placement', 'max_rss','entire flow']

def perc_diff(original_num, new_num):
    diff = new_num - original_num
    div = diff / original_num
    return div * 100

def commas(num):
    n = 3
    line = str(num)[::-1]
    list_num = [line[i:i+n] for i in range(0, len(line), n)]
    list_num = ','.join(list_num)
    return list_num[::-1]

def pmil(num):
    return num/1000000


def compare(stats1, stats2, dir1, dir2):
    print('\n---compare\n')
    out = f'# Results for {dir1} vs {dir2}\n'
    # miss_types = ['cache refs', 'L1-dcache accesses', 'LL-cache accesses', 'routing', 'lookahead', 'packing', 'placement', 'max_rss','entire flow', 'nodes', 'edges', 'size']
    # print()
    # print('| category '.ljust(21)+'|  ', end='')
    out += '| category '.ljust(21)+'|  '
    for miss_type in miss_types:
        if miss_type=='vtr':
                out += '  |  '.join(valid_runs)
                out += '  |\n'
                out += '|'+'-'*20+('|'+'-'*8)*len(valid_runs)+'|\n'
        else:
            out += f'| {miss_type}'.ljust(21)+'|'
            for run in valid_runs:
                if miss_type in stats1[run]:
                    cur_ratio = stats1[run][miss_type]/stats2[run][miss_type]
                    marker = ''
                    if cur_ratio < 1:
                        marker = '+'
                    out += f' {abs(perc_diff(stats1[run][miss_type], stats2[run][miss_type])):.2f}{marker}'.ljust(8)+'|'
                else:
                    out += ''.ljust(8)+'|'

            out += '\n'

    out += f'\t+ {dir1} was better\n'
    out += f'\t  {dir2} was better\n'

    print()
    print(out)
    # if write_file:
    #     with open(cwd+'/reg_results.md', 'w') as file:
    #         file.write(out)
    # return stats

def latex_table(stats1, stats2, dir1, dir2):
    print('\n---latex_table\n')
    out = '\\begin{table}[H]\n' + \
          '\\centering\n' + \
          '\\begin{tabular}{|'+'|'.join(['l']*(len(valid_runs)+1))+'|}\n' + r'\hline'+'\n' + \
          'Category & ' + ' & '.join(valid_runs) + r' \\\hline' + '\n'
    # miss_types = ['cache refs', 'L1-dcache accesses', 'LL-cache accesses', 'routing', 'lookahead', 'packing', 'placement', 'max_rss','entire flow', 'nodes', 'edges', 'size']
    # miss_types = ['routing', 'lookahead', 'packing', 'placement', 'max_rss','entire flow']
    for miss_type in miss_types:
        if miss_type == 'entire flow':
            out += 'entire vtr flow & '
        else:
            out += miss_type.replace('_', ' ') + ' & '
        for run in valid_runs:
            if miss_type in stats1[run]:
                # print(f'{stats[run][miss_type]}'.ljust(8)+'|', end='')
                cur_ratio = stats1[run][miss_type]/stats2[run][miss_type]
                marker = ''
                if cur_ratio < 1:
                    marker = ''
                # out += f' {abs((1-cur_ratio)*100):.2f}{marker}'.ljust(8)+'|'
                out += f' {perc_diff(stats1[run][miss_type], stats2[run][miss_type]):.2f}{marker}'+' &'
            else:
                # print(''.ljust(8)+'|', end='')
                out += ''.ljust(8)+'&'
        out = out[:-1]
        out += ' \\\\ \n'
    out += '\hline\n\end{tabular}\n'
    out += '\caption{\label{tab:with_without_api} Percent increase in runtime with addition of API.}\n'
    out += '\end{table}'
    print(out)

def latex_table_simple(stats, dir):
    print(f'\n---Table for {dir}\n')
    out = '\\begin{table}[H]\n' + \
          '\\centering\n' + \
          '\\begin{tabular}{|'+'|'.join(['l']*(len(valid_runs)+1))+'|}\n' + r'\hline'+'\n' + \
          'Category & ' + ' & '.join(valid_runs) + r' \\\hline' + '\n'
    # miss_types = ['cache refs', 'L1-dcache accesses', 'LL-cache accesses', 'routing', 'lookahead', 'packing', 'placement', 'max_rss','entire flow', 'nodes', 'edges', 'size']
    for miss_type in miss_types:
        if miss_type == 'entire flow':
            out += 'entire vtr flow & '
        else:
            out += miss_type.replace('_', ' ') + ' & '
        for run in valid_runs:
            if miss_type in stats[run]:
                cur_ratio = stats[run][miss_type]
                marker = ''
                if miss_type in ['nodes', 'edges']:
                    out += f' {commas(cur_ratio)}{marker}'+' &'
                else:
                    out += f' {cur_ratio:.2f}{marker}'+' &'
            else:
                out += ''.ljust(8)+'&'
        out = out[:-1]
        out += ' \\\\ \n'
    out += '\hline\n\end{tabular}\n'
    out += '\caption{\label{tab:'+f'{dir.replace("/", "")}'+'} Percent increase in runtime with addition of API.}\n'
    out += '\end{table}'
    print(out)

def latex_table_combined(stats1, stats2, dir1, dir2):
    print('\n---latex_table_combined\n')
    out = '\\begin{table}[H]\n' + \
          '\\centering\n' + \
          '\\begin{tabular}{|'+'|'.join(['l']*(len(valid_runs)+1))+'|}\n' + r'\hline'+'\n' + \
          'Category & ' + ' & '.join(valid_runs) + r' \\\hline' + '\n'
    # miss_types = ['cache refs', 'L1-dcache accesses', 'LL-cache accesses', 'routing', 'lookahead', 'packing', 'placement', 'max_rss','entire flow', 'nodes', 'edges', 'size']
    for miss_type in miss_types:
        if miss_type == 'entire flow':
            out += 'entire vtr flow & '
        else:
            out += miss_type.replace('_', ' ') + ' & '
        for run in valid_runs:
            if miss_type in stats1[run]:
                # print(f'{stats[run][miss_type]}'.ljust(8)+'|', end='')
                cur_ratio = stats1[run][miss_type]/stats2[run][miss_type]
                marker = ''
                if cur_ratio < 1:
                    marker = ''
                if miss_type in ['nodes', 'edges']:
                    if True: # pmil
                        out += f' {pmil(stats1[run][miss_type]):.3f} / {pmil(stats2[run][miss_type]):.3f} &'
                    else:
                        out += f' {commas(stats1[run][miss_type])} / {commas(stats2[run][miss_type])} &'
                else:
                    out += f' {stats1[run][miss_type]:.1f} / {stats2[run][miss_type]:.1f} &'
            else:
                out += ''.ljust(8)+'&'
        out = out[:-1]
        out += ' \\\\ \n'
    out += '\hline\n\end{tabular}\n'
    out += '\caption{\label{tab:with_without_api} Percent increase in runtime with addition of API.}\n'
    out += '\end{table}'
    print(out)

def compare_both(stats1, stats2, dir1, dir2):
    print('\n---compare\n')
    out = f'# Results for {dir1} vs {dir2}\n'
    # miss_types = ['cache refs', 'L1-dcache accesses', 'LL-cache accesses', 'routing', 'lookahead', 'packing', 'placement', 'max_rss','entire flow', 'nodes', 'edges', 'size']
    # print()
    # print('| category '.ljust(21)+'|  ', end='')
    out += '| category '
    for run in valid_runs:
        out += f'|{run}'
    out += '|\n'
    for run in valid_runs:
        out += f'|---'
    out += '|---|\n'
    for miss_type in miss_types:
        if miss_type=='vtr':
                out += '  |  '.join(valid_runs)
                out += '  |\n'
                out += '|'+'-'*20+('|'+'-'*8)*len(valid_runs)+'|\n'
        else:
            out += f'| {miss_type}'.ljust(21)+'|'
            for run in valid_runs:
                if miss_type in stats1[run]:
                    cur_ratio = stats1[run][miss_type]/stats2[run][miss_type]
                    marker = ''
                    if cur_ratio < 1:
                        marker = '+'
                    # out += f' {abs(perc_diff(stats1[run][miss_type], stats2[run][miss_type])):.2f}{marker}'.ljust(8)+'|'
                    if miss_type in ['size']:
                        out += f' {stats1[run][miss_type]:.2f} / {stats2[run][miss_type]:.2f}'.ljust(8)+'|'
                    else:
                        out += f' {stats1[run][miss_type]} / {stats2[run][miss_type]}'.ljust(8)+'|'
                else:
                    out += ''.ljust(8)+'|'

            out += '\n'

    out += f'\t+ {dir1} was better\n'
    out += f'\t  {dir2} was better\n'

    print()
    print(out)

def compare_rel(stats1, stats2, dir1, dir2):
    print('\n---compare\n')
    out = f'# Results for {dir1} vs {dir2}\n'
    # miss_types = ['cache refs', 'L1-dcache accesses', 'LL-cache accesses', 'routing', 'lookahead', 'packing', 'placement', 'max_rss','entire flow', 'nodes', 'edges', 'size']
    # print()
    # print('| category '.ljust(21)+'|  ', end='')
    out += '| category '
    for run in valid_runs:
        out += f'|{run}'
    out += '|\n'
    for run in valid_runs:
        out += f'|---'
    out += '|---|\n'
    for miss_type in miss_types:
        if miss_type=='vtr':
                out += '  |  '.join(valid_runs)
                out += '  |\n'
                out += '|'+'-'*20+('|'+'-'*8)*len(valid_runs)+'|\n'
        else:
            out += f'| {miss_type}'.ljust(21)+'|'
            for run in valid_runs:
                if miss_type in stats1[run]:
                    cur_ratio = stats1[run][miss_type]/stats2[run][miss_type]
                    marker = ''
                    if cur_ratio < 1:
                        marker = '+'
                    # out += f' {abs(perc_diff(stats1[run][miss_type], stats2[run][miss_type])):.2f}{marker}'.ljust(8)+'|'
                    one = stats1[run][miss_type]
                    two = stats2[run][miss_type]
                    out += f' {(perc_diff(one, two)):.2f}'.ljust(8)+'|'
                else:
                    out += ''.ljust(8)+'|'

            out += '\n'

    out += f'\t+ {dir1} was better\n'
    out += f'\t  {dir2} was better\n'

    print()
    print(out)




def md_all_absolute(dirs, stats):
    ''' Generates a table like the following.
        Device - EArch_tseng
        | category |nodes_all_attr_binary_search|flat|switches_subsets|nodes_all_attr|edge_switch_subsets|
        |---|---|---|---|---|---|
        | cache refs         | 2.70   | 3.27   | 2.74   | 2.97   | `2.52` |
        | L1-dcache accesses | 5.06   | 5.34   | 5.39   | 5.48   | `4.43` |
        | LL-cache accesses  | 1.47   | `1.41` | 1.53   | 1.57   | 1.50   |
        | routing            | 0.18   | `0.09` | 0.10   | 0.10   | 0.11   |
    '''

    methods = [x.split('/')[-1] for x in dirs]
    methods = ['_'.join(x.split('_')[:-4]) for x in methods]
    print('\n---compare\n')
    out = f'### Comparisons for '
    for cur_dir in dirs:
        out += f'{cur_dir}, '
    out += '\n'
    attribute_order = ['routing', 'lookahead', 'packing', 'placement', 'rr_graph delta_rss', 'max_rss','entire flow', ]


    # print()
    # print('| category '.ljust(21)+'|  ', end='')

    first_dir = dirs[0]
    for device in stats[first_dir]:
        out += f'## Device - {device}\n'

        # Header with Categories line
        out += '| category '
        for method in methods:
            out += f'|{method}'
        out += '|\n'

        # Hyphens line
        for method in methods:
            out += f'|---'
        out += '|---|\n'

        
        for attr in attribute_order: # use stats[first_dir][device]: if you don't want to predefine the attributes
            if attr=='vtr':
                    out += '  |  '.join(dirs)
                    out += '  |\n'
                    out += '|'+'-'*20+('|'+'-'*8)*len(dirs)+'|\n'
            else:
                out += f'| {attr}'.ljust(21)+'|' # category
                minimum = None
                if attr in stats[first_dir][device]:
                    minimum = min([stats[x][device][attr] for x in dirs])
                for cur_dir in dirs:
                    cur_stats = stats[cur_dir][device]
                    if attr in cur_stats:
                        if cur_stats[attr] == minimum:
                            out += f' `{cur_stats[attr]:.2f}`'.ljust(8)+'|' # data
                        else:
                            out += f' {cur_stats[attr]:.2f}'.ljust(8)+'|' # data
                    else:
                        out += ''.ljust(8)+'|'

                out += '\n'


    print()
    print(out)
    return out


def md_all_relative(dirs, stats):
    ''' Generates a table like the following.
        Device - EArch_tseng
        | category |nodes_all_attr_binary_search|flat|switches_subsets|nodes_all_attr|edge_switch_subsets|
        |---|---|---|---|---|---|
        | cache refs         | 2.70   | 3.27   | 2.74   | 2.97   | `2.52` |
        | L1-dcache accesses | 5.06   | 5.34   | 5.39   | 5.48   | `4.43` |
        | LL-cache accesses  | 1.47   | `1.41` | 1.53   | 1.57   | 1.50   |
        | routing            | 0.18   | `0.09` | 0.10   | 0.10   | 0.11   |
    '''

    methods = [x.split('/')[-1] for x in dirs]
    methods = ['_'.join(x.split('_')[:-4]) for x in methods]
    print('\n---compare\n')
    out = f'### Comparisons for '
    for cur_dir in dirs:
        out += f'{cur_dir}, '
    out += '\n'
    # attribute_order = ['cache refs', 'L1-dcache accesses', 'LL-cache accesses', 'routing', 'lookahead', 'packing', 'placement', 'max_rss','entire flow', 'nodes', 'edges', 'size']
    attribute_order = ['routing', 'lookahead', 'packing', 'placement', 'rr_graph delta_rss', 'max_rss','entire flow', ]


    # print()
    # print('| category '.ljust(21)+'|  ', end='')

    first_dir = dirs[0]
    flat_dir = ''
    for cur_dir in dirs:
        if 'flat' in cur_dir:
            flat_dir = cur_dir
    for device in stats[first_dir]:
        out += f'## Device - {device}\n'

        # Header with Categories line
        out += '| category '
        for method in methods:
            out += f'|{method}'
        out += '|\n'

        # Hyphens line
        for method in methods:
            out += f'|---'
        out += '|---|\n'

        
        for attr in attribute_order: # use stats[first_dir][device]: if you don't want to predefine the attributes
            if attr=='vtr':
                    out += '  |  '.join(dirs)
                    out += '  |\n'
                    out += '|'+'-'*20+('|'+'-'*8)*len(dirs)+'|\n'
            else:
                out += f'| {attr}'.ljust(21)+'|' # category
                minimum = None
                if attr in stats[first_dir][device]:
                    minimum = min([stats[x][device][attr] for x in dirs])
                for cur_dir in dirs:
                    cur_stats = stats[cur_dir][device]

                    if attr in cur_stats:
                        cur_val = stats[cur_dir][device][attr]
                        flat_val = stats[flat_dir][device][attr]
                        perc = 0
                        if flat_val != 0:
                            perc = (cur_val - flat_val)/flat_val*100
                        if cur_val == minimum:
                            out += f' `{perc:.2f}%`'.ljust(8)+'|' # data
                        else:
                            out += f' {perc:.2f}%'.ljust(8)+'|' # data
                    else:
                        out += ''.ljust(8)+'|'

                out += '\n'


    print()
    print(out)
    return out
    
    





def compare_all():
    '''
    Executes then compare_regressions.py is run with "python compare_regressions.py all <parent_directory>"
    Compares all regressions within the parent directory and prints LaTex or Markdown output
    '''
    print('Comparing all')

    parent_dir = sys.argv[2]
    dirs = []

    for file in os.listdir(parent_dir):
        subdirectory = f'{parent_dir}/{file}'
        if os.path.isdir(subdirectory):
            dirs.append(subdirectory)
    if not len(dirs):
        print("The parent directory has no subdirectories...")
        exit()

    first_dir = dirs[0]
    # just add all files of the first subdirectory as each subdirectory should have used the same folding_methods
    for file in os.listdir(first_dir):
        if '.log' in file:
            valid_runs.append(file.replace('.log', ''))

    stats = {}
    for cur_dir in dirs:
        stats[cur_dir] = parse_results(cur_dir)


    for cur_dir in dirs:
        print(cur_dir)
        print(stats[cur_dir])

    for device in stats[first_dir]:
        print(device)
        for attr in stats[first_dir][device]:
            print(f'{attr}')
            for cur_dir in dirs:
                print(f' {stats[cur_dir][device][attr]}')


    absolute = md_all_absolute(dirs, stats)
    relative = md_all_relative(dirs, stats)


    with open('temp_comparison.md', 'w') as file:
        file.write(absolute)
        file.write(relative)

    # compare(stats1, stats2, dir1, dir2)
    # latex_table(stats1, stats2, dir1, dir2)
    # latex_table_simple(stats1, dir1)
    # latex_table_simple(stats2, dir2)
    # latex_table_combined(stats1, stats2, dir1, dir2)
    # compare_both(stats1, stats2, dir1, dir2)
    # compare_rel(stats1, stats2, dir1, dir2)

    '''
    EArch_tseng
                flat | method1 | method2 | method3
    routing     0       0           0           0
    lookahead
    entire_flow


    k6_arm_core
                flat | method1 | method2 | method3
    routing     0       0           0           0
    lookahead
    entire_flow

    '''






if __name__ == '__main__':
    # valid_runs = [
    #           'EArch_tseng',  'k6_arm_core'
    #           ]
    if len(sys.argv) < 3:
        print('Please give the two directories you wish to compare as arguments...\n')
        print('To compare all the subdirectories of a parent folder,')
        print('give "all" as the first argument and the parent folder as the second argument')
        exit()
    else:

        if sys.argv[1] == 'all': # run all
            compare_all()
        else:
            dir1 = sys.argv[1]
            dir2 = sys.argv[2]
            for file in os.listdir(dir1):
                if '.log' in file:
                    valid_runs.append(file.replace('.log', ''))
            
            stats1 = parse_results(dir1)
            stats2 = parse_results(dir2)
            compare(stats1, stats2, dir1, dir2)
            latex_table(stats1, stats2, dir1, dir2)
            latex_table_simple(stats1, dir1)
            latex_table_simple(stats2, dir2)
            latex_table_combined(stats1, stats2, dir1, dir2)
            compare_both(stats1, stats2, dir1, dir2)
            compare_rel(stats1, stats2, dir1, dir2)


