# From xproto to protobuf

XOS exposes a gRPC API, here is the guide to generate `.proto` files starting from `xproto` files.

## Considerations

The XOS data model is defined through `xProto` (you can read mode on it [here](./xproto.md))
and services load their models at runtime, so the corresponding gRPC API is subject to changes.

There is a set of gRPC API that is stable and defined in [xos/coreapi/protos/utility.proto](https://github.com/opencord/xos/blob/master/xos/coreapi/protos/utility.proto)

The way we address this is to generate the proto files at runtime when a client connects.
You can find an example of this in the `xos-tosca` container, but here a short description of the workflow:

- Load the xProto files using the [GetXproto](https://github.com/opencord/xos/blob/master/xos/coreapi/protos/utility.proto#L100) rpc call
- Generate the `.proto` files using the [xosgenx](./xosgenx.md) toolchain with the [protoapi](https://github.com/opencord/xos/blob/master/lib/xos-genx/xosgenx/targets/protoapi.xtarget) .xtarget

> NOTE that if your are developing against a fixed version you don't need to do this

## Generate proto files

The models that XOS uses are spread in few places:

- core models are in the `xos` repo: [xos/core/models/core.xproto](https://github.com/opencord/xos/tree/master/xos/core/models/core.xproto)
- service models are in the service repo: `xos/synchronizer/models/<service-name>.xproto`

Once you have located the models you need and you have the [virtualenv](./unittest.html#setting-up-a-unit-testing-environment) installed,
you can use this command to generate the `.proto` files:

```bash
xosgenx --target=protoapi.xtarget --write-to-file=single --output=. --dest-file=xos.proto xos/synchronizer/models/hippie-oss.xproto ../olt-service/xos/synchronizer/models/volt.xproto
```



