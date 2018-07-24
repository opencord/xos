pushd ~/cord/orchestration/xos/testservice/helm-charts
helm dep update testservice
helm install -n testservice -f testservice_devel.yaml
popd
