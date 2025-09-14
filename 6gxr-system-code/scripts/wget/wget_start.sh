#/bin/bash

device=$1

IP=$(ip -4 addr show $device | grep inet | awk '{print $2}' | cut -d/ -f1)

wget --bind-address=$IP http://172.29.3.15:8080/5GB.zip  # -q is for quiet mode

rm "./5GB.zip"
