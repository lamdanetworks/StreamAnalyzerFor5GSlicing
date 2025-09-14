#/bin/bash
device=$1

IFACE=$device

INTERVAL=10 

IP=$(ip -4 addr show $device | grep inet | awk '{print $2}' | cut -d/ -f1)

# Get initial bytes received and transmitted
RX1=$(cat /sys/class/net/$IFACE/statistics/rx_bytes)
TX1=$(cat /sys/class/net/$IFACE/statistics/tx_bytes)

sleep $INTERVAL

# Get bytes again after interval
RX2=$(cat /sys/class/net/$IFACE/statistics/rx_bytes)
TX2=$(cat /sys/class/net/$IFACE/statistics/tx_bytes)

# Calculate bytes per second
RX_BYTES=$(( ($RX2 - $RX1) / $INTERVAL ))
TX_BYTES=$(( ($TX2 - $TX1) / $INTERVAL ))

# Convert to megabytes per second (MBps)
RX_MBPS=$(echo "scale=2; $RX_BYTES / 1000000" | bc)
TX_MBPS=$(echo "scale=2; $TX_BYTES  / 1000000" | bc)

echo "$RX_MBPS"


