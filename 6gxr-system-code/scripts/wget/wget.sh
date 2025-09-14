#/bin/bash

device=$1

IP=$(ip -4 addr show $device | grep inet | awk '{print $2}' | cut -d/ -f1)

wget --bind-address=$IP http://172.29.3.15:8080/5GB.zip  2>&1 | \
while read -r line; do
    if [[ $line == 1000K* ]]; then
        echo "$line" | awk '{for (i=1; i<=NF; i++) if ($i ~ /^[0-9]+\.[0-9]+M$/) { gsub("M", "", $i); print $i; exit }}'
    fi
done

rm "./5GB.zip*"
 
