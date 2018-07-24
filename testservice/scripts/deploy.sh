#! /bin/bash

pushd ~/cord/orchestration/xos/testservice/helm-charts
#helm dep update testservice
helm install testservice -n testservice -f testservice-devel.yaml
popd
