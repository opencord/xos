# Mock Workflow

This document describes a workflow for service or core development using a local 
environment with the `rcord-mock` or `rcord-single` profile. To learn more about scenarios you can refer to [Build Internals](../../build_internals.md#included-scenarios)

This workflow is intended to verify the correctness of your development on:
- `core` models
- `service` models
- `gui`
- `synchronizers` steps
- `profile`s configuration

For the rest of this guide, we assume that you already have cloned the source code 
following the guide in: [Getting the Source Code](../../cord_repo.md)

## Requirements

In order to deploy a `mock` or a `single` scenario on your machine
you'll need to have [Vagrant](https://www.vagrantup.com/) installed.

## Initial deployment

You can setup a `mock` deployment on you machine:

```
cd ~/cord/build
make PODCONFIG=rcord-mock.yml config
make -j4 build
```

This will setup a `Vagrant VM` on your machine, 
and once that the install has completed you can access:
- the UI at `192.168.46.100:8080/xos`
- the vagrant VM just by `ssh headnode`

### Configure your deployment

By default the `libvirt` provider is used to manage Vagrant's vm, 
if you prefer to use `VirtualBox` (this is the typical Mac OS case),
you can invoke the build command as:
```
VAGRANT_PROVIDER=virtualbox make -j4 build
```

The VM that is created as part of this lightweight deployment is configured
by default as:

| Scenario      | Memory        | Cores |
| ------------- |:-------------:| -----:|
| mock          | 2048          |     4 |
| single        | 4096          |     8 |

This configuration is defined in `~/cord/build/scenarios/mock/config.yaml` 
and `~/cord/build/scenarios/single/config.yaml`, you can
change those parameter to scale up or down your development
VM accordingly to your laptop resources.

## Development loop

Note that the code is shared in the VM so that:
- `~/cord` is mounted on `/opt/cord`
- `~/cord_profile` is mounted on `/opt/cord_profile`
- `~/cord/platform-install/credentials/` is mounted on `~/opt/credentials` (only in the `single` scenario)

### Update the code running in the containers

```
cd ~/cord/build
make xos-update-images
make -j4 build
```

### Destroy and rebuild XOS

This is the workflow that you'll need to follow if you want 
start from a fresh XOS installation. Note that it will wipe the
database out.

```
cd ~/cord/build
make xos-teardown
make -j4 build
```

### Update the profile configuration
```
cd ~/cord/build
make clean-genconfig
make PODCONFIG=rcord-mock.yml config
make -j4 build
```
