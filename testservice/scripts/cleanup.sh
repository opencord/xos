#!/bin/bash

TOSCA_URL=http://`hostname`:30007
RECIPE=../tosca/test_no_constraints.yaml
curl -H "xos-username: admin@opencord.org" -H "xos-password: letmein" -X POST --data-binary @$RECIPE $TOSCA_URL/delete
