Quick Start Notes:

1) cd protos; make install-protoc; make rebuild-protos; make

2) apt-get -y install cython

3) python -m pip install grpcio grpcio-tools

4) source env.sh

5) python ./grpc_server.py

Note: If you don't run env.sh before running grpc_server.sh, things break.
