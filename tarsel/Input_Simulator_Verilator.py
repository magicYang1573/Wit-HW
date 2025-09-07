import json
import os
import sys
sys.path.append('./simulator')
from run_verilator import RunConf, comp_with_verilator, sim_with_verilator, gen_basic_sim_env

# Tarsel only uses one initial input and cut them to different input
# for buggy design, each input should be simulated to get coverage
# for correct design, only the initial input need to be simulated

class Tarsel_Input_Simulator_Verilator():
    def __init__(self, data_dir, input_files, case_info_file):
        self.input_files = input_files  # list to store generated inputs files
        self.case_info_file = case_info_file    
        
        self.read_case_info()
        
        self.data_dir = os.path.join(data_dir, self.case_name + '/sim')

        parent_dir = os.path.dirname(data_dir)
        self.sim_run_dir_correct = os.path.join(parent_dir, 'sim-tmp/' + self.case_name + '/verilator-tmp-correct')
        self.sim_run_dir_buggy = os.path.join(parent_dir, 'sim-tmp/' + self.case_name + '/verilator-tmp-buggy')

        # os.system(f'rm -rf {self.data_dir}')
        # if not os.path.exists(self.data_dir):
        #     os.makedirs(self.data_dir, exist_ok=True)

        self.sim_data = {}

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


    # return dict { input_file : [correct_output, buggy_output, buggy_cov] }
    # for cutted input file, correct_output = ""
    def get_sim_data(self):
        # print("=== Simulation Result ===\n", self.sim_data)
        return self.sim_data

        
    # simulate buggy and correct designs using all the input files
    def sim_buggy_and_correct_designs(self):
        
        verilator_run_conf = RunConf(
            defines=[("DUMP_TRACE", "1")],
            timeout=30,
        )
        
        ##########################
        ### for correct design ###
        ##########################
        input_file = self.input_files[-1]
        gen_basic_sim_env(self.sim_run_dir_correct, [self.correct_design_path] + self.include_files, self.testbench_path, input_file)
        
        ## already compile when generating input
        # verilator_compile_success = comp_with_verilator(self.sim_run_dir_correct, ['dut.sv', 'testbench.sv'], verilator_run_conf)
        # assert(verilator_compile_success==True)

        # only need to simulate the initial input
        verilator_sim_success = sim_with_verilator(self.sim_run_dir_correct, verilator_run_conf)
        assert(verilator_sim_success==True)

        output_file = os.path.join(self.sim_run_dir_correct, "output-signals.txt")
        prefix = "correct-" + input_file.split('/')[-1].split('.')[0] + '-'
        output_data_file = os.path.join(self.data_dir, prefix + "output-signals.txt")
        os.system(f'cp {output_file} {output_data_file}')

        
        # cov_dir = os.path.join(self.verilator_running_dir, "coverage")
        # prefix = "correct-" + input.split('/')[-1].split('.')[0] + '-'
        # cov_data_file = os.path.join(self.data_dir, prefix + "coverage")
        # os.system(f'cp -dr {cov_dir} {cov_data_file}')

        self.sim_data[input_file] = [output_data_file]


        ########################
        ### for buggy design ###
        ########################    
        ## already compile when generating input
        # verilator_compile_success = comp_with_verilator(self.sim_run_dir_buggy, ['dut.sv', 'testbench.sv'], verilator_run_conf)
        # assert(verilator_compile_success==True)

        # only need to compile once
        for input in self.input_files:
            gen_basic_sim_env(self.sim_run_dir_buggy, [], '', input)
            verilator_sim_success = sim_with_verilator(self.sim_run_dir_buggy, verilator_run_conf)
            assert(verilator_sim_success==True)

            output_file = os.path.join(self.sim_run_dir_buggy, "output-signals.txt")
            prefix = "buggy-" + input.split('/')[-1].split('.')[0] + '-'
            output_data_file = os.path.join(self.data_dir, prefix + "output-signals.txt")
            os.system(f'cp {output_file} {output_data_file}')

            cov_log = os.path.join(self.sim_run_dir_buggy, "coverage.dat")
            prefix = "buggy-" + input.split('/')[-1].split('.')[0] + '-'
            cov_data_file = os.path.join(self.data_dir, prefix + "coverage")
            os.system(f'cp {cov_log} {cov_data_file}')

            if input!=self.input_files[-1]:
                self.sim_data[input] = [""]
            self.sim_data[input].append(output_data_file)
            self.sim_data[input].append(cov_data_file)


