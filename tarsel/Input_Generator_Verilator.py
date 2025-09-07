import json
import os
import sys
sys.path.append('./simulator')
from run_verilator import RunConf, comp_with_verilator, sim_with_verilator, gen_basic_sim_env

class Input_Generator():
    def __init__(self, data_dir, case_info_file):
        self.case_info_file = case_info_file 
        self.data_dir = data_dir

        self.input_file_list = []

        self.read_case_info()

        self.input_dir = os.path.join(data_dir, self.case_name + '/inputs')
        self.sim_dir = os.path.join(data_dir, self.case_name + '/sim')

        os.system(f'rm -rf {self.input_dir}')
        if not os.path.exists(self.input_dir):
            os.makedirs(self.input_dir, exist_ok=True)
            
        os.system(f'rm -rf {self.sim_dir}')
        if not os.path.exists(self.sim_dir):
            os.makedirs(self.sim_dir, exist_ok=True)


    def generate_input(self):
        pass
    
    def read_case_info(self):
        json_file_path = self.case_info_file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            self.case_name = data['case_name']
            self.correct_design_path = data['correct_design']
            self.buggy_design_path = data['buggy_design']
            self.testbench_path = data['testbench']
            self.input_signals = data['input_signals']
            self.bug_trigger_input = data['bug_trigger_input']
            self.include_files = data.get('include_files', [])

    def get_input_files(self):
        return self.input_file_list

# cut initial input file which can trigger bug to generate multiple inputs
class Tarsel_Input_Generator_Verilator(Input_Generator):
    def __init__(self, input_dir, case_info_file):
        super().__init__(input_dir, case_info_file)
        parent_dir = os.path.dirname(self.data_dir)
        self.sim_run_dir_correct = os.path.join(parent_dir, 'sim-tmp/' + self.case_name + '/verilator-tmp-correct')
        self.sim_run_dir_buggy = os.path.join(parent_dir, 'sim-tmp/' + self.case_name + '/verilator-tmp-buggy')

        if not os.path.exists(self.sim_run_dir_correct):
            os.makedirs(self.sim_run_dir_correct)
        if not os.path.exists(self.sim_run_dir_buggy):
            os.makedirs(self.sim_run_dir_buggy)

    # generate input from original input clock by clock
    def generate_fine_grained_input(self):
        with open(self.bug_trigger_input, 'r') as f:
            lines = f.readlines()

        input_file_list = []
        for i in range(len(lines)):
            input_file = f'{self.input_dir}/input_{i+1}.txt'
            with open(input_file, 'w') as f:
                part_lines = lines[:i+1]

                # delete the '\n' in the last line of the generated input file 
                # this is very important, or it will make SV testbench run another extra cycle
                part_lines[-1] = part_lines[-1].rstrip('\n')

                f.writelines(part_lines)

            self.input_file_list.append(input_file)


    # generate sampled input according to Tarsel paper
    def generate_tarsel_input(self, delta_F, delta_f):
        sample_times = self.gen_sample_times(delta_F, delta_f)

        with open(self.bug_trigger_input, 'r') as f:
            lines = f.readlines()

        for i in sorted(sample_times):
            input_file = f'{self.input_dir}/input_end-time={i}.txt'
            with open(input_file, 'w') as f:
                part_lines = lines[:i]

                # delete the '\n' in the last line of the generated input file 
                # this is very important, or it will make SV testbench run another extra cycle
                part_lines[-1] = part_lines[-1].rstrip('\n')

                f.writelines(part_lines)

            self.input_file_list.append(input_file)


    # simulate initial input on correct and buggy designs
    def sim_correct_and_buggy_designs(self):

        # using the same verilator compilation config with Wit-HW, will save compilation time
        verilator_run_conf = RunConf(
            defines=[("DUMP_TRACE", "1")],
            timeout=30,
        )

        # only need to simulate the initial input
        input_file = self.bug_trigger_input
        ##########################
        ### for correct design ###
        ##########################
        print('Compiling correct design...')
        gen_basic_sim_env(self.sim_run_dir_correct, [self.correct_design_path] + self.include_files, self.testbench_path, input_file)
        verilator_compile_success = comp_with_verilator(self.sim_run_dir_correct, [], verilator_run_conf)
        assert(verilator_compile_success==True)
        
        print('Simulating correct design...')
        verilator_sim_success = sim_with_verilator(self.sim_run_dir_correct, verilator_run_conf)
        assert(verilator_sim_success==True)

        output_file = os.path.join(self.sim_run_dir_correct, "output-signals.txt")
        prefix = "correct-init-" + input_file.split('/')[-1].split('.')[0] + '-'
        correct_output_data_file = os.path.join(self.sim_dir, prefix + "output-signals.txt")
        os.system(f'cp {output_file} {correct_output_data_file}')

        ##########################
        ### for buggy design ###
        ##########################
        print('Compiling buggy design...')
        gen_basic_sim_env(self.sim_run_dir_buggy, [self.buggy_design_path] + self.include_files, self.testbench_path, input_file)
        verilator_compile_success = comp_with_verilator(self.sim_run_dir_buggy, [], verilator_run_conf)
        assert(verilator_compile_success==True)

        # only need to compile once
        print('Simulating buggy design...')
        verilator_sim_success = sim_with_verilator(self.sim_run_dir_buggy, verilator_run_conf)
        assert(verilator_sim_success==True)

        output_file = os.path.join(self.sim_run_dir_buggy, "output-signals.txt")
        prefix = "buggy-init-" + input_file.split('/')[-1].split('.')[0] + '-'
        buggy_output_data_file = os.path.join(self.sim_dir, prefix + "output-signals.txt")
        os.system(f'cp {output_file} {buggy_output_data_file}')

        return correct_output_data_file, buggy_output_data_file

    
    # compare the correct and buggy output 
    # generate sample points
    #   parameter: delta_F, delta_f
    #   error time: for each time i where correct and buggy has different output
    #   sample points: 
    #       sample with step length delta_f 
    #       in [err_time_i - delta_F, err_time_i + delta_F]
    def gen_sample_times(self, delta_F, delta_f):
        correct_output_data_file, buggy_output_data_file = self.sim_correct_and_buggy_designs()

        sample_times = set()
        with open(correct_output_data_file, "r") as correct_output, open(buggy_output_data_file, "r") as buggy_output:
            correct_lines = correct_output.readlines()
            buggy_lines = buggy_output.readlines()
            assert(len(correct_lines)==len(buggy_lines))
            
            for i in range(1, len(correct_lines)):
                correct_line = correct_lines[i]
                buggy_line = buggy_lines[i]

                if correct_line != buggy_line:
                    for x in range(i - delta_F, i + delta_F + delta_f, delta_f):
                        if x < len(correct_lines) and x > 0:
                            sample_times.add(x)
                    break   # only select the first error position

        assert len(sample_times)!=0, "initial input didn't trigger bug"

        return sample_times