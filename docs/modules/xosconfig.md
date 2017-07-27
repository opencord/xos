# XOS Config

This module is responsible for reading, validating and distributing
the configuration for all XOS-related components.

_The code for this module can be found in lib/xos-config_

The `xosconfig` module uses a combination of parameters provided
via a `.yaml` file and a service discovery mechanism.

## How to Use This Module

This module needs to be initialized once (and only once) when you
start the application. Yyou can do it with:

```python
from xosconfig import Config
Config.init()
```

By default, the `xosconfig` module looks for a configuration file
in `/opt/xos/config.yaml`. If for any reason you need to pass a
different config file, it can be done with:

```python
from xosconfig import Config
Config.init("/path/to/my/config.yaml")
```

### Configuration Defaults

Note that defaults are defined for some of the configuration items.
Defaults are defined in `lib/xos-config/xosconfig/default.py`.

### Reading Data from the Configuration File

To access static information defined in the `config.yaml` file, use
the following API:

```python
from xosconfig import Config
res = Config.get('database')
```
this call returns something like:

```python
{
    'username': 'test',
    'password': 'safe'
}
```

Since the configuration support nested dictionary, it is possible to
query directly nested values using the `dot` notation. For example:

```python
from xosconfig import Config
res = Config.get('database.username')
```

returns

```python
"test"
```

**The configuration schema is defined in `/lib/xos-config/config-schema.yaml`**

### Reading Service Information

XOS is composed of a set of services. To discover these services and
their address, use the
[registrator](https://github.com/gliderlabs/registrator) tool.
 
#### Retrieving a List of Services

Invoking

```python
from xosconfig import Config
Config.get_service_list()
```

returns an array of available services; by default:

```python
[
  "xos-ws",
  "xos-ui-deprecated",
  "xos-rest",
  "xos-gui",
  "xos-db",
  "consul-rest",
  "consul",
]
```

>You can get the same information on the `head node` using:
>```bash
> curl consul:8500/v1/catalog/services
>```

#### Retrieve Information for a Single Service

Invoking

```python
from xosconfig import Config
Config.get_service_info('xos-db')
```

returns

```python
{
    'name': 'xos-db',
    'url': '172.18.0.4',
    'port': 5432
}
```
>You can get the same information on the `head node` using:
>```bash
> curl consul:8500/v1/catalog/service/xos-db
>```

#### Retrieving Endpoint for a Single Service

Invoking

```python
from xosconfig import Config
Config.get_service_endpoint('xos-db')
```

returns

```python
"http://172.18.0.4:5432"
```
