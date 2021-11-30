# Citrix Node Controller

In Kubernetes environments, sometimes the services are exposed for external access through an ingress device. To route the traffic into the cluster from outside via ingress device, proper routes should be configured between Kubernetes cluster and ingress device. [Citrix](https://www.citrix.com/en-in/) provides a Controller for Citrix ADC MPX (hardware) and Citrix ADC VPX (virtualized) to creates network between the Kubernetes cluster and Citirx ADC VPX/MPX device when they are deployed as an ingress device for a Kubernetes cluster.

## TL;DR;

```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/

   helm install cnc citrix/citrix-node-controller --set license.accept=yes,nsIP=<NSIP>,vtepIP=<Citrix ADC SNIP>,vxlan.id=<VXLAN ID>,vxlan.port=<VXLAN PORT>,network=<IP-address-range-for-VTEP-overlay>,adcCredentialSecret=<Secret-for-ADC-credentials>,cniType=<CNI-overlay-name>
```

> **Important:**
>
> The `license.accept` argument is mandatory. Ensure that you set the value as `yes` to accept the terms and conditions of the Citrix license.

## Introduction
This Helm chart deploys Citrix node controller in the [Kubernetes](https://kubernetes.io) or in the [Openshift](https://www.openshift.com) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version 1.6 or later if using Kubernetes environment.
-  The [Openshift](https://www.openshift.com) version 4.8 or later if using OpenShift platform.
-  The [Helm](https://helm.sh/) version 2.x or later. You can follow instruction given [here](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.
-  You determine the ingress Citrix ADC IP address needed by the controller to communicate with Citrix ADC. The IP address might be anyone of the following depending on the type of Citrix ADC deployment:

   -  (Standalone appliances) NSIP - The management IP address of a standalone Citrix ADC appliance. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).

-  You determine the ingress Citrix ADC SNIP. This IP address is used to establish an overlay network between the Kubernetes clusters needed by the controller to communicate with Citrix ADC.
-  The user name and password of the Citrix ADC VPX or MPX appliance used as the ingress device. The Citrix ADC appliance needs to have system user account (non-default) with certain privileges so that Citrix Node controller can configure the Citrix ADC VPX or MPX appliance. For instructions to create the system user account on Citrix ADC, see [Create System User Account for CNC in Citrix ADC](#create-system-user-account-for-citrix-node-controller-in-citrix-adc)

    You have to pass user name and password using Kubernetes secrets. Create a Kubernetes secret for the user name and password using the following command:

    ```
       kubectl create secret generic nslogin --from-literal=username='cnc' --from-literal=password='mypassword'
    ```

#### Create system User account for Citrix node controller in Citrix ADC

Citrix node controller configures the Citrix ADC using a system user account of the Citrix ADC. The system user account should have certain privileges so that the CNC has permission configure the following on the Citrix ADC:

- Add, Delete, or View routes
- Add, Delete, or View arp
- Add, Delete, or View Vxlan
- Add, Delete, or View IP

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
       add system user cnc mypassword
    ```

3.  Create a policy to provide required permissions to the system user account. Use the following command:

    ```
       add cmdpolicy cnc-policy ALLOW  (^\S+\s+arp)|(^\S+\s+arp\s+.*)|(^\S+\s+route)|(^\S+\s+route\s+.*)|(^\S+\s+vxlan)|(^\S+\s+vxlan\s+.*)|(^\S+\s+ns\s+ip)|(^\S+\s+ns\s+ip\s+.*)|(^\S+\s+bridgetable)|(^\S+\s+bridgetable\s+.*)
    ```

4.  Bind the policy to the system user account using the following command:

    ```
       bind system user cnc cnc-policy 0
    ```

## Installing the Chart
1. Add the Citrix Node Controller helm chart repository using command:
   ```
     helm repo add citrix https://citrix.github.io/citrix-helm-charts/
   ```

2. To install the chart with the release name, `my-release`, use the following command:
   ```
     helm install my-release citrix/citrix-node-controller --set license.accept=yes,nsIP=<NSIP>,vtepIP=<Citrix ADC SNIP>,vxlan.id=<VXLAN ID>,vxlan.port=<VXLAN PORT>,network=<IP-address-range-for-VTEP-overlay>,adcCredentialSecret=<Secret-for-ADC-credentials>
   ```

> **Note:**
>
> By default the chart installs the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and role bindings.

The command deploys Citrix node controller on Kubernetes cluster with the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

### Installed components

The following components are installed:

-  [Citrix Node Controller](https://github.com/citrix/citrix-k8s-node-controller)

### Configuration

The following table lists the mandatory and optional parameters that you can configure during installation:

| Parameters | Mandatory or Optional | Default value | Description |
| --------- | --------------------- | ------------- | ----------- |
| license.accept | Mandatory | no | Set `yes` to accept the CNC end user license agreement. |
| image | Mandatory | `quay.io/citrix/citrix-k8s-node-controller:2.2.8` | The CNC image. |
| pullPolicy | Mandatory | IfNotPresent | The CNC image pull policy. |
| adcCredentialSecret | Mandatory | N/A | The secret key to log on to the Citrix ADC VPX or MPX. For information on how to create the secret keys, see [Prerequisites](#prerequistes). |
| nsIP | Mandatory | N/A | The IPaddress or Hostname of the Citrix ADC device. For details, see [Prerequisites](#prerequistes). |
| vtepIP | Mandatory | N/A | The Citrix ADC SNIP. |
| network | Mandatory | N/A | The IP address range that CNC uses to configure the VTEP overlay end points on the Kubernetes nodes. |
| vxlan.id | Mandatory | N/A | A unique VXLAN VNID to create a VXLAN overlay between Kubernetes cluster and the ingress devices. |
| vxlan.port | Mandatory | N/A | The VXLAN port that you want to use for the overlay. |
| cniType | Mandatory | N/A | The CNI used in k8s cluster. Valid values: flannel,calico,canal,weave,cilium |
| dsrIPRange | Optional | N/A | This IP address range is used for DSR Iptable configuration on nodes. Both IP and subnet must be specified in format : "xx.xx.xx.xx/xx"  |
| clusterName | Optional | N/A | Unique identifier for the kubernetes cluster on which CNC is deployed. If Provided CNC will configure PolicyBasedRoutes instead of static Routes. For details, see [CNC-PBR-SUPPORT](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/docs/how-to/pbr.md#configure-pbr-using-the-citrix-node-controller) |
| cncRouterImage | Optional | N/A | The Internal Repo Image to be used for kube-cnc-router helper pods when internet access is disabled on cluster nodes. For more details, see [running-cnc-without-internet-access](https://github.com/citrix/citrix-k8s-node-controller/blob/master/deploy/README.md#running-citrix-node-controller-without-internet-access) |
Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

> **Note:**
>
> 1. Ensure that the subnet that you provide in "network" is different from your Kubernetes cluster
> 2. Ensure that the VXLAN ID that you use in vxlan.id does not conflict with the Kubernetes cluster or Citrix ADC VXLAN VNID
> 3. Ensure that the VXLAN PORT that you use in vxlan.port does not conflict with the Kubernetes cluster or Citrix ADC VXLAN PORT.

For example:
```
   helm install my-release citrix/citrix-node-controller -f values.yaml
```

> **Tip:** 
>
> The [values.yaml](https://github.com/citrix/citrix-helm-charts/blob/master/citrix-node-controller/values.yaml) contains the default values of the parameters.

## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:

```
   helm delete my-release
```
The command removes all the Kubernetes components associated with the chart and deletes the release.

## Related documentation

-  [Citrix node controller Documentation](https://github.com/citrix/citrix-k8s-node-controller)
