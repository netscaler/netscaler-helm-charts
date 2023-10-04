# NetScaler Node Controller

In Kubernetes environments, sometimes the services are exposed for external access through an ingress device. To route the traffic into the cluster from outside via ingress device, proper routes should be configured between Kubernetes cluster and ingress device. [NetScaler](https://www.netscaler.com/) provides a Controller for NetScaler MPX (hardware) and NetScaler VPX (virtualized) to creates network between the Kubernetes cluster and Citirx NetScaler VPX/MPX device when they are deployed as an ingress device for a Kubernetes cluster.

## TL;DR;

```
   helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

   helm install cnc netscaler/citrix-node-controller --set license.accept=yes,nsIP=<NSIP>,vtepIP=<NetScaler SNIP>,vxlan.id=<VXLAN ID>,vxlan.port=<VXLAN PORT>,network=<IP-address-range-for-VTEP-overlay>,adcCredentialSecret=<Secret-for-NetScaler-credentials>,cniType=<CNI-overlay-name>
```

> **Important:**
>
> The `license.accept` argument is mandatory. Ensure that you set the value as `yes` to accept the terms and conditions of the NetScaler license.

## Introduction
This Helm chart deploys NetScaler node controller in the [Kubernetes](https://kubernetes.io) or in the [Openshift](https://www.openshift.com) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version 1.6 or later if using Kubernetes environment.
-  The [Openshift](https://www.openshift.com) version 4.8 or later if using OpenShift platform.
-  The [Helm](https://helm.sh/) version 2.x or later. You can follow instruction given [here](https://github.com/netscaler/netscaler-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.
-  You determine the ingress NetScaler IP address needed by the controller to communicate with NetScaler. The IP address might be anyone of the following depending on the type of NetScaler deployment:

   -  (Standalone appliances) NSIP - The management IP address of a standalone NetScaler appliance. For more information, see [IP Addressing in NetScaler](https://docs.netscaler.com/en-us/citrix-adc/current-release/networking/ip-addressing.html).

    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in NetScaler](https://docs.netscaler.com/en-us/citrix-adc/current-release/networking/ip-addressing.html).

-  You determine the ingress NetScaler SNIP. This IP address is used to establish an overlay network between the Kubernetes clusters needed by the controller to communicate with NetScaler.
-  The user name and password of the NetScaler VPX or MPX appliance used as the ingress device. The NetScaler appliance needs to have system user account (non-default) with certain privileges so that NetScaler Node controller can configure the NetScaler VPX or MPX appliance. For instructions to create the system user account on NetScaler, see [Create System User Account for NSNC in NetScaler](#create-system-user-account-for-citrix-node-controller-in-citrix-adc)

    You have to pass user name and password using Kubernetes secrets. Create a Kubernetes secret for the user name and password using the following command:

    ```
       kubectl create secret generic nslogin --from-literal=username='cnc' --from-literal=password='mypassword'
    ```

#### Create system User account for NetScaler node controller in NetScaler

NetScaler node controller configures the NetScaler using a system user account of the NetScaler. The system user account should have certain privileges so that the NSNC has permission configure the following on the NetScaler:

- Add, Delete, or View routes
- Add, Delete, or View arp
- Add, Delete, or View Vxlan
- Add, Delete, or View IP

> **Note:**
>
> The system user account would have privileges based on the command policy that you define.

To create the system user account, do the following:

1.  Log on to the NetScaler appliance. Perform the following:
    1.  Use an SSH client, such as PuTTy, to open an SSH connection to the NetScaler appliance.

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
1. Add the NetScaler Node Controller helm chart repository using command:
   ```
     helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/
   ```

2. To install the chart with the release name, `my-release`, use the following command:
   ```
     helm install my-release citrix/citrix-node-controller --set license.accept=yes,nsIP=<NSIP>,vtepIP=<NetScaler SNIP>,vxlan.id=<VXLAN ID>,vxlan.port=<VXLAN PORT>,network=<IP-address-range-for-VTEP-overlay-in-CIDR-format>,adcCredentialSecret=<Secret-for-NetScaler-credentials>
   ```

## Providing Tolerations
Successful Node controller deployment involves two types of pods:

i) Node controller pod and

ii) kube-cnc-router-pod

Node controller pod might need to be provided with particular tolerations so that it can be scheduled on a tainted node(s). 
Tolerations of the node-controller pod can be provided with `deploymentTolerations` variable in the values.yaml. 
Here is an example of helm command to provide **tolerations to the node-controller**:
```
   helm install my-release netscaler-helm-charts/citrix-node-controller --set license.accept=yes,nsIP=<NSIP>,vtepIP=<NetScaler SNIP>,vxlan.id=<VXLAN ID>,vxlan.port=<VXLAN PORT>,network=<IP-address-range-for-VTEP-overlay-in-CIDR-format>,adcCredentialSecret=<Secret-for-NetScaler-credentials>,cniType=<CNI> \
   --set deploymentTolerations[0].key=myCustomKey1,deploymentTolerations[0].operator=Exists,deploymentTolerations[0].effect=NoExecute --set deploymentTolerations[1].key=myCustomKey2,deploymentTolerations[1].operator=Exists,deploymentTolerations[1].effect=NoExecute
```

This node-controller pod creates the kube-cnc-router-pod on each worker node of the Kubernetes cluster. 
These kube-cnc-router-pods also might need to be provided with a particular set of tolerations to ensure appropriate effect on the tainted node.
Tolerations for this kube-cnc-router pod should be provided in the **JSON format** in a NSNC configmap using `cncConfigMap.tolerationsInJson` variable. 
Here is an example  helm command to provide **tolerations for the kube-cnc-router pod**:
```
   helm install my-release netscaler-helm-charts/citrix-node-controller --set license.accept=yes,nsIP=<NSIP>,vtepIP=<NetScaler SNIP>,vxlan.id=<VXLAN ID>,vxlan.port=<VXLAN PORT>,network=<IP-address-range-for-VTEP-overlay-in-CIDR-format>,adcCredentialSecret=<Secret-for-NetScaler-credentials>,cniType=<CNI> \
   --set-json cncConfigMap.tolerationsInJson='[{"key": "myCustomKey1","operator": "Equal","value": "myValue1","effect": "NoExecute"},{"key": "myCustomKey2","operator": "Equal","value": "myValue2","effect": "NoExecute"}]'
```

### Providing tolerations in values.yaml

These tolerations can also be provided in values.yaml like below:

```
cncConfigMap:
  name:
  tolerationsInJson: [{"key": "myCustomKey1","operator": "Equal","value": "myValue1","effect": "NoExecute"},{"key": "myCustomKey2","operator": "Equal","value": "myValue2","effect": "NoExecute"}]
deploymentTolerations:
  - key: myCustomKey1
    effect: NoExecute
    operator: Exists
  - key: myCustomKey2
    effect: NoExecute
    operator: Exists
```

> **Note:**
>
> By default the chart installs the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and role bindings.

The command deploys NetScaler node controller on Kubernetes cluster with the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

### Installed components

The following components are installed:

-  [NetScaler Node Controller](https://github.com/netscaler/netscaler-k8s-node-controller)

### Configuration

The following table lists the mandatory and optional parameters that you can configure during installation:

| Parameters | Mandatory or Optional | Default value | Description |
| --------- | --------------------- | ------------- | ----------- |
| license.accept | Mandatory | no | Set `yes` to accept the NSNC end user license agreement. |
| imageRegistry                   | Mandatory  |  `quay.io`               |  The NSNC image registry             |  
| imageRepository                 | Mandatory  |  `citrix/citrix-k8s-node-controller`              |   The NSNC image repository             | 
| imageTag                  | Mandatory  |  `2.2.10`               |  The NSNC image tag            | 
| pullPolicy | Mandatory | IfNotPresent | The NSNC image pull policy. |
| nameOverride | Optional | N/A | String to partially override deployment fullname template with a string (will prepend the release name) |
| fullNameOverride | Optional | N/A | String to fully override deployment fullname template with a string |
| adcCredentialSecret | Mandatory | N/A | The secret key to log on to the NetScaler VPX or MPX. For information on how to create the secret keys, see [Prerequisites](#prerequistes). |
| nsIP | Mandatory | N/A | The IPaddress or Hostname of the NetScaler device. For details, see [Prerequisites](#prerequistes). |
| vtepIP | Mandatory | N/A | The NetScaler SNIP. |
| network | Mandatory | N/A | The IP address range that NSNC uses to configure the VTEP overlay end points on the Kubernetes nodes. |
| vxlan.id | Mandatory | N/A | A unique VXLAN VNID to create a VXLAN overlay between Kubernetes cluster and the ingress devices. |
| vxlan.port | Mandatory | N/A | The VXLAN port that you want to use for the overlay. |
| cniType | Mandatory | N/A | The CNI used in k8s cluster. Valid values: flannel,calico,canal,weave,cilium |
| dsrIPRange | Optional | N/A | This IP address range is used for DSR Iptable configuration on nodes. Both IP and subnet must be specified in format : "xx.xx.xx.xx/xx"  |
| clusterName | Optional | N/A | Unique identifier for the kubernetes cluster on which NSNC is deployed. If Provided NSNC will configure PolicyBasedRoutes instead of static Routes. For details, see [NSNC-PBR-SUPPORT](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/network/pbr.md#configure-pbr-using-the-citrix-node-controller) |
| cncConfigMap.name | Optional | N/A | ConfigMapName which NSNC will watch for to add/delete configurations. If not set, it will be auto-generated |
| deploymentTolerations | Optional | N/A | Tolerations to be associated with the Node controller pod. Provide in the format `--set deploymentTolerations[0].key=key1,deploymentTolerations[0].operator=Exists,deploymentTolerations[0].effect=NoSchedule` |
| cncConfigMap.tolerationsInJson | Optional | N/A | Tolerations to be associated with the Kube-cnc-router pods. Provide in the appropriate JSON format `--set-json cncConfigMap.tolerationsInJson='[{"key": "first","operator": "Equal","value": "one","effect": "NoExecute"},{"key": "second","operator": "Equal","value": "true","effect": "NoExecute"}]'` |
| cncRouterImage | Optional | N/A | The Internal Repo Image to be used for kube-cnc-router helper pods when internet access is disabled on cluster nodes. For more details, see [running-cnc-without-internet-access](https://github.com/netscaler/netscaler-k8s-node-controller/blob/master/deploy/README.md#running-citrix-node-controller-without-internet-access) |
| cncRouterName | Optional | N/A | The name to be used for ServiceAccount/RBAC/ConfigMap and even as prefix for kube-cnc-router helper pods. If not set, it will be auto-generated. |
Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

> **Note:**
>
> 1. Ensure that the subnet that you provide in "network" is different from your Kubernetes cluster
> 2. Ensure that the VXLAN ID that you use in vxlan.id does not conflict with the Kubernetes cluster or NetScaler VXLAN VNID
> 3. Ensure that the VXLAN PORT that you use in vxlan.port does not conflict with the Kubernetes cluster or NetScaler VXLAN PORT.

For example:
```
   helm install my-release citrix/citrix-node-controller -f values.yaml
```

> **Tip:** 
>
> The [values.yaml](https://github.com/netscaler/netscaler-helm-charts/blob/master/citrix-node-controller/values.yaml) contains the default values of the parameters.

## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:

```
   helm delete my-release
```
The command removes all the Kubernetes components associated with the chart and deletes the release.

## Related documentation

-  [NetScaler node controller Documentation](https://github.com/netscaler/netscaler-k8s-node-controller)
