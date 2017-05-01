# xos_client #

Xos_client is a python library that is used for synchronizers. It includes a self-learning grpc client (based on Chameleon) as well as a client-side ORM layer. Xos_client is intended to be installed into a container.

## XOSSH ##

XOSSH is a shell for interactively using the xos client API and client ORM layer. A script is provided in xos/tools to assist in invoking xossh. 

## Running Unit Tests ##

Some unit tests (orm\_test.py) require an environment were the xos_client is installed and running. It's suggested that the xos-client container be used. For example,

    docker run --rm -it --entrypoint bash docker-registry:5000/xosproject/xos-client:candidate

Once inside of the container, run the test. For example,

    python ./usr/local/lib/python2.7/dist-packages/xosapi/orm_test.py

