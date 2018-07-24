#!/bin/bash

set -e

CHAMELEON_URL=http://`hostname`:30006/xosapi/v1/testservice/testserviceserviceinstances
TOSCA_URL=http://`hostname`:30007
TEST_POD=`kubectl get pods | grep -i testservice | cut -f 1 -d " "`
RECIPE=../tosca/test_no_constraints.yaml

curl -H "xos-username: admin@opencord.org" -H "xos-password: letmein" -X post --data-binary @$RECIPE $TOSCA_URL/run

echo "done tosca"

cat <<EOF > wait_for.txt
TEST:SYNC_DONE                 id=[0-9]+ model_class=TestserviceServiceInstance model_name=u'test-no-constraints' some_integer=0 some_other_integer=0
TEST:POLICY_DONE               id=[0-9]+ model_class=TestserviceServiceInstance model_name=u'test-no-constraints' some_integer=0 some_other_integer=0
EOF
kubectl logs -f --since=30s $TEST_POD | ansi2txt | python wait_for_lines.py wait_for.txt

python ./verify_model.py $CHAMELEON_URL name=test-no-constraints "updated>=0" "enacted>=@updated" "policed>=@updated"
