#!/bin/bash

source ./config.sh

ACCOUNT_NUM=1238

DATA=$(cat <<EOF
{"identity": {"account_num": "$ACCOUNT_NUM", "name": "test-subscriber"},
 "features": {"cdn": false,
              "uplink_speed": 2000000000,
              "downlink_speed": 2000000000,
              "uverse": true,
              "status": "enabled"}}
EOF
)

curl -H "Accept: application/json; indent=4" -H "Content-Type: application/json" -u $AUTH -X POST -d "$DATA" $HOST/api/tenant/cord/subscriber/   
