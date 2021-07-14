# Service Type LB deployment using Helm Chart

Services of type `LoadBalancer` are natively supported in Kubernetes deployments on public clouds such as, AWS, GCP, or Azure. In cloud deployments, when you create a service of type LoadBalancer, a cloud managed load balancer is assigned to the service. The service is then exposed using the load balancer.

For on-premises, bare metal, or public cloud deployments of Kubernetes, you can use a Citrix ADC outside the cluster to load balance the incoming traffic. The Citrix ingress controller provides flexible IP address management that enables multitenancy for Citrix ADCs. The Citrix ingress controller allows you to load balance multiple services using a single ADC and also combines various Ingress functions. Using the Citrix ADC with the Citrix ingress controller, you can maximize the utilization of load balancer resources for your public cloud and significantly reduce your operational expenses.

The Citrix ingress controller supports the services of type `LoadBalancer` when the Citrix ADC is outside the Kubernetes cluster (Tier-1). When a service of type `LoadBalancer` is created, updated, or deleted, the Citrix ingress controller configures the Citrix ADC with a load balancing virtual server.

The following diagram shows Citrix solution for service type LoadBalancer:
![Service Type LoadBalancer](images/type-loadbalancer.png)

## Introduction
This document explains how [citrix-cloud-native](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-cloud-native) [Helm](https://helm.sh) chart can be used for service type LB topology which consists of Citrix Ingress Controller for tier-1 Citrix ADC VPX/MPX, Citrix IPAM Contoller and an example application Guestbook in a [Kubernetes](https://kubernetes.io) or in the [Openshift](https://www.openshift.com) cluster.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version 1.6 or later if using Kubernetes environment.
-  The [Openshift](https://www.openshift.com) version 3.11.x or later if using OpenShift platform.
-  The [Helm](https://helm.sh/) version 3.x or later. You can follow instruction given [here](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.
-  You determine the NS_IP IP address needed by the controller to communicate with Citrix ADC. The IP address might be anyone of the following depending on the type of Citrix ADC deployment:

   -  (Standalone appliances) NSIP - The management IP address of a standalone Citrix ADC appliance. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in Clustered mode) CLIP - The cluster management IP (CLIP) address for a clustered Citrix ADC deployment. For more information, see [IP addressing for a cluster](https://docs.citrix.com/en-us/citrix-adc/12-1/clustering/cluster-overview/ip-addressing.html).

-  You have installed [Prometheus Operator](https://github.com/coreos/prometheus-operator), if you want to view the metrics of the Citrix ADC CPX collected by the [metrics exporter](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics).

-  The user name and password of the Citrix ADC VPX or MPX appliance used as the ingress device. The Citrix ADC appliance needs to have system user account (non-default) with certain privileges so that Citrix ingress controller can configure the Citrix ADC VPX or MPX appliance. For instructions to create the system user account on Citrix ADC, see [Create System User Account for CIC in Citrix ADC](#create-system-user-account-for-cic-in-citrix-adc).

    You can pass user name and password using Kubernetes secrets. Create a Kubernetes secret for the user name and password using the following command:

    ```
       kubectl create secret generic nslogin --from-literal=username='cic' --from-literal=password='mypassword'
    ```

#### Create system User account for Citrix ingress controller in Citrix ADC

Citrix ingress controller configures the Citrix ADC using a system user account of the Citrix ADC. The system user account should have certain privileges so that the CIC has permission configure the following on the Citrix ADC:

-  Add, Delete, or View Content Switching (CS) virtual server
-  Configure CS policies and actions
-  Configure Load Balancing (LB) virtual server
-  Configure Service groups
-  Cofigure SSl certkeys
-  Configure routes
-  Configure user monitors
-  Add system file (for uploading SSL certkeys from Kubernetes)
-  Configure Virtual IP address (VIP)
-  Check the status of the Citrix ADC appliance

> **Note:**
>
> The system user account would have privileges based on the command policy that you define.

To create the system user account, do the following:

1.  Log on to the Citrix ADC appliance. Perform the following:
    1.  Use an SSH client, such as PuTTy, to open an SSH connection to the Citrix ADC appliance.

    2.  Log on to the appliance by using the administrator credentials.

2.  Create the system user account using the following command:

    ```
       add system user <username> <password>
    ```

    For example:

    ```
       add system user cic mypassword
    ```

3.  Create a policy to provide required permissions to the system user account. Use the following command:

    ```
       add cmdpolicy cic-policy ALLOW "(^\S+\s+cs\s+\S+)|(^\S+\s+lb\s+\S+)|(^\S+\s+service\s+\S+)|(^\S+\s+servicegroup\s+\S+)|(^stat\s+system)|(^show\s+ha)|(^\S+\s+ssl\s+certKey)|(^\S+\s+ssl)|(^\S+\s+route)|(^\S+\s+monitor)|(^show\s+ns\s+ip)|(^\S+\s+system\s+file)"
    ```

4.  Bind the policy to the system user account using the following command:

    ```
       bind system user cic cic-policy 0
    ```

## Installing the Chart
1. Get the [citrix_cloud_native_values.yaml](../citrix_cloud_native_values.yaml):
   ```
   wget https://code.citrite.net/projects/CNN/repos/citrix-helm-charts/browse/citrix_cloud_native_values.yaml
   ```

2. Add the Citrix Cloud Native helm chart repository using command:
   ```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/
   ```

3. Update the following parameters in the citrix_cloud_native_values.yaml:
   ```
   cic:
     # set enable to true as we want to use CIC for tier-1 ADC
     enabled: true
     # Give the name of the sceret created with tier-1 Citrix ADC VPX/MPX credentials
     adcCredentialSecret: <Secret-for-ADC-credentials>
     # NSIP of tier-1 Citrix ADC VPX/MPX
     nsIP: <NSIP>
     # Accept EULA licence for stanalone CIC
     accept: yes
     # Enable IPAM in CIC
     ipam: true

   ipam:
     # set enable to true as we want to use IPAM controller
     enabled: true
     # IPs in this range are used to assign values for IP to service of type Loadbalancer
     vipRange: '<List-of-free-IP-or-Range>'
   ```

4. Install Chart:
   #### For Kubernetes:
   To install the chart with the release name, `my-release`, use the following command:
   ```
   helm install my-release citrix/citrix-cloud-native -f citrix_cloud_native_values.yaml
   ```

   #### For Openshift:
   * Add the service account named "cic-k8s-role" to the privileged Security Context Constraints of OpenShift:

     ```
     oc adm policy add-scc-to-user privileged system:serviceaccount:<namespace>:cic-k8s-role
     ```
   * Update additonal parameter in citrix_cloud_native_values.yaml:
     ```
     cic:
       openshift: true
     ```
   * To install the chart with the release name, `my-release`, use the following command:
     ```
     helm install my-release citrix/citrix-cloud-native -f citrix_cloud_native_values.yaml
     ```

> **Note:**
>
> By default the chart installs the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and role bindings.

The command deploys Citrix ingress controller for tier-1 ADC VPX/MPX and Citrix ADC CPX with ingress controller for tier-2 on Kubernetes cluster with the default configuration. The following section lists the mandatory and optional parameters that you can configure during installation:

* [Configuration parameters for Citrix Ingress Controller for Citrix ADC VPX/MPX](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-cloud-native/charts/citrix-ingress-controller#configuration)
* [Configuration parameters for Citrix IPAM Controller](https://github.com/citrix/citrix-helm-charts/tree/master/citrix-cloud-native/charts/citrix-ipam-controller#configuration)

5. Deploy the application whose frontend service is of type `LoadBalancer`:
   ```
   kubectl create -f https://code.citrite.net/projects/CNN/repos/citrix-helm-charts/browse/examples/manifests/guestbook_service_type_lb.yaml
   ```

### Installed components

The following components are installed:

- Citrix ingress controller
- Citrix IPAM controller
- Guestbook application

## Route Addition in MPX/VPX
For seamless functioning of services deployed in the Kubernetes cluster, it is essential that Ingress NetScaler device should be able to reach the underlying overlay network over which Pods are running.
`feature-node-watch` knob of Citrix Ingress Controller can be used for automatic route configuration on NetScaler towards the pod network. Refer [Static Route Configuration](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network/staticrouting.md) for further details regarding the same.
By default, `feature-node-watch` is false. It needs to be explicitly set to true if auto route configuration is required.
This can also be achieved by deploying [Citrix Node Controller](https://github.com/citrix/citrix-k8s-node-controller).

For configuring static routes manually on Citrix ADC VPX or MPX to reach the pods inside the cluster follow:

### For Kubernetes:
1. Obtain podCIDR using below options:
   ```
   kubectl get nodes -o yaml | grep podCIDR
   ```
   * podCIDR: 10.244.0.0/24
   * podCIDR: 10.244.1.0/24
   * podCIDR: 10.244.2.0/24

2. Log on to the Citrix ADC instance.

3. Add Route in Netscaler VPX/MPX
   ```
   add route <podCIDR_network> <podCIDR_netmask> <node_HostIP>
   ```
4. Ensure that Ingress MPX/VPX has a SNIP present in the host-network (i.e. network over which K8S nodes communicate with each other. Usually eth0 IP is from this network).

   Example:
   * Node1 IP = 192.0.2.1
   * podCIDR  = 10.244.1.0/24
   * add route 10.244.1.0 255.255.255.0 192.0.2.1

### For OpenShift:
1. Use the following command to get the information about host names, host IP addresses, and subnets for static route configuration.
   ```
   oc get hostsubnet
   ```

2. Log on to the Citrix ADC instance.

3. Add the route on the Citrix ADC instance using the following command.
   ```add route <pod_network> <podCIDR_netmask> <gateway>```

4. Ensure that Ingress MPX/VPX has a SNIP present in the host-network (i.e. network over which OpenShift nodes communicate with each other. Usually eth0 IP is from this network).

    For example, if the output of the `oc get hostsubnet` is as follows:
    * oc get hostsubnet

        NAME            HOST           HOST IP        SUBNET
        os.example.com  os.example.com 192.0.2.1 10.1.1.0/24

    * The required static route is as follows:

           add route 10.1.1.0 255.255.255.0 192.0.2.1

## Acessing the application:
Access http://<External-IP-of-frontend-svc> from browser which opens guestbook application.

## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:

   ```
   helm delete my-release
   ```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Related documentation

- [Citrix ingress controller Documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/)
- [Citrix ingress controller GitHub](https://github.com/citrix/citrix-k8s-ingress-controller)
- [Citrix IPAM controller and Service Type LoadBalancer](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/)
