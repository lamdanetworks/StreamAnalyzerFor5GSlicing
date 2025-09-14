#!/bin/bash

set -x
index=100
for UPF in upf250 upf500; do
for UE in $(seq 1 2); do

pid_file="pid/$UPF-$UE.pid"
echo $pid_file
echo $UPF > $pid_file
echo "UE $UE starting"
tmp_file="pid/$UPF-$UE.pid.temp"
(/home/leon/ueransim/build/nr-ue -c  "/home/leon/ueransim/config/cumucore-ue$UE-$UPF.yaml" > "$tmp_file") &
sleep 10
line=$(tail -n 1 "$tmp_file")
echo "Printing the last line of the temp file"
echo $line
#removing the temp file
rm "$tmp_file"

string=$(echo $line | awk '{print $13 $14}')  
# Run awk, print desired values, and capture them into Bash variables
read device ip <<< $(echo "$string" | awk '
{
    if (match($0, /interface\[([^,]+),([^\]]+)\]/, m)) {
        print m[1], m[2]  # print interface and IP
    }
}')

echo "device: $device"
echo "IP Address: $ip"

echo $device >> $pid_file
echo $ip >> $pid_file



#Configuring the qdisc of the device 

tc qdisc add dev $device root tbf rate 10mbit burst 32kbit latency 400ms

#Configuring ip routes using tables

ip rule add from $ip table $index

ip route add $ip  dev uesimtun0 table $index

index=$((index + 1))


echo "UE $UE started at $UPF "
sleep 5
done
done
