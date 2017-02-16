all: chameleon_protos xosapi_install

chameleon_protos:
	cd xosapi/chameleon/protos; export VOLTHA_BASE=anything make

xosapi_install:
	python ./setup.py install
