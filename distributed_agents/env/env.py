import numpy as np
import pandas as pd
import sys
from utils import *
from concurrent.futures import ProcessPoolExecutor
from job_distribution import UE_Distribution
from datetime import datetime, timezone, timedelta
from imsi_pool import IMSI_POOL
from pettingzoo import AECEnv
from gymnasium import spaces
import sys
import traceback
import threading


ENDPOINT = "http://localhost:8000/collect"


# log_path = "csvs/times.csv"
# # Open the file and write the header once
# with open(log_path, mode="w", newline="") as f:
#     writer_times = csv.writer(f)
#     writer_times.writerow(["time", "IMSI", "bw requested", "real bandwith received", "slice"])

class UEAdmissionEnv(AECEnv):

    metadata = {"render_modes": ["human"], "name": "ue_scheduling_shared_v1"}


    def __init__(self, timestamp1, ue_bw1, ue_len1, \
                 timestamp2, ue_bw2, ue_len2,
                 timestamp3, ue_bw3, ue_len3, \
                 timestamp4, ue_bw4, ue_len4, \
                 timestamp5, ue_bw5, ue_len5,
                 timestamp6, ue_bw6, ue_len6, \
                 bw1_left, bw2_left, max_job_len, job_small_chance, \
                 bw_min, bw_max, a, max_steps=30, render_mode="human"):

        super().__init__()
        
        self.max_job_len = max_job_len
        self.max_job_chance = job_small_chance
        self.bw_min=bw_min
        self.bw_max=bw_max
        self.a = float(a)
        self.writter=None 
        self.log_path=None
        self.active_UEs=[]
        self.queue_size = 3
        self.render_mode = render_mode
        self.agents = ["UPF500", "UPF250"]
        self.possible_agents = self.agents[:]
        self.agent_order = self.agents[:]
        self.max_steps = max_steps
        self.current_step = 0
        self.bw = {"UPF500": 15, "UPF250": 15}
        self.imsi_pool = IMSI_POOL()
        self.t0=timestamp1
        self.real_bw_received=0

        imsi_init = 999991000000081
        self.agent_imsis = {}
        self.agent_really_used_imsis = {}
        # for imsis
        for agent in self.agents:
            if (agent=="UPF500"):
                 self.agent_imsis[agent]=np.array([imsi_init, imsi_init+1, \
                                                   imsi_init+2],dtype=np.int64)
                 
            if (agent=="UPF250"):
                 self.agent_imsis[agent]=np.array([imsi_init+3, imsi_init+4, \
                                                   imsi_init+5],dtype=np.int64)
        
        self.agent_features = {}
        for agent in self.agents:
            if (agent=="UPF500"):
                 self.agent_features[agent]=np.array([timestamp1, ue_bw1, ue_len1, \
                 timestamp2, ue_bw2, ue_len2,
                 timestamp3, ue_bw3, ue_len3, bw1_left], dtype=np.float32)
                 
            if (agent=="UPF250"):
                 self.agent_features[agent]=np.array([timestamp4, ue_bw4, ue_len4, \
                 timestamp5, ue_bw5, ue_len5,
                 timestamp6, ue_bw6, ue_len6, bw2_left], dtype=np.float32)
       

        
        self.observation_spaces = {
            agent: spaces.Box(low=0.0, high=300.0, shape=(10,), dtype=np.float32)
            for agent in self.agents
        }
        
        self.action_spaces = {
            agent: spaces.Discrete(self.queue_size)
            for agent in self.agents
        }

    def reset(self, seed=None, options=None):
        self.queue_size = 3
        self.render_mode = "human"
        self.agents = ["UPF500", "UPF250"]
        self.possible_agents = self.agents[:]
        self.agent_order = self.agents[:]
        self.max_steps = 20
        self.current_step = 0
        self.agents = ["UPF500", "UPF250"]
        self.agent_selection = self.agent_order[0]
        self.rewards = {a: 0.0 for a in self.agents}
        self.terminations = {a: False for a in self.agents}
        self.truncations = {a: False for a in self.agents}
        self.infos = {a: {} for a in self.agents}
        self.current_step = 0
        self.bw = {"UPF500": 15, "UPF250": 15}
        self.imsi_pool = IMSI_POOL()
        self.used_imsis = []
        self.real_bw_received=0
        max_job_len = self.max_job_len
        job_small_chance = self.max_job_chance
        a=self.a
        bw_min = self.bw_min
        bw_max=self.bw_max
        q_size=3
       
        
        #print ("*********************** RESET IS CALLED ********************")

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
        self.t0 = timestamp

        timestamp1=timestamp - self.t0
        timestamp2=timestamp - self.t0
        timestamp3=timestamp - self.t0
        timestamp4=timestamp - self.t0
        timestamp5=timestamp - self.t0
        timestamp6=timestamp - self.t0

        # o xronos ksekinaewi apo 0 omws exw kratisei to self.t0
        system_init() #each episode starts with a clean system   

        import csv
        self.log_path = f"csvs/bandwidth_real_info__{a}_{job_small_chance}.csv"
         # Open the file and write the header once   
        with open(self.log_path, mode="w", newline="") as f:
            self.writer = csv.writer(f)
            self.writer.writerow(["time", "IMSI", "bw requested", "real bandwith received", "slice"])

        
        self.agent_features = {}
        for agent in self.agents:
            if (agent=="UPF500"):
                 self.agent_features[agent]=np.array([timestamp1, ue_bw1, ue_len1, \
                 timestamp2, ue_bw2, ue_len2,
                 timestamp3, ue_bw3, ue_len3, bw1_left], dtype=np.float32)
                 
            if (agent=="UPF250"):
                 self.agent_features[agent]=np.array([timestamp4, ue_bw4, ue_len4, \
                 timestamp5, ue_bw5, ue_len5,
                 timestamp6, ue_bw6, ue_len6, bw2_left], dtype=np.float32)

        
                        
        self._cumulative_rewards = {a: 0.0 for a in self.agents}
        result = self._observe()
        if result is None:
            print("[ERROR] Reset returned None. Check _observe and observe methods.")
        return result
    
   
    
    def _observe(self):
        result = {a: self.observe(a) for a in self.agents}
        #print("[DEBUG] Observation result:", result)
        return result
    
    def observe(self, agent):
        if agent not in self.agent_features:
            print(f"[ERROR] Agent '{agent}' not in self.agent_features: {list(self.agent_features.keys())}")
            return None
        
        # all my observations must be normalized
        try:
            obs = self.agent_features[agent]  # shape (10,)
            #  self.agent_features[agent]=np.array([timestamp1, ue_bw1, ue_len1, \
            #      timestamp2, ue_bw2, ue_len2,
            #      timestamp3, ue_bw3, ue_len3, bw1_left], dtype=np.int64)


            return obs
        except Exception as e:
            print(f"[ERROR] Failed to build observation for {agent}: {e}")
        return None

    def get_active_UEs(self):
        return self.active_UEs
    
   
    def get_pair(self, x, y, z, w):
        return [x, y, z, w ]


    def run_wget_thread(self, hostname, username, password, agent, imsi, device, action, time_needed, bw_needed, callback):
        def worker():
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=hostname, username=username, password=password)
                args= str(imsi) + ' ' + str(device) + ' ' + str(time_needed)
                command = f'/home/leon/6gxr_system/scripts/wget/wget_start_and_measure.sh {args}'
                
                stdin, stdout, stderr = client.exec_command(command)
                stdout.channel.recv_exit_status()  # Waits for command to finish

                result = stdout.read().decode() # here I get real_bw
                error = stderr.read().decode()
                
                output=self.get_pair(agent, imsi, bw_needed, result)
                client.close()

                # Call the callback function when done
                callback(output, error)
            
            except Exception as e:
                print ('Exception happened in run wget', e)

                print ('action was ', action)
                traceback.print_exc() 
                #raise ValueError("Stopping episode because of exception in wget worker")
                raise RuntimeError("Stopping episode because of exception in wget worker")
                callback(None, str(e))
                
        thread = threading.Thread(target=worker)
        thread.start()
    
    
    def notify_when_done(self, output, error):
        print("[INFO] wget is finished.")

        agent=output[0]
        imsi=output[1]
        bw_needed=output[2]
        real_bw_received=output[3]

        if agent=='UPF500':
            self.agent_features["UPF500"][9] += bw_needed

        if agent=='UPF250':
            self.agent_features["UPF250"][9] += bw_needed

        from datetime import datetime, timezone

        utc_now = datetime.now(timezone.utc)            

        real_bw_received = real_bw_received.rstrip('\n')
        real_bw_received = real_bw_received.replace('"','')
        
        import csv
         # logging 
        with open(self.log_path, mode="a", newline="") as f:
                     self.writer = csv.writer(f)
                     self.writer.writerow([utc_now, imsi, bw_needed, real_bw_received, agent])
    # state shape (20,)
    def step(self, action):
        device_index=0
        
        done = False
        reward = 0 # must be a global var for this function
        device =""
        
        agent = self.agent_selection
        
        self.observe(agent) # so I have the current state after modifications

        # print ('***************** I am agent', agent, 'and I am in STEP', \
        #        self.current_step, ' and action is ', action)
        
        
        if action is None: # lets see when the phenomenon happens
            # if self.render_mode == "human":
            #     self.render()
            # raise ValueError("Action cannot be None for agent: {}".format(agent))
            #print ('NONE ACTION - ALARM')
            self.terminations[agent] = False
            self.truncations[agent] = False  # if desired
            reward = 0
            #raise ValueError("Stopping episode because of XYZ condition")
            raise RuntimeError("Terminating training because of None action")
            #return None, 0.0, self.terminations[agent], self.truncations[agent], {}

        elif 0 <= action <self.queue_size: # only these actions are permitted 
            #print ('In permitted action space')
            #print (self.agent_features[agent])
            # bw must be reduced since I have chosen this action
            #self.bw[agent] = self.bw[agent] - self.agent_features[agent][action][2]
            #print ('remaining bw after this action is ', self.bw)

            # STARTING THE UE AT REAL TIME and observing the system
            waiting_time=0
            time_needed=0
            bw_needed=0
            imsi = -1 

            # print ('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            # print (self.agent_features[agent][0])
            # print (self.agent_features[agent][3])
            # print (self.agent_features[agent][6])
            # print ('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            
            if (action==0):
                time_needed = self.agent_features[agent][2]
                bw_needed = self.agent_features[agent][1]
                waiting_time = self.agent_features[agent][0] 
                imsi = self.agent_imsis[agent][2] 
            if (action==1):
                time_needed = self.agent_features[agent][5]
                bw_needed = self.agent_features[agent][4]
                waiting_time = self.agent_features[agent][3] 
                imsi = self.agent_imsis[agent][1]
            if (action==2):
                time_needed = self.agent_features[agent][8]
                bw_needed = self.agent_features[agent][7]
                waiting_time = self.agent_features[agent][6]
                imsi = self.agent_imsis[agent][2] 

            # print ('Chosen imsi is based on action is ', imsi)
            # self.used_imsis.append(imsi)

            # print ('Printing all used IMSIs')
            # for imsi in self.used_imsis:
            #     print(imsi)
            
            ########################## immediate replacement -start###################
            max_job_len = self.max_job_len # seconds
            job_small_chance = self.max_job_chance
            bw_min = self.bw_min
            bw_max= self.bw_max
            
            distribution=UE_Distribution(max_job_len, job_small_chance, bw_min, bw_max)
            ue_len, ue_bw = distribution.binomial_model()
            
            current_time = datetime.now()
            timestamp = int(current_time.timestamp())

            delta = timestamp - self.t0
            #    print ('**************I replaced UE ', action, 'with timestamp ', delta)
            replacement_imsi=self.imsi_pool.get_imsi()       
            

            # now I am replacing the line with a new line
            if (action==0):
                self.agent_features[agent][2]=ue_len
                self.agent_features[agent][1]=ue_bw
                self.agent_features[agent][0]=delta
                self.agent_imsis[agent][0]=replacement_imsi
            if (action==1):
                self.agent_features[agent][5]=ue_len
                self.agent_features[agent][4]=ue_bw
                self.agent_features[agent][3]=delta
                self.agent_imsis[agent][1]=replacement_imsi
            if (action==2):
                self.agent_features[agent][8]=ue_len
                self.agent_features[agent][7]=ue_bw
                self.agent_features[agent][6]=delta
                self.agent_imsis[agent][2]=replacement_imsi  
            ########################## immediate replacement - end ###################

            admission=True

            if agent=='UPF500' and bw_needed <= self.agent_features["UPF500"][9]:
               
                self.agent_features["UPF500"][9]=self.agent_features["UPF500"][9]-bw_needed
                bw1_left=self.agent_features["UPF500"][9]  
                #print ('bw1 left is ', bw1_left)              
                # init_UE (imsi, "upf500")
                # start_UE(imsi, "upf500") 
                               
            elif agent=='UPF500' and bw_needed > self.agent_features["UPF500"][9]:
                # print ('I wont allow this to happen because \
                #        neeed = ', bw_needed , 'and offer is ', \
                #         self.agent_features["UPF500"][9], \
                #         'Therefore, I do not admit the device')
                  admission = False
                
            elif agent=="UPF250" and bw_needed<=self.agent_features["UPF250"][9]:
                self.agent_features["UPF250"][9] = self.agent_features["UPF250"][9] - bw_needed
                bw2_left=self.agent_features["UPF250"][9] 
                #print ('bw2 left is ', bw2_left)
                # init_UE (imsi, "upf250")
                # start_UE(imsi, "upf250") 
            
            elif agent=='UPF250' and bw_needed > self.agent_features["UPF250"][9]:
                # print ('I wont allow this to happen because \
                #        neeed = ', bw_needed , 'and offer is ', \
                #         self.agent_features["UPF250"][9], \
                #         'Therefore, I do not admit the device')
                 admission = False
            
            if (admission):
                # devices=[]
                # ips=[]
                # get_ueransim_state()
                # devices, ips = get_current_ueransim_state()      
                # device = devices[-1]

                # if (device==''):
                #     raise RuntimeError(" Terminating because UERANSIM failed to give me a valid device")
                
                # print('[INFO] I try to start WGET for device ', device)

                # try:
                #     # print ('before starting the thread')
                #         self.run_wget_thread(hostname=hostname, username=username, device=device,\
                #         password=password, imsi=imsi, agent=agent, action=action, bw_needed=bw_needed,
                #         time_needed=time_needed, callback=self.notify_when_done)
                # except Exception as e:
                #         print("Error in run_wget_command:", e)

                # print('[INFO] WGET started sucessfully for device ', device)
        
                
                a=self.a 
                b=1-self.a

                reward = 1.0/  (a*(time_needed/100.0) + b*(waiting_time/100.0) + 1e-5)
                #reward = 1.0 / (  a*(time_needed) + b*(waiting_time))
                if (waiting_time>100.0):
                    print ("BAM ! waiting time more than 100!")
                
                reward = min(reward, 100.0)

                # print ('!!!time needed ', time_needed, 'waiting time ', waiting_time, \
                #          ' reward ', reward)            
        
                #print ('reward received is ', reward)    
                #giving back my bw
                #self.bw[agent]= self.bw[agent]+  self.agent_features[agent][action][2]      
            
            
                self.rewards[agent] = reward
                self._cumulative_rewards[agent] += reward
                self.current_step = self.current_step + 1 

            # in final steps, definetely I will need to get from the pool.
            # i want to print the fact that the episode has ended.
            if  self.imsi_pool.get_pool_info()==0:
                done=True
                self.terminations[agent] = done
                self.truncations[agent] = False
                self.agent_selection = self._next_agent(agent)
      
            self.terminations[agent] = done
            self.truncations[agent] = False
            self.agent_selection = self._next_agent(agent)

            payload = {
            "IMSI_UE1": str(self.agent_imsis[agent][0]),
            "waiting_time_UE1" :  int(self.agent_features[agent][0]),
            "time_requested_UE1":int(self.agent_features[agent][2]),
            "IMSI_UE2": str(self.agent_imsis[agent][1]),
            "waiting_time_UE2" :  int(self.agent_features[agent][3]),
            "time_requested_UE2":int(self.agent_features[agent][5]),
            "IMSI_UE3": str(self.agent_imsis[agent][2]),
            "waiting_time_UE3" :  int(self.agent_features[agent][6]),
            "time_requested_UE3":int(self.agent_features[agent][8]),
            "episode_done":done,  
            "action":action,
            "reward": float(reward)
                        }
            # print("just before posting to metrics collector", payload)
            # #  saving the metrics to my db
            # requests.post(ENDPOINT, json=payload)
        
            # if self.render_mode == "human":
            #     self.render(agent)
              
            #print ('my done flag is ', done)
            # print ('my self termination flag is ', self.terminations[agent])
            # # debug 
            #print (self._observe(),  self.rewards[agent] , self.terminations[agent], self.truncations[agent])
            return None,  reward , self.terminations[agent], self.truncations[agent], {} 
        

    def _next_agent(self, current):
        idx = self.agent_order.index(current)
        return self.agent_order[(idx + 1) % len(self.agent_order)]

    def render(self, agent):
        print('Remaining bw of agent ', agent, ' is ', self.agent_features[agent][9])
        # for a in self.agents:
        #     print(f"{a} queues: {self.agent_features[a]}")
