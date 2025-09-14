import json
import paramiko
import requests
import time
import sys
import os
import subprocess

hostname = None #IP of UERANSIM
port = 22  # Default SSH port
sudo_password= None 
hostnameUPF250 = None #IP of UPF250
hostnameUPF500 = None #IP of UPF500
portUPF = 22  # Default SSH port
username= None

def get_bw(device):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    print ('inside the UERANSIM vm to get the bw of :', device)
    args= device 
    command = f'/home/leon/6gxr_system/scripts/wget/wget_report.sh {args}' 
    stdin, stdout, stderr = ssh.exec_command(command) 
    result_bw = stdout.read().decode()
    print('bw  ', result_bw)
    ssh.close()
   
def get_rtt(q, device):
    print ('get_rtt arg received is ', device)
    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    # Connect to SSH server
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    print ('inside UERASIM to get rtt of device ', device)
    command = f'/home/leon/6gxr_system/scripts/rtt/average_ping.sh {device}'
    stdin, stdout, stderr = ssh.exec_command(command)  # Retrieving the rtt of the UE
    # Print command output
    result_rtt = stdout.read().decode()
    print('rtt of device ', device , 'is ', result_rtt)
    ssh.close()
    q.put(result_rtt)

def get_UPF_usage(q, UPF):
    global result_cpu_ram
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    # Connect to SSH server
    if (UPF=="upf250"):
        hostname = hostnameUPF250
    elif (UPF=="upf500"):
         hostname = hostnameUPF500
    else:
        print ("Error: Unkwown UPF")

    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    
    print ('inside UPF ', UPF)
    #Run the script computing_resources.sh
    stdin, stdout, stderr = ssh.exec_command("./computing_resources.sh")  # Retrieving the CPU and RAM of the UPF
    #Print command output
    result_cpu_ram = stdout.read().decode()
    print('cpu_ram results ', result_cpu_ram)
    #print('error', stderr.read().decode())
    ssh.close()
    q.put(result_cpu_ram)


def get_networks_stats(q, device):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    print ('inside the UERANSIM vm to get the bw of :', device)
    args= device 
    command = f'/home/leon/6gxr_system/scripts/wget/wget_report.sh {args}' 
    stdin, stdout, stderr = ssh.exec_command(command) 
    result_bw = stdout.read().decode()
    print('bw  ', result_bw)
    ssh.close()
    q.put(result_bw)

def start_WGET_and_get_BW(device):
    global result_bw
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    print ('inside the UERANSIM vm to get the bw of :', device)
    args= device 
    command = f'/home/leon/6gxr_system/scripts/wget/wget.sh {args}' 
    stdin, stdout, stderr = ssh.exec_command(command) 
    # Wait until output is ready
    while not stdout.channel.recv_ready():
        time.sleep(0.1)

    # Read first line
    first_line = stdout.readline()
    print("First output line:", first_line.strip())
    
    #result_bw = stdout.read().decode()
    print('bw  ', first_line)
    ssh.close()
    return first_line

def start_WGET(device):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    #print ('inside the UERANSIM to start continous wget for :', device)
    args= device 
    command = f'nohup /home/leon/6gxr_system/scripts/wget/wget_start.sh {args} > /dev/null 2>&1 &' 
    stdin, stdout, stderr = ssh.exec_command(command) 
    ssh.close()


def start_WGET_speficic_time(imsi, device, time_required):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    print ('inside the UERANSIM to start continous wget for :', device)
    args= str(imsi) + ' ' + str(device) + ' ' + str(time_required)
    command = f'/home/leon/6gxr_system/scripts/wget/wget_start_with_timer.sh {args}' 
    stdin, stdout, stderr = ssh.exec_command(command) 
    # here I will get my BW inside the wget!!!!!

    # Wait until command finishes
    exit_status = stdout.channel.recv_exit_status()

    # Then read output
    stdout_output = stdout.read().decode()
    stderr_output = stderr.read().decode()

    print("Exit status:", exit_status)
    print("STDOUT:", stdout_output)
    # print("STDERR:", stderr_output)
    return stdout_output
    
def start_UE(imsi_to_start, upf):

    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    # Connect to SSH server
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    
    # Use get_pty=True to allow sudo to prompt
    
    args= str(imsi_to_start) + ' ' + str(upf)   
    command =  f'sudo -S /home/leon/6gxr_system/ue_controller/start_ue_with_imsi_and_slice_new.sh {args} \n' # -S tells sudo to read password from stdin
    #print ('In start_UE: the command to issue is ', command)
        
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)

    # Send the sudo password
    stdin.write(sudo_password + '\n')
    stdin.flush()

    # Read output
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    ssh.close
    

def stop_UE(imsi_to_stop):
    print ("in stop_UE for detaching it")
    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    # Connect to SSH server
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    command =  f'sudo -S /home/leon/6gxr_system/ue_controller/stop_ue.sh {imsi_to_stop} \n' # -S tells sudo to read password from stdin
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)

    # Send the sudo password
    stdin.write(sudo_password + '\n')
    stdin.flush()

    # Read output
    output = stdout.read().decode()
    error = stderr.read().decode()

    print("Output:\n", output)
    print("Errors:\n", error)
    ssh.close

def deregister_UE(imsi_to_deregister):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    print ('inside the UERANSIM vm to deregister :', imsi_to_deregister)
    command =  f'/home/leon/6gxr_system/ue_controller/deregister_ue.sh {imsi_to_deregister} \n' # -S tells sudo to read password from stdin
    stdin, stdout, stderr = ssh.exec_command(command) 
    output = stdout.read().decode()
    error = stderr.read().decode()
    print("Output:\n", output)
    print("Errors:\n", error)
    ssh.close

def init_gnb(program_name):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
        ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
        print ('inside the UERANSIM vm to reset my gnodeB')
        command = f'sudo -S supervisorctl restart {program_name} \n'
        print(f"🔁 Restarting Supervisor program: {program_name}")
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)

        # Send the sudo password
        stdin.write(sudo_password + '\n')
        stdin.flush()

        # Read output
        output = stdout.read().decode()
        error = stderr.read().decode()

        # print("Output:\n", output)
        # print("Errors:\n", error)
        ssh.close

    except Exception as e:
        print(f"Exception occurred: {e}")


def switch_slice(imsi, new_group):
    #todo: Delete with curl the imsi from its existing slice
    # the next command if for assigning to the new slice
    # sh ./local_scripts/assign_ue_to_upf.sh 999991000000081 group1

    command =  "./local_scripts/assign_ue_to_upf.sh"
    result = subprocess.run([command, str(imsi), new_group], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #print(result.stdout)

def init_UE(imsi, upf):
    args= str(imsi) 
    if (upf=="upf500"):
        result = subprocess.run(["./local_scripts/init_ue_to_upf500.sh", args], capture_output=True, text=True)
    if (upf=="upf250"):
        result = subprocess.run(["./local_scripts/init_ue_to_upf250.sh", args], capture_output=True, text=True)
        
    print(result.stdout)


def system_init():

    #delete local pid folder
    folder_path = './pid'

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
         os.remove(file_path)

    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    # Connect to SSH server
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    
    # Use get_pty=True to allow sudo to prompt
      
    command =  f'sudo -S /home/leon/6gxr_system/ue_controller/stop_all_ues.sh \n' # -S tells sudo to read password from stdin
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)

    # Send the sudo password
    stdin.write(sudo_password + '\n')
    stdin.flush()

    # Read output
    output = stdout.read().decode()
    error = stderr.read().decode()

    #print("Output:\n", output)
    # print("Errors:\n", error)
    ssh.close


remote_folder = '/home/leon/6gxr_system/ue_controller/state/'
local_folder = './ueransim_state'

def get_ueransim_state():

    # Create SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
    # Connect to SSH server
    ssh.connect(hostname, port, username, key_filename='/home/leonidas/.ssh/id_ed25519')
    #print ('inside UERANIM')
    # Open SFTP session
    sftp = ssh.open_sftp()

    # Ensure local folder exists
    os.makedirs(local_folder, exist_ok=True)

    # List and download files
    for filename in sftp.listdir(remote_folder):
        remote_path = f"{remote_folder}/{filename}"
        local_path = os.path.join(local_folder, filename)
        #print(f"Downloading {remote_path} → {local_path}")
        sftp.get(remote_path, local_path)

    # Close connections
    sftp.close()
    ssh.close()


def get_current_ueransim_state():
    devices=[]
    ips=[]
    

    #Device: uesimtun0 | IP: 172.29.7.217
    # Iterate over all files in the folder
    for filename in os.listdir(local_folder):
        file_path = os.path.join(local_folder, filename)

        # Ensure it's a file (not a subdirectory)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                for line in lines:
                    parts = line.split('|')
                    device = parts[0].split(':')[1].strip()
                    ip = parts[1].split(':')[1].strip()
                    devices.append(device)
                    ips.append(ip)
                    # print("Device:", device)
                    # print("IP:", ip)

    return devices, ips


def delete_local_files():


    folder_path = local_folder

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

