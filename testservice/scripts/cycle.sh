#! /bin/bash

pushd ~/cord/orchestration/xos/testservice/scripts
helm del --purge testservice
./rebuild.sh
./deploy.sh
popd
