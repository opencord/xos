# Kubernetes on a Laptop 

XOS runs on any version of Kubernetes (1.10 or greater), and uses the 
Helm client-side tool. If you are new to Kubernetes, we recommend https://kubernetes.io/docs/tutorials/ as a good place to start. 

Although you are free to set up Kubernetes and Helm in whatever way 
makes sense for your deployment, the following walks you through an 
example installation sequence on  MacOS. It was tested on version 10.12.6. 

By the end of the installation process, you will have a running XOS 
control plane, plus one example service (cleverly called `SimpleExampleService`) 
deployed as a Kubernetes pod. 

## Prerequisites 

You need to install Docker. Visit `https://docs.docker.com/docker-for-mac/install/` for instructions. 

You also need to install VirtualBox. Visit `https://www.virtualbox.org/wiki/Downloads` for instructions. 

The following assumes you've installed the Homebrew package manager. Visit 
`https://brew.sh/` for instructions. 

## Install Minikube and Kubectl 

To install Minikube, run the following command:

```shell 
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.28.0/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```
To install Kubectl, run the following command:

```shell 
brew install kubectl 
```

## Install Helm and Tiller 

The following installs both Helm and Tiller. 

```shell 
brew install kubernetes-helm 
```

## Bring Up a Kubernetes Cluster 

Start a minikube cluster as follows. This automatically runs inside VirtualBox. 

```shell 
minikube start 
```

To see that it's running, type 

```shell 
kubectl cluster-info 
```

You should see something like the following 

```shell 
Kubernetes master is running at https://192.168.99.100:8443 
KubeDNS is running at https://192.168.99.100:8443/api/v1/namespaces/kube-system/services/kube-dns:dn s/proxy 

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'. 
```

You can also see how the cluster is configured by looking at `~/.kube/config`. 
Other tools described on this page use this configuration file to find your cluster. 

If you want, you can see minikube running by looking at the VirtualBox dashboard. 
Or alternatively, you can visit the Minikube dashboard:

```shell 
minikube dashboard 
```

As a final setp, you need to start Tiller on the Kubernetes cluster. 

```shell 
helm init 
```

## Download CORD Helm-Charts 

You don't need to download all of CORD. You just need to download a set of helm charts. They will, in turn, download a collection of CORD containers from Docker 
Hub. The rest of this section assumes all CORD-related downloads are placed in 
directory `~/cord`. 

```shell 
mkdir ~/cord 
cd ~/cord 
git clone https://gerrit.opencord.org/helm-charts 
cd helm-charts 
```

## Bring Up CORD 

Deploy the service profiles corresponding to the `xos-core`,
`base-kubernetes`, and `demo-simpleexampleservice` helm-charts. 
To do this, execute the following from the `~/cord/helm-charts` directory. 

```shell 
helm dep update xos-core 
helm install xos-core -n xos-core 
helm dep update xos-profiles/base-kubernetes 
helm install xos-profiles/base-kubernetes -n base-kubernetes 
helm dep update xos-profiles/demo-simpleexampleservice 
helm install xos-profiles/demo-simpleexampleservice -n demo-simpleexampleservice 
```

Use `kubectl get pods` to verify that all containers in the profile 
are successful and none are in the error state. 

> **Note:** It will take some time for the various helm charts to 
> deploy and the containers to come online. The `tosca-loader`
> container may error and retry several times as it waits for 
> services to be dynamically loaded. This is normal, and eventually 
> the `tosca-loader` will enter the completed state. 

When all the containers are successfully up and running, `kubectl get pod`
will return output that looks something like this:

```shell 
NAME                                           READY     STATUS    RESTARTS   AGE 
base-kubernetes-kubernetes-55c55bd897-rn9ln    1/1       Running   0          2m 
base-kubernetes-tosca-loader-vs6pv             1/1       Running   1          2m 
demo-simpleexampleservice-787454b84b-ckpn2     1/1       Running   0          1m 
demo-simpleexampleservice-tosca-loader-4q7zg   1/1       Running   0          1m 
xos-chameleon-6f49b67f68-pdf6n                 1/1       Running   0          2m 
xos-core-57fd788db-8b97d                       1/1       Running   0          2m 
xos-db-f9ddc6589-rtrml                         1/1       Running   0          2m 
xos-gui-7fcfcd4474-prhfb                       1/1       Running   0          2m 
xos-redis-74c5cdc969-ppd7z                     1/1       Running   0          2m 
xos-tosca-7c665f97b6-krp5k                     1/1       Running   0          2m 
xos-ws-55d676c696-pxsqk                        1/1       Running   0          2m 
```

## Visit CORD Dashboard 

Finally, to view the CORD dashboard, run the following:

```shell 
minikube service xos-gui 
```

This will launch a window in your default browser. Administrator login 
and password are defined in `~/cord/helm-charts/xos-core/values.yaml`. 

## Next Steps 

This completes our example walk-through. At this point, you can do one 
of the following:

* Explore other [installation options](README.md). 
* Take a tour of the [operational interfaces](operating_cord/general.md). 
* Drill down on the internals of [SimpleExampleService](simpleexampleservice/simple-example-service.md). 
