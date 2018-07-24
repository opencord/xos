cat <<EOF > wait_for.txt
TEST:SYNC_DONE                 id=[0-9]+ model_class=TestserviceServiceInstance model_name=u'test-no-constraints'
TEST:POLICY_DONE               id=[0-9]+ model_class=TestserviceServiceInstance model_name=u'test-no-constraints'
EOF
TEST_POD=`kubectl get pods | grep -i testservice | cut -f 1 -d " "`
echo "Pod is $TEST_POD"
kubectl logs -f $TEST_POD | ansi2txt | python wait_for_lines.py wait_for.txt
