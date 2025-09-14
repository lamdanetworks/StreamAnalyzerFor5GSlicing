import torch
import torch.nn as nn
import torch.nn.functional as F
from multiprocessing import Process, Queue
from utils import get_networks_stats, init_gnb, delete_local_files
class DQN(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_sizes=[64, 64]):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_sizes[0])
        self.fc2 = nn.Linear(hidden_sizes[0], hidden_sizes[1])
        self.out = nn.Linear(hidden_sizes[1], output_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x)  # Q-values
    

import random
from collections import deque, namedtuple

Transition = namedtuple('Transition', ('state', 'action', 'reward', 'next_state', 'done'))



import numpy as np
from env import UEAdmissionEnv
from datetime import datetime, timezone, timedelta
from job_distribution import UE_Distribution
# each agent has its own queue. 

max_job_len = 60 # seconds
job_small_chance = 0.3
bw_min = 5
bw_max=10
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

env = UEAdmissionEnv(timestamp1, ue_bw1, ue_len1, \
                 timestamp2, ue_bw2, ue_len2,
                 timestamp3, ue_bw3, ue_len3, \
                 timestamp4, ue_bw4, ue_len4, \
                 timestamp5, ue_bw5, ue_len5,
                 timestamp6, ue_bw6, ue_len6, \
                 bw1_left, bw2_left, max_job_len, job_small_chance,bw_min,bw_max)

agent_id = "UPF250"
obs = env.reset()[agent_id]
obs_dim = np.prod(obs.shape)
n_actions = env.action_spaces[agent_id].n
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
policy_net = DQN(obs_dim, n_actions).to(device)
target_net = DQN(obs_dim, n_actions).to(device)
#target_net.load_state_dict(policy_net.state_dict()) # called when training mode in on
target_net.load_state_dict(torch.load("best_model/best_model.pth"))
target_net.eval()

# import torch

# # Recreate the model structure
# model = YourModelClass(...)  # same architecture as during training
# model.eval()  # important for evaluation mode



optimizer = torch.optim.Adam(policy_net.parameters(), lr=1e-5)

# Traing loop
import torch.nn.functional as F

batch_size = 64
gamma = 0.99
eps_start = 1.0
eps_end = 0.05
eps_decay = 1000
target_update_freq = 10

steps_done = 0
num_episodes = 1 # should 1000 at least

best_reward = float('-inf')  
model_save_path = "best_model/best_model.pth"

import csv

log_path = "csvs/dqn_episode_rewards.csv"
# Open the file and write the header once
with open(log_path, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Episode", "TotalReward"])

recent_rewards = []

import time

for episode in range(num_episodes):
    time.sleep(60) # for the threads to finish from the previous episose
    obs_dict = env.reset()
    delete_local_files()
    state = obs_dict[agent_id].flatten()
    total_reward = 0
    init_gnb("gnb")

    for t in range(20):  # max steps per episode. It opens a new thread for 
                            # every step, this is why I have so many devices created.

        # Epsilon-greedy action
        eps = eps_end + (eps_start - eps_end) * np.exp(-steps_done / eps_decay)
        if random.random() < eps:
            action = random.randrange(n_actions)
        else:
            with torch.no_grad():
                state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
                q_values = policy_net(state_tensor)
                action = q_values.argmax().item()

        _, reward, done, _, _ = env.step(action)
        #print ('action chosen is ', action,  'and reward is', reward)

        next_state = env.observe(agent_id).flatten()
   
        state = next_state
        total_reward += reward
        steps_done += 1
      
       
        if done:
            break
        # end of the for loop 
             
    # logging episode total reward
    with open(log_path, mode="a", newline="") as f:
                     writer = csv.writer(f)
                     writer.writerow([episode, total_reward])

    recent_rewards.append(total_reward)
   

    print(f"Episode {episode}, total_reward = {total_reward:.3f}")



