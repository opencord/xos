# seed initial data in the db
python /opt/xos/manage.py makemigrations;
python /opt/xos/manage.py migrate;
python /opt/xos/manage.py makemigrations core;
python /opt/xos/manage.py migrate core;

# build protobuf
cd protos
make rebuild-protos
make

# start the grpc server
cd ..
source env.sh
python ./core_main.py
