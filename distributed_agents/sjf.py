import json
import paramiko
import requests
import time
import sys
import os
from datetime import datetime, timezone, timedelta
from multiprocessing import Process, Queue
from collections import defaultdict
import queue
from concurrent.futures import ProcessPoolExecutor
from collections import deque 
 
import numpy as np
from job_distribution import UE_Distribution
from utils import *
import requests

ENDPOINT = "http://localhost:8000/collect"


#The episode will end once I handle all imsis from my pool 

remote_folder = '/home/leon/ue_controller/pid'
local_folder = './pid'



   
class SJFPolicy:
    # (imsi, timestamp, ue_bw, ue_len, remaining_bw)
    def select_action(self, obs):
        min=np.inf
        action = - 1
        time_needed = -1 
        bw_needed = 0
        imsi = 0
        q_size = 3 # I have 3 queue size
        #[ 0  6  1  0  7  8  0  9 22 25]

        for i in range(q_size):
             
             if obs[i*q_size+2] < min:
                     min = obs[i*q_size+2]
                     action = i
        print ('[INFO] sjf action chosen is ', action)           
        return (action)  

import argparse

def main(arg1, arg2, arg3):
    print(f"Arg1: {arg1}, Arg2: {arg2}, Arg3: {arg3}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arg1", help="First argument")
    parser.add_argument("arg2", help="Second argument")
    parser.add_argument("arg3", help="Third argument")
    args = parser.parse_args()
    
    main(args.arg1, args.arg2, args.arg3)

    num_episodes = int(args.arg1)
    a=args.arg2
    job_small_chance=args.arg3



    
    max_job_len = 60 # seconds
    bw_min = 3
    bw_max=5
    q_size=3

    distribution=UE_Distribution(max_job_len, job_small_chance, bw_min, bw_max)
    ue_len1, ue_bw1 = distribution.binomial_model()
    distribution=UE_Distribution(max_job_len, job_small_chance, bw_min, bw_max)
    ue_len2, ue_bw2 = distribution.binomial_model()
    distribution=UE_Distribution(max_job_len, job_small_chance, bw_min, bw_max)
    ue_len3, ue_bw3 = distribution.binomial_model()    
    distribution=UE_Distribution(max_job_len, job_small_chance, bw_min, bw_max)
    ue_len4, ue_bw4 = distribution.binomial_model()
    distribution=UE_Distribution(max_job_len, job_small_chance, bw_min, bw_max)
    ue_len5, ue_bw5 = distribution.binomial_model()
    distribution=UE_Distribution(max_job_len, job_small_chance, bw_min, bw_max)
    ue_len6, ue_bw6 = distribution.binomial_model()  
        
    bw1_left = 15
    bw2_left = 15

    current_time = datetime.now()
    timestamp = int(current_time.timestamp())

    timestamp1=timestamp
    timestamp2=timestamp
    timestamp3=timestamp
    timestamp4=timestamp
    timestamp5=timestamp
    timestamp6=timestamp

    
    
    from env import UEAdmissionEnv
    env = UEAdmissionEnv(timestamp1, ue_bw1, ue_len1, \
                 timestamp2, ue_bw2, ue_len2,
                 timestamp3, ue_bw3, ue_len3, \
                 timestamp4, ue_bw4, ue_len4, \
                 timestamp5, ue_bw5, ue_len5,
                 timestamp6, ue_bw6, ue_len6, \
                 bw1_left, bw2_left, max_job_len, job_small_chance,bw_min,bw_max,a)      
    
    system_init() #each episode starts with a clean system     
   
    import csv
    log_path = f"csvs/sjf_episode_rewards_{num_episodes}_{a}_{job_small_chance}.csv"

    # Open the file and write the header once
    with open(log_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Episode", "TotalReward"])
  
       
    episode_rewards=[]

    agents = ["UPF500", "UPF250"]     
    
    policy = SJFPolicy()      

    done=False

    for episode in range (num_episodes):
       env.reset()
       ep_reward = 0
       rewards = []
       episode_total_reward=0
       time.sleep(120) # for the threads to finish from the previous episose
       delete_local_files()
       init_gnb("gnb")


       print ('in episode ', episode)
    #    if done == False:
    #         doneStr= "False"
       
       for step in range (20):
            print ('In step ', step)
            agent_id = env.agent_selection
            obs = env.observe(agent_id)
            print (obs)
            # I will save the state in the db
            action = policy.select_action(obs)

            print ('action chosen is ', action)

            obs, reward, done, trancation, info = env.step(action)
            print (reward)
            ep_reward = reward

            obs = env.observe(agent_id)

                            
            rewards.append(ep_reward)
            
            if done:
                episode_total_reward = np.sum(rewards)
                episode_rewards.append(episode_total_reward)
                print ('the total reward of this episode has been ', episode_total_reward)
                print ("i go to next episode")
                  # Append to CSV
                with open(log_path, mode="a", newline="") as f:
                     writer = csv.writer(f)
                     writer.writerow([episode, episode_total_reward])
                          
                break # means I start a new episode

        

        
    print(f"\nAverage reward over all episodes: {np.mean(episode_rewards):.2f}")

   