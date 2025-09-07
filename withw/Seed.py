import numpy as np
import random
import os
import math
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

# from rtlil_coverage import read_branch_coverage, read_state_trace
from verilator_coverage import read_line_coverage
from verilator_vcd import read_vcd_trace


def dtw_distance(state_trace_1, state_trace_2):
    distance_sum = 0
    for i in range(0, len(state_trace_1)):
        sequence1 = state_trace_1[i]
        sequence2 = state_trace_2[i]
        states1 = np.array([state for _, state in sequence1])
        states2 = np.array([state for _, state in sequence2])
        
        # Calculate DTW distance
        # distance, _ = fastdtw(states1, states2, dist=lambda x, y: euclidean([x], [y])) / max(len(states1), len(states2))
        # distance, _ = fastdtw(states1, states2, dist=lambda x, y: euclidean([x], [y])) 
        distance, _ = fastdtw(states1, states2, dist=lambda x, y: 0 if x == y else 1)
        distance_sum += distance**2

    if len(state_trace_1)==0:
        return 0.0
        
    distance = math.sqrt(distance_sum) / len(state_trace_1)
    return distance

def coverage_distance(branch_hit_1, branch_hit_2):
    branch_hit_1 = np.array(branch_hit_1)
    branch_hit_2 = np.array(branch_hit_2)
    return np.sqrt(np.sum((branch_hit_1 - branch_hit_2)**2)) / sum(1 for x in (branch_hit_1+branch_hit_2) if x != 0)
    # return np.sum(((branch_hit_1>0) ^ (branch_hit_2>0)))


class Seed():
    def __init__(self, input_file='', correct_output_file = '', buggy_output_file='', cov_file='', vcd_file='', input_signals=[], pass_flag=False, sequential_flag=True):
        self.input_file = input_file
        self.cov_file = cov_file
        self.vcd_file = vcd_file
        self.buggy_output_file = buggy_output_file
        self.correct_output_file = correct_output_file
        self.input_signals = input_signals
        self.pass_flag = pass_flag
        self.sequential_flag = sequential_flag

        self.value = []  # each position corresponds to the value of a signal in one clock cycle

        self.branch_hit_total = []  # each position corresponds to the hit number of a branch under the test input
        self.state_trace = []
        self.out_trace = []

        self.fitness = 0

    def delete(self):
        if self.input_file and os.path.isfile(self.input_file):
            os.remove(self.input_file)

        if self.cov_file and os.path.isfile(self.cov_file):
            os.remove(self.cov_file)
        
        if self.vcd_file and os.path.isfile(self.vcd_file):
            os.remove(self.vcd_file)

        if self.buggy_output_file and os.path.isfile(self.buggy_output_file):
            os.remove(self.buggy_output_file)     

        if self.correct_output_file and os.path.isfile(self.correct_output_file):
            os.remove(self.correct_output_file)     
        
        

    def __str__(self):
        s = ''
        s += '--------------\n'
        s += 'Seed: \n'
        s += 'input file: ' + self.input_file + '\n'
        s += 'value: ' + str(self.value) + '\n'
        s += 'pass: ' + str(self.pass_flag) + '\n'
        s += 'cov file: ' + self.cov_file + '\n'
        s += 'branch hit: ' + str(self.branch_hit_total) + '\n'
        s += 'state trace: ' + str(self.state_trace) + '\n'
        return s

    # mutate according to Rfuzz harness
    def mutate(self, mutate_rate):
        num_to_mutate = int(len(self.value) * mutate_rate)
        indices_to_mutate = random.sample(range(len(self.value)), num_to_mutate)
        for index in indices_to_mutate:
            self.value[index] = random.randint(0, 1024)

        self.input_file = ''
        self.buggy_output_file = ''
        self.correct_output_file = ''
        self.cov_file = ''
        self.branch_hit_total = []
        self.state_trace = []
        self.out_trace = []
    
    # mutate according to cycle and with pos priority
    def mutate_with_pri(self, mutate_rate, mut_pos_pri):
        num_to_mutate = max(1, int(len(mut_pos_pri) * mutate_rate))
        signals_num = int(len(self.value) / len(mut_pos_pri))

        # choose which cycle position to mutate
        mut_pos_pri = np.array(mut_pos_pri).astype(float)
        mut_pos_pri /= mut_pos_pri.sum()
        selected_indices = np.random.choice(
            range(len(mut_pos_pri)), 
            size=num_to_mutate, 
            p=mut_pos_pri,
            replace=False  # Ensure we don't pick the same index more than once
        )

        # for each position, choose the mutate signal value
        for pos in selected_indices:
            # mut_signal_num = random.randint(1, signals_num)
            mut_signal_num = random.randint(1, 4)

            cycle_indice = [pos*signals_num + i for i in range(0,signals_num)]
            signal_indices = random.sample(cycle_indice, random.randint(1, signals_num))

            for index in signal_indices:
                signal_width = self.input_signals[index % len(self.input_signals)][1]
                self.value[index] = random.randint(0, 2**signal_width-1)

        return selected_indices

    def crossover(self, other_seed):
        assert(len(self.value)==len(other_seed.value))
        crossover_point = random.randint(1, len(self.value) - 1)
        self.value = self.value[:crossover_point] + other_seed.value[crossover_point:]
        self.input_file = ''
        self.buggy_output_file = ''
        self.correct_output_file = ''
        self.cov_file = ''
        self.branch_hit_total = []
        self.state_trace = []
        self.out_trace = []

    def cal_fitness(self, init_bug_trigger_seed, similarity_pattern):
        if similarity_pattern=='cov':
            cov_dis = coverage_distance(self.branch_hit_total, init_bug_trigger_seed.branch_hit_total)
            self.fitness = 1 / (1+cov_dis)
        elif similarity_pattern=='dtw':
            if self.sequential_flag==True:
                state_dis = dtw_distance(self.state_trace, init_bug_trigger_seed.state_trace)
            else:
                state_dis = 0
            self.fitness = 1 / (1+state_dis)
        elif similarity_pattern=='merge':
            cov_dis = coverage_distance(self.branch_hit_total, init_bug_trigger_seed.branch_hit_total)
            if self.sequential_flag==True:
                state_dis = dtw_distance(self.state_trace, init_bug_trigger_seed.state_trace)
            else:
                state_dis = 0
            self.fitness = 1 / (1+cov_dis) + 1 / (1+state_dis)
        elif similarity_pattern=='none':
            self.fitness = 1
    

    def cal_distance(self, other_seed, similarity_pattern):
        if similarity_pattern=='cov':
            cov_dis = coverage_distance(self.branch_hit_total, other_seed.branch_hit_total)
            return cov_dis
        elif similarity_pattern=='dtw':
            if self.sequential_flag==True:
                state_dis = dtw_distance(self.state_trace, other_seed.state_trace)
            else:
                state_dis = 1   # avoid return distance=0 and do not add any new seed by diversity mechanism
            return state_dis
        elif similarity_pattern=='merge':
            cov_dis = coverage_distance(self.branch_hit_total, other_seed.branch_hit_total)
            if self.sequential_flag==True:
                state_dis = dtw_distance(self.state_trace, other_seed.state_trace)
            else:
                state_dis = 0
            return cov_dis + state_dis
        elif similarity_pattern=='none':
            return 1            
        # cov_dis = coverage_distance(self.branch_hit_total, other_seed.branch_hit_total)
        # state_dis = dtw_distance(self.state_trace, other_seed.state_trace)
        # print(cov_dis, state_dis)
        # return cov_dis + state_dis
    

    def map_input_file_to_vec(self, input_file):
        self.input_file = input_file
        with open(self.input_file, 'r') as file:
            for line in file:
                line_numbers = line.strip().split(',')
                self.value.extend(int(num, 2) for num in line_numbers)
                

    def map_vec_to_input_file(self, input_file):
        self.input_file = input_file
        signal_num = len(self.input_signals)
        assert(len(self.value) % signal_num == 0)
        s = ''
        for i in range(0, int(len(self.value) / signal_num)):
            line = ''
            for j in range(0, signal_num):
                number = self.value[i*signal_num+j] % (2**self.input_signals[j][1])
                line += str(bin(int(number))[2:]) + ','
            line = line[ :-1]
            s += line + '\n'
        s = s[ :-1]
        with open(self.input_file, 'w') as file:
            file.write(s)
        
    
    def map_cov_file_to_branch_hit(self, cov_file):
        self.cov_file = cov_file
        coverage = read_line_coverage(cov_file)
        self.branch_hit_total = [cov[1] for cov in coverage]


    def map_out_file_to_out_trace(self, correct_out_file, buggy_out_file):
        self.correct_output_file = correct_out_file
        self.buggy_output_file = buggy_out_file
    

    def map_vcd_file_to_state_trace(self, vcd_file, reg_list):
        self.vcd_file = vcd_file
        self.state_trace = read_vcd_trace(vcd_file, reg_list)
    
    
    def set_pass_flag(self, pass_flag):
        self.pass_flag = pass_flag
    