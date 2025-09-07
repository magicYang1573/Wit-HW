import os
from Input_Generator_Verilator import Input_Generator, Tarsel_Input_Generator_Verilator
from Input_Simulator_Verilator import Tarsel_Input_Simulator_Verilator
from Tarsel_Bug_Loc_Verilator import Tarsel_Bug_Loc_Verilator
# from simulator.coverage_extract import read_vcs_cond_coverage, read_vcs_line_coverage

def main():
    data_dir = "./example/tarsel"  # dir to store generated running data
    os.makedirs(data_dir, exist_ok=True)
    
    ## example case
    case_info_file = "./buggy_designs/decoder_3_to_8/bug-info-1.json"  

    generator = Tarsel_Input_Generator_Verilator(data_dir, case_info_file)

    delta_F = 2
    delta_f = 1
    generator.generate_tarsel_input(delta_F, delta_f)
    input_files = generator.get_input_files()
    print('Tarsel sampled input files:')
    print(input_files)

    input_simulator = Tarsel_Input_Simulator_Verilator(data_dir, input_files, case_info_file)
    input_simulator.sim_buggy_and_correct_designs()

    sim_data_dict = input_simulator.get_sim_data()
    tarsel_loc = Tarsel_Bug_Loc_Verilator(data_dir, case_info_file, input_files, sim_data_dict)
    tarsel_loc.get_suspicious_rank()


if __name__ == "__main__":
    main()