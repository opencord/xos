# Core Models

Each service in CORD defines one or more service-specific models,
which are in turn reference and extend a set of *core*  models.
Collectively, these models define relationships among the various
components in CORD (e.g., between a service and the resources
allocated to that service). Individually, each model defines a set
of fields that are used to either configure/control the underlying
component (these fields are said to hold *declarative state*) or to
record operational data about the underlying component (these
fields are said to hold *feedback state*). For more information
about declarative and feedback state, and the role they play in
synchornizing the data model with the backend components,
read about the [Synchronizer Architecture](dev/sync_arch.md).

CORD's core models are defined by a set of [xproto](dev/xproto.md)
specifications. They are defined in their full detail in the source
code. See:
[core.xproto](https://github.com/opencord/xos/blob/master/xos/core/models/core.xproto).
The following describes these core models -- along with the
relationships (bindings) among them -- in words.

* **Service:** Represents an elastically scalable, multi-tenant
program, including the declarative state needed to instantiate,
control, and scale functionality.

   - Bound to a set of `Slices` that contains the collection of
      virtualized resources (e.g., compute, network) in which the
      `Service` runs.

  In many CORD documents you will see mention of each service also
  having a "controller" but this effectively corresponds to the
  `Service` model itself, which is used to generate a "control
  interface" for the service. There is no explicit "Controller" model
  bound to a service. (There actually is a `Controller` model today,
  but it represents information about OpenStack, and is expected to
  be deprecated as we model OpenStack like any other service.)
   
* **ServiceDependency:** Represents a dependency between a *Subscriber*
service on a *Provider*  service. The set of `ServiceDependency` 
and `Service` models defined in CORD collectively represent the edges 
and verticies of a *Service Graph*, but there is no explicit
"ServiceGraph" model in CORD. The dependency between a pair of
services is parameterized by the method by which the service are
interconnected in the data plane. `Connect` methods include:

   - **None:** The two services are not connected in the data plane. 
   - **Private:** The two services are connected by a common private network. 
   - **Public:** The two services are connected by a publicly routable 
   network. 
   

* **ServiceInstance:** Represents an instance of a service
  instantiated on behalf of a particular tenant. This is a
  generalization of the idea of a Compute-as-a-Service spinning up
  individual "compute instances," or using another common
  example, the `ServiceInstance` corresponding to a Storage Service
  might be called a "Volume" or a "Bucket." Confusingly, there are
  also instances of a `Service` model that represent different
  services, but this is a consequence of standard modeling
  terminology, whereas  `ServiceInstance` is a core model in CORD
  (and yes, there are instances of the `ServiceInstance` model).

* **ServiceInstanceLink:** Represents a logical connection between
`ServiceInstances` of two `Services`. A related model, `ServiceInterface`,
types the `ServiceInstanceLink` between two `ServiceInstances`. A
connected sequence of `ServiceInstances` and `ServiceInstanceLinks` form
what is often called a *Service Chain*, but there is no explicit
"ServiceChain" model in CORD.

* **Slice:** Represents a distributed resource container that includes
the compute and network resources that belong to (are used by) some
`Service`.

   - Bound to a set of `Instances` that provide compute resources for
      the `Slice`.

   - Bound to a set of `Networks` that connect the  slice's `Instances` to
      each other.
  
   - Bound to a `Flavor` that represents a bundle of resources (e.g., disk, memory,
      and cores) allocated to an instance. Current flavors borrow from EC2. 

   - Bound to an `Image` that boots in each of the slice's`Instances`.
      Each `Image` implies a virtualization layer (e.g., Docker, KVM).


* **Instance:** Represents a single compute instance associated
   with a Slice and instantiated on some physical Node. Each Instance
   is of some `isolation` type: `vm` (implemented as a KVM virtual machine),
   `container` (implemented as a Docker container), or `container_vm`
   (implemented as a Docker container running inside a KVM virtual machine).

* **Network:** Represents a virtual network associated with a `Slice`. The
behavior of a given `Network`is defined by a `NetworkTemplate`, which
specifies a set of parameters, including `visibility` (set to `public` or
`private`),  `access` (set to `direct` or `indirect`), `translation`
(set to `none`or `nat`), and `topology_kind` (set to `bigswitch`,
`physical` or `custom`). There is also a `vtn_kind` parameter
(indicating the `Network` is manged by VTN), with possible settings:
`PRIVATE`, `PUBLIC`, `MANAGEMENT_LOCAL`, `MANAGEMENT_HOST`,
`VSG`, or `ACCESS__AGENT`.

* **Node:** Represents a physical server that can be virtualized and host Instances.

   - Bound to the `Site` where the `Node` is physically located.


* **User:** Represents an authenticated principal that is granted a set of
  privileges to invoke operations on a set of models, objects, and
  fields in the data model.

* **Privilege:** Represents the right to perform a set of read, write,
  or grant operations on a set of models, objects, and fields.

* **Site:** Represents a logical grouping of `Nodes` that are
  co-located at the same geographic location, which also typically
  corresponds to the nodes' location in the physical network.

  - Bound to a set of `Nodes` located at the `Site`.


  The typical use case involves one configuration of a CORD POD 
  deployed at a single location. However, the underlying core includes 
  allows for multi-site deployments.
