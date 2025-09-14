#!/usr/bin/env bash

random_number=$(( (RANDOM % 40) + 1 ))
UEs=$(( (RANDOM % 20) + 1 ))
if [[ $random_number -lt 10 ]]; then
    echo "Stopping $UEs"
    for i in $(seq 1 $UEs); do
        UE=$(printf "%02d" $i)
        echo "Stopping UE: $UE"
        sleep 3
        /home/kostas/task_executor/stop_ue.sh $UE
    done
else
    echo "Starting $UEs"
    for i in $(seq 1 $UEs); do
        UE=$(printf "%02d" $i)
        echo "Starting UE: $UE"
        sleep 3
        /home/kostas/task_executor/start_ue.sh $UE
    done
fi