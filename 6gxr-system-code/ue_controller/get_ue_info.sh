#/bin/bash

UPF=$1
UE=$2
pid_file="$UPF-$UE.pid"
echo $pid_file
echo $UPF > $pid_file
echo "UE $UE starting"
tmp_file="$UPF-$UE.pid.temp"
(/home/leon/ueransim/build/nr-ue -c  "/home/leon/ueransim/config/cumucore-ue$UE-$UPF.yaml" > "$tmp_file") &
sleep 3
line=$(tail -n 1 "$tmp_file") 
#echo "tail -n 1 "$tmp_file" | awk '{sub(/^\[[^]]+\] /, ""); match($line, /TUN interface\[([^,]+), ([^]]+)\]/, a); print a[1], a[2]}'" 
echo "Printing the last line of the temp file"
echo $line
echo $line | awk '{print $13 $14}' >> $pid_file
echo "UE $UE started at $UPF "

