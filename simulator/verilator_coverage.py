import os

def read_line_coverage(cov_file):
    with open(cov_file,'r') as f:
        lines=f.readlines()

    coverage = []
    for line in lines:
        if line.startswith('C '):
            parts = line.split("'")
            sub_parts = parts[1].split('\x01')
            testbench_flag = False
            for sub_part in sub_parts:
                field = sub_part.split('\x02')
                if len(field)==2:
                    if field[0]=='h' and field[1].strip()=='TOP.testbench':
                        testbench_flag = True    
            if testbench_flag:
                continue    # eliminate the code lines in testbench

            cov_info_str = parts[1].strip().replace('\x01', ' |').replace('\x02', ': ')
            cov_hit_num = parts[2].strip()
            coverage.append((cov_info_str, int(cov_hit_num)))
    
    return coverage