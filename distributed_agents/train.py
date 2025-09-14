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

    import random
    from collections import deque, namedtuple

    Transition = namedtuple('Transition', ('state', 'action', 'reward', 'next_state', 'done'))

    class ReplayBuffer:
        def __init__(self, capacity=10000):
            self.buffer = deque(maxlen=capacity)

        def push(self, *args):
            self.buffer.append(Transition(*args))

        def sample(self, batch_size):
            return random.sample(self.buffer, batch_size)

        def __len__(self):
            return len(self.buffer)
        
    import numpy as np
    from env import UEAdmissionEnv
    from datetime import datetime, timezone, timedelta
    from job_distribution import UE_Distribution
    # each agent has its own queue. 

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

    env = UEAdmissionEnv(timestamp1, ue_bw1, ue_len1, \
                    timestamp2, ue_bw2, ue_len2,
                    timestamp3, ue_bw3, ue_len3, \
                    timestamp4, ue_bw4, ue_len4, \
                    timestamp5, ue_bw5, ue_len5,
                    timestamp6, ue_bw6, ue_len6, \
                    bw1_left, bw2_left, max_job_len, job_small_chance,bw_min,bw_max,a)

    agent_id = "UPF500"
    obs = env.reset()[agent_id]
    obs_dim = np.prod(obs.shape)
    n_actions = env.action_spaces[agent_id].n

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    policy_net = DQN(obs_dim, n_actions).to(device)
    target_net = DQN(obs_dim, n_actions).to(device)
    target_net.load_state_dict(policy_net.state_dict())
    target_net.eval()

    optimizer = torch.optim.Adam(policy_net.parameters(), lr=1e-5)
    buffer = ReplayBuffer(10000)

    # Traing loop using plain pytorch starts in a while, first defining the training params.
    import torch.nn.functional as F

    batch_size = 64
    gamma = 0.99
    eps_start = 1.0
    eps_end = 0.05
    eps_decay = 1000
    target_update_freq = 10

    steps_done = 0
    
    best_Q= float('-inf')  
    model_save_path = "best_model/best_model.pth"

    import csv

    log_path = f"csvs/sa_episode_rewards_{num_episodes}_{a}_{job_small_chance}.csv"
    # Open the file and write the header once
    with open(log_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Episode", "TotalReward"])


    log_path2 = f"csvs/loss_q_values_per_episode_{num_episodes}_{a}_{job_small_chance}.csv"
    # Open the file and write the header once
    with open(log_path2, mode="w", newline="") as f:
        writer_loss_q = csv.writer(f)
        writer_loss_q.writerow(["Episode", "Loss", "Average Q"])
    
    recent_rewards = []

    import time

    for episode in range(num_episodes):
        #time.sleep(180) # for the threads to finish from the previous episose
        obs_dict = env.reset()
        delete_local_files()
        state = obs_dict[agent_id].flatten()
        total_reward = 0
        #init_gnb("gnb")

        for t in range(20):  # max steps per episode. 13 is my max value. Change this
                                # if you run the loop and done flag has not become True.

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
            buffer.push(state, action, reward, next_state, done)

            state = next_state
            total_reward += reward
            steps_done += 1
            episode_q_values = []

            # Learn using buffer. 
            if len(buffer) >= batch_size:
                
                transitions = buffer.sample(batch_size)
                batch = Transition(*zip(*transitions))

                state_batch = torch.tensor(np.array(batch.state), dtype=torch.float32).to(device)
                action_batch = torch.tensor(batch.action).unsqueeze(1).to(device)
                reward_batch = torch.tensor(batch.reward, dtype=torch.float32).to(device)
                next_batch = torch.tensor(np.array(batch.next_state), dtype=torch.float32).to(device)
                done_batch = torch.tensor(batch.done, dtype=torch.float32).to(device)
               
                q_values = policy_net(state_batch).gather(1, action_batch)
                q_values = torch.clamp(q_values, min=-10, max=10)
                next_q = target_net(next_batch).max(1)[0].detach()
                expected_q = reward_batch + gamma * next_q * (1 - done_batch)


                episode_q_values.append(q_values.mean().item())
              
                
               
                #loss = F.mse_loss(q_values.squeeze(), expected_q)
                loss  = F.smooth_l1_loss(q_values.squeeze(), expected_q)

                optimizer.zero_grad()
                loss.backward()
                #to refine
                torch.nn.utils.clip_grad_norm_(policy_net.parameters(), 10.0) # noooooosrgfdgfdgfd
                optimizer.step()
                #print(f"Reward: {reward}, Q-values: {q_values.cpu().detach().numpy()}")
                #print(f"[INFO] Loss: {loss.item():.4f}, Avg Q: {q_values.mean().item():.2f}")
                if (episode>=4):
                        with open(log_path2, mode="a", newline="") as f:
                            writer_loss_q = csv.writer(f)
                            writer_loss_q.writerow([episode, loss.item(), q_values.mean().item()])
    
            if done:
                break
            # end of the for loop 
                
        # logging episode total reward
        with open(log_path, mode="a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([episode, total_reward])


        avg_q=np.mean(episode_q_values)
        #smoothed_q = 0.9 * smoothed_q + 0.1 * avg_q
        
        if  avg_q> best_Q:
                torch.save(policy_net.state_dict(), model_save_path)
                best_Q=avg_q
                policy_net.load_state_dict(torch.load("best_model/best_model.pth"))
                policy_net.eval()
                print(f"[INFO] 🔥 New best model found at episode {episode} with Avg Q {avg_q:.2f}")



        # recent_rewards.append(total_reward)
        # if len(recent_rewards) % 10 ==0 :
        #     avg_reward = np.mean(recent_rewards[-5:])
        #     if avg_reward > best_reward:
        #         torch.save(policy_net.state_dict(), model_save_path)
        #         print(f"[INFO] New best model saved at episode {episode} using the AVERAGE of LAST 10 rewards {avg_reward}")
        #         best_reward=avg_reward
        #         policy_net.load_state_dict(torch.load("best_model/best_model.pth"))
        #         policy_net.eval()


        #print(f"Episode {episode}, total_reward = {total_reward:.3f}")



