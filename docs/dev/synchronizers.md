# Writing Synchronizers

Synchronizers are the components of CORD that map the abstract
declarative state about how the system is suppose to behave (as defined by the
XOS data model) into the concrete operational state of the backend components
that implement the system (e.g., VNFs, micro-services, SDN control
applications).

Writing a Synchronizer is half of the work required to on-board a service into
CORD. First a model for the service is written as an [xproto](xproto.md)
specification, and then you implement a synchronizer that translates that model
onto some backend component.

To implement a Synchronizer, it is important to first understand the role they
play in CORD and the assumptions made about their behavior. The next section
describes a set of [design guidelines](sync_arch.md) and the following one
presents the [implementation details](sync_impl.md).

## Overview of the synchronizer framework APIs

This section is intended to be a reference for the commonly used APIs exposed by the synchronizer framework.

### Model Policies

Model Policies can be seen as `post-save` hooks and they are generally defined in the `xos/synchronizer/model_policies` folder of your service.

Model policies are generally used to dynamically create a service chain (when a ServiceInstance is created it will create a ServiceInstance of its east side Service)

> Note that you'll need to add this folder in your synchronizer configuration file as 
>```yaml
> model_policies_dir: "/opt/xos/synchronizers/<synchronizer_name>/model_policies"
>```

A model policy is a class that inherits from `Policy`

```python
from synchronizers.new_base.modelaccessor import MyServiceInstance, ServiceInstanceLink, model_accessor
from synchronizers.new_base.policy import Policy
 
class MyServiceInstancePolicy(Policy):
    model_name = "MyServiceInstance"
```

and overrides one or more of the following methods:

```python
def handle_create(self, model):
```

```python
def handle_update(self, model):
```

```python
def handle_delete(self, model):
```
> where model is the instance of the model that has been created

### Sync Steps

Sync Steps are the actual piece of code that provide the mapping between your models and your backend. 
You will need to define a sync step for each model.

> Note that you'll need to add this folder in your synchronizer configuration file as 
>```yaml
> steps_dir: "/opt/xos/synchronizers/<synchronizer_name>/steps"
>```

A Sync Step is a class that inherits from `SyncStep`

```python

from synchronizers.new_base.SyncInstanceUsingAnsible import SyncStep
from synchronizers.new_base.modelaccessor import MyModel

from xosconfig import Config
from multistructlog import create_logger
 
log = create_logger(Config().get('logging'))
 
class SyncMyModel(SyncStep):
    provides = [MyModel]

    observes = MyModel
```

and provides these methods:
```python
def sync_record(self, o):
    log.info("sync'ing object", object=str(o), **o.tologdict())
```

```python
def delete_record(self, o):
    log.info("deleting object", object=str(o), **o.tologdict())
```

This methods will 