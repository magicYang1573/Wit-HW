from Init_Input_Simulator import Init_Input_Simulator
from Fuzz_Engine import Fuzz_Engine
from Fuzz_Bug_Loc import Fuzz_Bug_Loc
import argparse
import os
import time

def main():

    parser = argparse.ArgumentParser(description='Run Wit-HW')
    
    parser.add_argument('--data_dir', type=str, default='./example/withw',
                        help='Directory to store generated running data')

    parser.add_argument('--case_info_file', type=str,
                        default="buggy_designs/fsm_16/bug-info-1.json",
                        help='Path to the case info JSON file')

    parser.add_argument('--similarity', type=str, default='merge',
                        help='Heuristic method to use for similarity')
    
    parser.add_argument('--diversity', type=str, default='yes',
                        help='Heuristic method to use for diversity')   

    parser.add_argument('--iter', type=int, default=100,
                        help='Iteration number') 

    parser.add_argument('--mutate_rate', type=float, default=0.3,
                        help='Mutation rate for seed input sequence') 

    args = parser.parse_args()


    data_dir = args.data_dir
    os.makedirs(data_dir, exist_ok=True)
    case_info_file = args.case_info_file
    
    config = {
        'iter': args.iter,
        'max_corpus_size': 50,
        'similarity': args.similarity,
        'diversity': args.diversity,
        'mutate_rate': args.mutate_rate,
        'choose_init_seed_rate': 0.2,
        'pos_pri_update_coefficient': 0.1,
        'pos_failed_loss': 5
    }

    start_time = time.time()

    init_sim = Init_Input_Simulator(data_dir, case_info_file)
    init_sim.sim_buggy_and_correct_designs()
    correct_output_path, buggy_output_path, buggy_cov_path, buggy_vcd_path = init_sim.get_init_sim_data()

    
    fuzz_engine = Fuzz_Engine(data_dir, case_info_file, buggy_cov_path, buggy_vcd_path, config)
    fuzz_engine.fuzz(config['iter'])

    pass_seeds, failed_seeds = fuzz_engine.get_seeds()

    fuzz_bug_loc = Fuzz_Bug_Loc(data_dir, case_info_file)
    cov_example = fuzz_engine.get_cov_example()
    top_pass_seeds = sorted(pass_seeds, key=lambda seed: seed.fitness, reverse=True)[:10]
    
    # for seed in top_pass_seeds:
    #     print('=========')
    #     print(seed)
    #     print(seed.fitness)

    fuzz_bug_loc.cal_suspicious(top_pass_seeds, failed_seeds)
    fuzz_bug_loc.report_suspicious_rank(cov_example)

    fuzz_engine.show_distance()

    end_time = time.time()

    print(f'Wit-HW time: {end_time - start_time:.2f}')

if __name__ == "__main__":
    main()