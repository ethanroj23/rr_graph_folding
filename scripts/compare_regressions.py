import sys
import os
from parse_regression import parse_results

# this will be filled in later
valid_runs = []
    


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





if __name__ == '__main__':
    # valid_runs = [
    #           'EArch_tseng',  'k6_arm_core'
    #           ]
    if len(sys.argv) < 3:
        print('Please give the two directories you wish to compare as arguments...')
        exit()
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


