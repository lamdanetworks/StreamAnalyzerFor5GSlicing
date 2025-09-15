import json
import paramiko
import requests
import time
import sys
import os
from datetime import datetime, timezone, timedelta
from multiprocessing import Process, Queue
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import queue
from collections import deque 
from utils import * 
import numpy as np


def predict_admission(ue_features):
        # ue_features = [slice1_active_ues, slice2_active_ues]
        X = scaler.transform([ue_features])
        prob = model.predict(X)[0][0]
        return prob >= 0.5


ENDPOINT = "http://localhost:8000/collect"

hostname = None  #IP of UERANSIM
port = 22  # Default SSH port
username = None
password = None
sudo_password= None
hostnameUPF250 = None #IP of UPF250
hostnameUPF500 = None #IP of UPF500

portUPF = 22  # Default SSH port
usernameUPF = None
passwordUPF = None

result_rtt = 0
result_speed ="default"
result_cpu_ram ="default:default:default"
result_network_stats="default"
download_speed =""
upload_speed=""

count = 0

imsi = 999991000000081

remote_folder = '/home/leon/ue_controller/pid'
local_folder = './pid'

#global variables specific to the network environmen  this script is addressed to. They get values using
# 1. get_running_UEs (to get the info from UERANSIM) 2.get_UE_details (that parses the info received from UERANSIM)
all_UPFs =[]
all_devices=[]
all_interfaces=[]
all_imsis=[]
slice1_active_ues = []
slice2_active_ues = []
active_ues=[]


satisfied_ues = np.zeros(10)

startFlag=True


if __name__ == "__main__":

    system_init() #each test starts with a clean system cleaning any junk files in UERANSIM VM    
   
    for ue in range (10): 

        total_bw=0    
        
        current_imsi = imsi + ue
        print ('This loop handles the UE with id' , ue, ' and IMSI ', current_imsi)  


        ######## AI-based admission logic ##################################

        import tensorflow as tf
        import joblib
        import numpy as np

        # Load model and scaler
        model = tf.keras.models.load_model("ue_admission_model.h5")
        scaler = joblib.load("ue_admission_scaler.pkl")

        slice1_selected = False
        slice2_selected = False 

         #### AI-based admission logic with slice as feauture####################
               
        if (ue>0):
            # see what would happen if I tried slice 1     
            space_features = [len(active_ues)+1, len(slice1_active_ues)+1, len(slice2_active_ues), 1]
            if predict_admission(space_features) == 1:
                slice1_selected = True
                print('Could admit UE with IMSI, ', current_imsi, 'to slice 1')
            #see what would happen if I tred slice 2
            space_features = [len(active_ues)+1, len(slice1_active_ues), len(slice2_active_ues)+1, 2]
            if predict_admission(space_features) == 1:
                slice2_selected = True
                print('Could admit UE with IMSI, ', current_imsi, 'to slice 2')

               ###################################################
       
            
        if (slice1_selected and slice2_selected) or ue==0:
            print ('BOTH slides are selected-------------------------')
            if (ue%2==0): # ue=0 is treated with the startFlag
                    init_UE (current_imsi, "upf500")
                    device,ip=start_UE(current_imsi, "upf500") 
                    ip = ip.rstrip('\r')

                    start_WGET(device)
                
                    all_devices.append(device)
                    all_interfaces.append(ip)
                    all_UPFs.append("upf500")
                    all_imsis.append(current_imsi)
                    slice1_active_ues.append(current_imsi)
                    active_ues.append(current_imsi)
            elif (ue%2==1):
                    init_UE (current_imsi, "upf250")
                    device,ip=start_UE(current_imsi, "upf250") 
                    ip = ip.rstrip('\r')
                
                    start_WGET(device)
                            
                    all_devices.append(device)
                    all_interfaces.append(ip)
                    all_UPFs.append("upf250")
                    all_imsis.append(current_imsi)
                    slice2_active_ues.append(current_imsi)
                    active_ues.append(current_imsi)
                     
        elif (slice2_selected):
                print ('SLICE 2 selected---------------------------')
                init_UE (current_imsi, "upf250")
                device,ip=start_UE(current_imsi, "upf250") 
                ip = ip.rstrip('\r')
                
                start_WGET(device)
                            
                all_devices.append(device)
                all_interfaces.append(ip)
                all_UPFs.append("upf250")
                all_imsis.append(current_imsi)
                slice2_active_ues.append(current_imsi)
                active_ues.append(current_imsi)

        elif (slice1_selected==1):
                print ('SLICE 1 selected----------------------------')
                init_UE (current_imsi, "upf250")
                device,ip=start_UE(current_imsi, "upf250") 
                ip = ip.rstrip('\r')
                
                start_WGET(device)
                            
                all_devices.append(device)
                all_interfaces.append(ip)
                all_UPFs.append("upf250")
                all_imsis.append(current_imsi)
                slice2_active_ues.append(current_imsi)
                active_ues.append(current_imsi)

        print(all_UPFs)
        print(all_devices)
        print(all_interfaces)
        

        number_of_running_UEs=len(all_devices)
        
        q_rtt=[]
        q_bw=[]
        q_cpu_ram=[]


        
        try:
            #create the necessary queues
            q_rtt = [Queue() for _ in range(len(all_devices))]
            q_bw = [Queue() for _ in range(len(all_devices))]
            q_cpu_ram = [Queue() for _ in range(len(all_devices))]
                
            processes = []

            for i in range(len(all_devices)):
                device=all_devices[i]
                UPF=all_UPFs[i]
                print ("Measuring device ", device, 'attached to UPF ', UPF)
                p1 = Process(target=get_rtt, args=(q_rtt[i], device)) #Process needs args as a tuple!!!
                p2 = Process(target=get_networks_stats, args=(q_bw[i], device))
                p3 = Process(target=get_UPF_usage, args=(q_cpu_ram[i], UPF))
                
                p1.start()
                p2.start()
                p3.start()
                    
                processes.append(p1)
                processes.append(p2)
                processes.append(p3)
                
                for p in processes:
                    p.join()
                
        except Exception as e:
                print(f"Error: {e}")

        finally:
                print ("Measurement performed for all UEs")


        #Once measurements are gathered per device then filling in my db

        # Get current time
        current_time = datetime.now()

        # Get timestamp
        timestamp = int(current_time.timestamp())


            
            # system reporting
        bw=0
        for i in range(len(all_devices)):
            result_rtt = q_rtt[i].get()
            print ('---rtt---- ', str(result_rtt))
            result_bw = q_bw[i].get()
            bw = float(result_bw.rstrip('\n'))
            total_bw = total_bw + bw
            print ('---bw---- ', str(result_bw))
            result_cpu_ram = q_cpu_ram[i].get()
            print ('---cpu_ram---- ', str(result_cpu_ram))

            # labeling the admission flag in this for loop
            
            # labeling the admission flag in this for loop
        
            print ('bw received by this device is ', type(bw), bw)
            if bw>5.0:
                satisfied_ues[i]=1
                print ("+++++++++++++++++++++++++++++++++++++++++++++")
            else:
                satisfied_ues[i]=0    
                print ("---------------------------------------------")     
              
            
            payload = {
                        "imsi": all_imsis[i],
                        "device": all_devices[i],
                        "timestamp": timestamp,
                        "rtt": result_rtt.rstrip('\n'),
                        "upf": all_UPFs[i],
                        "cpu": result_cpu_ram.split('\n')[0],
                        "ram": result_cpu_ram.split('\n')[1],
                        "bw_requested": "5.0",
                        "bw_received": bw,                   
                        "slice1_active_ues": len(slice1_active_ues),
                        "slice2_active_ues": len(slice2_active_ues),
                        "active_ues": len(all_devices), 
                        "admission_flag": int(satisfied_ues[i])
                        }

            # end of if 
            print("just before posting to metrics aggregator", payload)
            # # saving the metrics to my db
            requests.post(ENDPOINT, json=payload)

        #end of for loop  
        print ('################################## total_bw:', total_bw)         
        time.sleep(20) # performing the next measurement in the next half min

    system_init() # so we avoid hd space problems