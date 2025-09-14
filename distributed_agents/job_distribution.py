import numpy as np


class UE_Distribution:

    def __init__(self,  max_job_len, job_small_chance, bw_min, bw_max):
        
        
        self.job_small_chance = float(job_small_chance)

        self.job_len_big_lower = max_job_len * 2 / 3
        self.job_len_big_upper = max_job_len

        self.job_len_small_lower = 1
        self.job_len_small_upper = max_job_len / 3

        self.bw_min = bw_min
        self.bw_max = bw_max

        
  
    def binomial_model(self):

        # -- UE request time length --
        if np.random.rand() < self.job_small_chance:  # small job
            ue_len = np.random.randint(self.job_len_small_lower,
                                       self.job_len_small_upper + 1)
        else:  # big job
            ue_len = np.random.randint(self.job_len_big_lower,
                                       self.job_len_big_upper + 1)

        ue_bw = np.random.randint(self.bw_min, self.bw_max)   
        #ue_bw = self.bw_min      # 5                        
        return ue_len, ue_bw



