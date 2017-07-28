# seed initial data in the db
bash /opt/xos/tools/xos-manage makemigrations
python /opt/xos/manage.py migrate;

# build protobuf
cd protos
make rebuild-protos
make

# start the grpc server
cd ..
source env.sh
python ./core_main.py
