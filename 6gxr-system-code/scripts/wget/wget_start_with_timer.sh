#/bin/bash

imsi=$1
device=$2
time=$3
minute="s"

IP=$(ip -4 addr show $device | grep inet | awk '{print $2}' | cut -d/ -f1)

start_time=$(date +%s)
timeout $time$minute wget --bind-address=$IP http://172.29.3.15:8080/5GB.zip -q # quit mode 
#timeout $time$minute wget --bind-address=$IP http://172.29.3.15:8080/5GB.zip > /dev/null 2>&1 
end_time=$(date +%s)
time_taken=$((end_time-start_time))

echo $imsi

rm "./5GB.zip"
rm "./wget-log" > /dev/null
rm "./wget-log.*" > /dev/null
tmp_file="/home/leon/6gxr_system/scripts/wget/pid/$imsi.pid"
echo $time_taken > $tmp_file
