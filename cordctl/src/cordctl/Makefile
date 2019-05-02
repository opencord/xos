ifeq ($(GOPATH),)
GOPATH=$(shell pwd)
endif

help:

commands/voltha_v1_pb.go: protosets/voltha_v1.pb
	@echo "package commands" > $@
	@echo "" >> $@
	@echo "var V1Descriptor = []byte{" >> $@
	hexdump -ve '1/1 "0x%02x,"' protosets/voltha_v1.pb | fold -w 60 -s >> $@
	@echo "}" >> $@
	@go fmt $@

commands/voltha_v2_pb.go: protosets/voltha_v2.pb
	@echo "package commands" > $@
	@echo "" >> $@
	@echo "var V2Descriptor = []byte{" >> $@
	hexdump -ve '1/1 "0x%02x,"' protosets/voltha_v2.pb | fold -w 60 -s >> $@
	@echo "}" >> $@
	@go fmt $@

encode-protosets: commands/voltha_v1_pb.go commands/voltha_v2_pb.go

build:
	GOPATH=$(GOPATH) go install cordctl

lint:
	GOPATH=$(GOPATH) find $(GOPATH)/src/cordctl -name "*.go" -not -path '$(GOPATH)/src/cordctl/vendor/*' | xargs gofmt -l
	GOPATH=$(GOPATH) go vet cordctl/...
	dep check

test:
	GOPATH=$(GOPATH) go test $(TEST_ARGS) -cover -coverprofile=voltctl.cp github.com/ciena/voltctl/...

view-coverage:
	GOPATH=$(GOPATH) go tool cover -html voltctl.cp
