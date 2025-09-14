#!/bin/bash

rm /home/leon/5GB*

for i in $(seq 0 9); do

UE=$(printf "%01d" $i)
imsi="imsi-99999100000008$i"
echo "deregistering UE with IMSI $imsi"
/home/leon/ueransim/build/nr-cli $imsi --exec 'deregister switch-off'        
#sleep 1
done


for i in $(seq 0 9); do

UE=$(printf "%01d" $i)
imsi="imsi-99999100000009$i"
echo "deregistering UE with IMSI $imsi"
/home/leon/ueransim/build/nr-cli $imsi --exec 'deregister switch-off'        
#sleep 1
done

for i in $(seq 0 20); do
sudo ip link delete dev uesimtun$i
done

sudo pkill -f /home/leon/ueransim/build/nr-ue

rm /home/leon/ue_controller/pid/*
