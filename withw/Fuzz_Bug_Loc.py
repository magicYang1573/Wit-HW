import math
import json
import os

class Fuzz_Bug_Loc():
    def __init__(self, data_dir, case_info_file):
        self.suspicious_list = []
        self.case_info_file = case_info_file
        self.read_case_info()
        self.result_file = os.path.join(data_dir, self.case_name + '/result.txt')

    def read_case_info(self):
        json_file_path = self.case_info_file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            self.case_name = data['case_name']

    def cal_suspicious(self, pass_seeds, failed_seeds):
        cov_num = len(failed_seeds[0].branch_hit_total)
        suspicious_list = [0 for _ in range(cov_num)]
        self.aep = [0 for _ in range(cov_num)]
        self.aef = [0 for _ in range(cov_num)]
        self.anf = [0 for _ in range(cov_num)]
        self.anp = [0 for _ in range(cov_num)]
        
        for seed in pass_seeds + failed_seeds:
            for i in range(0, cov_num):
                cov_hit = seed.branch_hit_total[i]
                if cov_hit > 0:
                    if seed.pass_flag:    
                        self.aep[i] += 1
                    else:
                        self.aef[i] += 1
                else:
                    if seed.pass_flag:    
                        self.anp[i] += 1
                    else:
                        self.anf[i] += 1

            
        # for seed in pass_seeds + failed_seeds:
        #     for i in range(0, cov_num):
        #         cov_hit = seed.branch_hit_total[i]
        #         if cov_hit > 0:
        #             if seed.pass_flag:    
        #                 self.aep[i] += cov_hit
        #             else:
        #                 self.aef[i] += cov_hit
        #         else:
        #             if seed.pass_flag:    
        #                 self.anp[i] += 1
        #             else:
        #                 self.anf[i] += 1

        for i in range(0, cov_num):
            # formula used in Tarsel
            # suspicious_list[i] = aef[i]*math.sqrt(abs(aep[i]-aef[i]+anf[i]-anp[i]))   

            # formula used in Diwi
            if self.aef[i]==0:
                suspicious_list[i] = 0
            else:
                suspicious_list[i] = self.aef[i] / math.sqrt((self.aef[i] + self.anf[i]) * (self.aef[i] + self.aep[i])) 

            # Hamming 
            # suspicious_list[i] = self.aef[i] + self.anp[i]
        
        self.suspicious_list = suspicious_list

    
    def report_suspicious_rank(self, cov_example):
        assert(len(self.suspicious_list)==len(cov_example))
        cov_num = len(cov_example)
        rank_index =  [i for i, _ in sorted(enumerate(self.suspicious_list), key=lambda x: x[1], reverse=True)]
        # for i, r in enumerate(rank_index):
        #     if r < cov_num:
        #         print(f'Rank {i+1} (Suspicious: {self.suspicious_list[r]}): Branch: {cov_example[r][0]}')
        with open(self.result_file, 'w') as result_file:
            for i, r in enumerate(rank_index):
                if r < cov_num:
                    result_file.write(f'Rank {i+1} (Suspicious: {self.suspicious_list[r]}): Branch: {cov_example[r][0]}\n')
                    result_file.write(f'ep: {self.aep[r]}; ef: {self.aef[r]}; np: {self.anp[r]}; nf: {self.anf[r]}\n')
                    result_file.write('-----------------------------------------------------------------------------------\n')