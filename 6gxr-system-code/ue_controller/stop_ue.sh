#!/bin/bash

set +x
imsi="imsi-$1"

echo "deregistering UE with IMSI $imsi"
/home/leon/ueransim/build/nr-cli $imsi --exec 'deregister switch-off'        


