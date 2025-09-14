#!/bin/bash

set +x
cd /home/leon/6gxr_system/ue_controller
imsi=$1
upf=$2
tmp_file="pid/$imsi.pid"
(/home/leon/6gxr_system/ueransim/build/nr-ue -c  "/home/leon/6gxr_system/ueransim/config/cumucore-$imsi-$upf.yaml" > "$tmp_file") &
sleep 10
line=$(tail -n 1 "$tmp_file")
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

echo "$device:$ip"
