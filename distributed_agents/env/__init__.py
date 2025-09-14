from .env import UEAdmissionEnv
from pettingzoo.utils import wrappers
from job_distribution import UE_Distribution
from utils import system_init
from datetime import datetime, timezone, timedelta

def make_env():

    max_job_len = 30 # seconds
    job_small_chance = 0.8
    bw_min = 5
    bw_max=10
    q_size=3
    q1 = [] # agent 1 queue
    q2 = [] # agent 2 queue

    # each agent has its own queue. 
    for ue in range (q_size):
            imsi =   999991000000081 + ue
            distribution=UE_Distribution(max_job_len, job_small_chance, bw_min, bw_max)
            ue_len, ue_bw = distribution.binomial_model()
        
                        
            tuple= (0, ue_len)
            
            q1.append(tuple)
   
    #print(q1)    
    
    for ue in range (q_size):
            imsi =   999991000000084 + ue        
            distribution=UE_Distribution(max_job_len, job_small_chance, bw_min, bw_max)
            ue_len, ue_bw = distribution.binomial_model()
        
            tuple= (0, ue_len)
            
            q2.append(tuple)
   
    #print(q2)    
        
    
    system_init() #each episode starts with a clean system     
   


    return wrappers.CaptureStdoutWrapper(UEAdmissionEnv(q1, q2, q_size, render_mode="human"))
