#Core Models

*This description is in-progress...*

CORD adopts a model-based design. Each service configured into a given CORD deployment has a service-specific model, but CORD as a whole defines a core set of models. Service-specific models are anchored in these core models.

CORD's core models are defined by a set of [xproto](dev/xproto.md)
specifications, which can be found in their full detail in the source
code:
[core.xproto](https://github.com/opencord/xos/blob/master/xos/core/models/core.xproto).
The following describes these core model -- along with the
relationships among them -- in words.

* **Service:** Represents an elastically scalable, multi-tenant program, including
the means to instantiate, control, and scale functionality.

   - Bound to a set of Slices that collectively contains the collection of
      virtualized resources (e.g., compute, network) in which the Service runs.

   - Bound to a set of Controllers that represents the service's control 
      interface.

* **ServiceDependency:** Represents a dependency of a *Subscriber*
Service on a *Provider* Service. A collection of ServiceDependency
and Service models, representing edges and verticies, respectively,
form a *Service Graph*. (There is no explicit **ServiceGraph** model.)

* **Slice:** A distributed resource container that includes the compute and 
network resources that belong to (are used by) a Service.

   - Bound to a (possibly empty) set of Instances that provide compute
      resources for the Slice. 

   - Bound to a set of Networks that connect the Slice's Instances to
      each other, and connect this Slice to the Slices of other Services.
  
   - Bound to a Flavor that defines how the Slice's Instances are 
      scheduled. 

   - Bound to an Image that boots in each of the Slice's Instances. 

* **Instance:** A single compute instance, implemented as either a VM
or a container, associated with a Slice. Each Instance is instantiated on
some physical Node. 

* **Network:** A virtual network associated with a Slice. Networks are
of one of the following Types:

   - **PRIVATE:** Virtual network for the instances in the same service
   - **PUBLIC:** Externally accessible network
   - **MANAGEMENT_LOCAL:** Instance management network which does not span
      compute nodes, only accessible from the host machine
   - **MANAGEMENT_HOST:** Real management network which spans compute and
 	  head nodes
   - **ACCESS_AGENT:** Network for access agent infrastructure service

* **Image:** A bootable image that runs in a virtual machine. Each 
  Image implies a virtualization layer (e.g., Docker, KVM), so the latter 
  need not be a distinct object. 

* **Flavor:** A pre-packaged collection of resources (e.g., disk,
  memory, and cores). Current flavors borrow from EC2. 

* **Controller:** An object that represents the binding of a site to 
  a back-end service (e.g., an OpenStack head node). Includes the URL 
  at which the back-end service controller can be invoked and the 
  credentials needed to invoke it. 

* **Node:** A physical server that can be virtualized. 

   - Bound to the Site where the Node is physically located.

   - Bound to a Deployment that defines the policies applied to the 
     Node. 

##Principals

* **User:** A principle that invokes operations on objects and uses 
  XOS resources. 

* **Role:** A set of privileges granted to a User in the scope of 
  some set of objects. 

* **Tenant:** Represents a binding of a tenant service to a provider 
  service, and so corresponds to the edges in a service dependency 
  graph. Each Tenant object includes the means by which the two 
  services connect in the data plane. Current objects include Public 
  and Shared-Private. 

* **TenantRoot:** Represents a principal... 

* **Privilege:** Represents the right to perform a set of operations on a set of models, objects, and fields.

##Sites and Deployments

Typically, CORD implies a single configuration of a POD deployed in a single site. However, the underlying core includes two models for multi-site deployments: **Site** and **Deployments**.

Sites and Deployments can be one-to-one, which corresponds to a each 
Site establishing its own policies. In practice, however, we expect 
Deployments will often span multiple Sites, where those Sites either 
correspond to a single distributed organization (e.g., Internet2) or 
agree to manage their Nodes in collaboration with the containing 
Deployment (e.g., Enterprise). It is also possible that a Site hosts 
Nodes that belong to more than one Deployment. 

Correspondingly, a Controller object represents the binding between 
Deployments and Sites. There could be one Controller per Site in the 
Deployment (i.e., one OpenStack head node per Site) or one Controller 
might be bound to a set of Sites (i.e., one OpenStack head node 
manages a set of Sites). 

* **Site:** A logical grouping of Nodes that are co-located at the
  same geographic location, which also typically corresponds to the
  Nodes' location in the physical network.

  - Bound to a set of Users that are affiliated with the Site.

  - Bound to a set of Nodes located at the Site.

  - Bound to a set of Deployments that the Site may access.

* **Deployment:** A logical grouping of Nodes running a compatible set
  of virtualization technologies and being managed according to a
  coherent set of resource allocation policies.

  - Bound to a set of Users that establish the Deployment's policies.

  - Bound to a set of Nodes that adhere to the Deployment's policies.

  - Bound to a set of supported Images that can be booted on the
    Deployment's nodes.

  - Bound to a set of supported NetworkTemplates that can connect VMs
    in the deployment.

  - Bound to a set of supported Flavors that establish allocation
    parameters.

  - Bound to a set of Controllers that represent the back-end
    infrastructure service that provides cloud resources (e.g., an
    OpenStack head node).

