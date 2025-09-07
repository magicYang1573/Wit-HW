import os
from vcdvcd import VCDVCD


def read_vcd_trace(vcd_file, reg_list):
    vcd = VCDVCD(vcd_file)
    signal_list = vcd.references_to_ids.keys()
    vcd_reg_dict = {}
    
    for s in signal_list:
        s_name = s.split('[')[0].split('.')[-1]
        if ('testbench.'+s_name) in s:
            continue
        if s_name in reg_list:
            vcd_reg_dict[s_name] = s
    
    # print(reg_list)
    # print(signal_list)
    # print(vcd_reg_dict)
    
    # Ensure all registers in reg_list are found in the VCD
    # assert(len(vcd_reg_dict) == len(reg_list))
    state_trace = []
    for reg in reg_list:
        s = vcd_reg_dict.get(reg)
        if s is not None:
            state_trace.append([(time, int(value, 2)) for time, value in vcd[s].tv])
    
    return state_trace
