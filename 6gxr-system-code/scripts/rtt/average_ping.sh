#!/bin/bash

device=$1

# Set the target host (default: google.com)
HOST="google.com"

COUNT="3"

#echo "Pinging $HOST $COUNT times..."

# Run the ping command and extract the average time. Using the uesimtun0 tunnel where my PDU session is established
AVG_TIME=$(ping -I $device -c "$COUNT" "$HOST" | awk -F'/' 'END{print $5}')

# Check if AVG_TIME is empty (meaning ping failed)
# Result is in milliseconds
if [[ -z "$AVG_TIME" ]]; then
    echo "Ping failed or no response from $HOST"
else
    echo "$AVG_TIME"
fi
