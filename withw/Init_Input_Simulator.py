import json
import os
import sys
sys.path.append('./simulator')
from run_verilator import RunConf, comp_with_verilator, sim_with_verilator, gen_basic_sim_env

# 1> simulate correct designs for correct behaviors
# 2> simulate failed designs for buggy trace

class Init_Input_Simulator():
    def __init__(self, data_dir, case_info_file):
        self.case_info_file = case_info_file    
        self.read_case_info()
        
        parent_dir = os.path.dirname(data_dir)
        self.sim_run_dir_correct = os.path.join(parent_dir, 'sim-tmp/' + self.case_name + '/verilator-tmp-correct')
        self.sim_run_dir_buggy = os.path.join(parent_dir, 'sim-tmp/' + self.case_name + '/verilator-tmp-buggy')

        self.data_dir = os.path.join(data_dir, self.case_name + '/sim')
        os.system(f'rm -rf {self.data_dir}')
        os.makedirs(self.data_dir, exist_ok=True)

        self.correct_output_path = ''
        self.buggy_output_path = ''
        self.buggy_cov_path = ''

    def read_case_info(self):
        json_file_path = self.case_info_file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            self.case_name = data['case_name']
            self.correct_design_path = data['correct_design']
            self.buggy_design_path = data['buggy_design']
            self.testbench_path = data['testbench']
            self.input_signals = data['input_signals']
            self.buggy_input_file =  data['bug_trigger_input']
            self.include_files = data.get('include_files', [])
            

    # return dict { input_file : [correct_output, buggy_output, buggy_cov] }
    # for cutted input file, correct_output = ""
    def get_init_sim_data(self):
        return self.correct_output_path, self.buggy_output_path, self.buggy_cov_path, self.buggy_vcd_path

        
    # simulate buggy and correct designs using all the input files
    def sim_buggy_and_correct_designs(self):
        
        verilator_run_conf = RunConf(
            defines=[("DUMP_TRACE", "1")],
            timeout=30,
        )
        
        ##########################
        ### for correct design ###
        ##########################
        input_file = self.buggy_input_file

        print('Compiling correct design...')
        gen_basic_sim_env(self.sim_run_dir_correct, [self.correct_design_path] + self.include_files, self.testbench_path, input_file)
        
        verilator_compile_success = comp_with_verilator(self.sim_run_dir_correct, [], verilator_run_conf)
        assert(verilator_compile_success==True)

        print('Simulating correct design...')
        verilator_sim_success = sim_with_verilator(self.sim_run_dir_correct, verilator_run_conf)
        assert(verilator_sim_success==True)

        output_file = os.path.join(self.sim_run_dir_correct, "output-signals.txt")
        prefix = "correct-" + input_file.split('/')[-1].split('.')[0] + '-'
        output_data_file = os.path.join(self.data_dir, prefix + "output-signals.txt")
        os.system(f'cp {output_file} {output_data_file}')

        self.correct_output_path = output_data_file


        ########################
        ### for buggy design ###
        ########################
        print('Compiling buggy design...')
        gen_basic_sim_env(self.sim_run_dir_buggy, [self.buggy_design_path] + self.include_files, self.testbench_path, input_file)
        
        verilator_compile_success = comp_with_verilator(self.sim_run_dir_buggy, [], verilator_run_conf)
        assert(verilator_compile_success==True)

        print('Simulating buggy design...')
        verilator_sim_success = sim_with_verilator(self.sim_run_dir_buggy, verilator_run_conf)
        assert(verilator_sim_success==True)

        output_file = os.path.join(self.sim_run_dir_buggy, "output-signals.txt")
        prefix = "buggy-" + input_file.split('/')[-1].split('.')[0] + '-'
        output_data_file = os.path.join(self.data_dir, prefix + "output-signals.txt")
        os.system(f'cp {output_file} {output_data_file}')

        cov_log = os.path.join(self.sim_run_dir_buggy, "coverage.dat")
        prefix = "buggy-" + input_file.split('/')[-1].split('.')[0] + '-'
        cov_data_file = os.path.join(self.data_dir, prefix + "coverage")
        os.system(f'cp {cov_log} {cov_data_file}')

        cov_log = os.path.join(self.sim_run_dir_buggy, "coverage.dat")
        prefix = "buggy-" + input_file.split('/')[-1].split('.')[0] + '-'
        cov_data_file = os.path.join(self.data_dir, prefix + "coverage")
        os.system(f'cp {cov_log} {cov_data_file}')

        vcd_log = os.path.join(self.sim_run_dir_buggy, "dump.vcd")
        prefix = "buggy-" + input_file.split('/')[-1].split('.')[0] + '-'
        vcd_data_file = os.path.join(self.data_dir, prefix + "vcd")
        os.system(f'cp {vcd_log} {vcd_data_file}')

        self.buggy_output_path = output_data_file
        self.buggy_cov_path = cov_data_file
        self.buggy_vcd_path = vcd_data_file


