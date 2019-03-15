#! /bin/bash

pushd ~/cord/orchestration/xos/testservice
sudo docker build -t xosproject/testservice-synchronizer:candidate -f Dockerfile.synchronizer .
popd
