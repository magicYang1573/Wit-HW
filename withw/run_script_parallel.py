import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_wit_hw(case_info_file, data_dir, similarity, diversity, iter, mutate_rate, log_file):
    command = [
        'python', 'fuzz/run.py', 
        '--case_info_file', case_info_file, 
        '--data_dir', data_dir, 
        '--similarity', similarity,
        '--diversity', diversity,
        '--iter', str(iter),
        '--mutate_rate', str(mutate_rate)
    ]
    print(command)

    with open(log_file, 'a') as log:
        log.write(f'\n\nRunning wit-hw for: {case_info_file}')
        subprocess.run(command, stdout=log, stderr=log)

def main():
    case_info_files = [
        "./buggy_designs/decoder_3_to_8/bug-info-1.json",
        "./buggy_designs/decoder_3_to_8/bug-info-2.json",
        "./buggy_designs/decoder_3_to_8/bug-info-3.json",
        "./buggy_designs/decoder_3_to_8/bug-info-4.json",
        "./buggy_designs/decoder_3_to_8/bug-info-5.json",
        "./buggy_designs/decoder_3_to_8/bug-info-6.json",
        "./buggy_designs/alu/bug-info-1.json",
        "./buggy_designs/alu/bug-info-2.json",
        "./buggy_designs/alu/bug-info-3.json",
        "./buggy_designs/alu/bug-info-4.json",
        "./buggy_designs/alu/bug-info-5.json",
        "./buggy_designs/alu/bug-info-6.json",
        "./buggy_designs/counter/bug-info-1.json",
        "./buggy_designs/counter/bug-info-2.json",
        "./buggy_designs/counter/bug-info-3.json",
        "./buggy_designs/fsm_16/bug-info-1.json",
        "./buggy_designs/fsm_16/bug-info-2.json",
        "./buggy_designs/fsm_16/bug-info-3.json",
        "./buggy_designs/fsm_16/bug-info-4.json",
        "./buggy_designs/led_controller/bug-info-1.json",
        "./buggy_designs/led_controller/bug-info-2.json",
        "./buggy_designs/led_controller/bug-info-3.json",
        "./buggy_designs/led_controller/bug-info-4.json",
        "./buggy_designs/arbiter/bug-info-1.json",
        "./buggy_designs/arbiter/bug-info-2.json",
        "./buggy_designs/arbiter/bug-info-3.json"
        "./buggy_designs/i2c/bug-info-1.json",
        "./buggy_designs/i2c/bug-info-2.json",
        "./buggy_designs/i2c/bug-info-3.json",
        "./buggy_designs/i2c/bug-info-4.json",
        "./buggy_designs/i2c/bug-info-5.json",
        "./buggy_designs/i2c/bug-info-6.json",
        "./buggy_designs/reed_solomon_decoder/bug-info-1.json", 
        "./buggy_designs/reed_solomon_decoder/bug-info-2.json", 
        "./buggy_designs/reed_solomon_decoder/bug-info-3.json", 
        "./buggy_designs/sha3/low_throughput_core/bug-info-1.json",
        "./buggy_designs/sha3/low_throughput_core/bug-info-2.json",
        "./buggy_designs/sha3/low_throughput_core/bug-info-3.json",
        "./buggy_designs/sdram_controller/bug-info-1.json",
        "./buggy_designs/sdram_controller/bug-info-2.json",
        "./buggy_designs/sdram_controller/bug-info-3.json"
    ]


    data_dir = './example/withw

    # similarity = 'dtw'   # only use dtw as similarity metric
    # similarity = 'cov'   # only use cov as similarity metric
    similarity = 'merge'  # use cov+dtw as similarity metric
    # similarity = 'none'  # use no similarity metric

    diversity = 'yes'       # use diversity-driven metric
    # diversity = 'none'      # use no diversity metric

    iter = 300

    # 'mutation rate' effects the localization accuracy, as the test case has varying length
    # users could adjust the mutation rate of each test case according to the 'fitness'
    mutate_rate = 0.2   

    os.makedirs(data_dir, exist_ok=True)
    log_file = os.path.join(data_dir, 'log')
    os.system(f'rm -rf {log_file}')

    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(run_wit_hw, case_info_file, data_dir, similarity, diversity, iter, mutate_rate, log_file): case_info_file for case_info_file in case_info_files}
        
        for future in as_completed(futures):
            case_info_file = futures[future]
            try:
                future.result()  # Get the result to raise exceptions if occurred
                print(f'Successfully run wit-hw for: {case_info_file}')
            except Exception as e:
                print(f'Error occurred while running wit-hw for {case_info_file}: {e}')

if __name__ == "__main__":
    main()
