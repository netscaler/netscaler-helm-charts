# Citrix IPAM controller.

Citrix provides a controller called IPAM controller for IP address management. When you create a service of type LoadBalancer, you can use the [Citrix IPAM controller](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/) to automatically allocate an IP address to the service. Once the IPAM controller is deployed, it allocates IP address to services of type LoadBalancer from predefined IP address ranges. The [Citrix ingress controller](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/) configures the IP address allocated to the service as virtual IP (VIP) in Citrix ADC MPX or VPX.

## TL;DR;

   ```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/

   helm install ipam citrix/citrix-ipam-controller --set vipRange=<IP-address-range>
   ```

## Introduction
This Helm chart deploys a Citrix IPAM controller in the [Kubernetes](https://kubernetes.io/) or in the [Openshift](https://www.openshift.com) cluster using the [Helm](https://helm.sh/) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version is 1.6 or later if using Kubernetes environment.
-  The [Openshift](https://www.openshift.com) version 3.11.x or later if using OpenShift platform.
-  The [Helm](https://helm.sh/) version 3.x or later. You can follow instruction given [here](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.

## Installing the Chart
Add the Citrix IPAM Controller helm chart repository using command:

   ```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/
   ```

   To install the chart with the release name ``` my-release```:

   ```
   helm install my-release citrix/citrix-ipam-controller --set vipRange=<IP-address-range>
   ```

> **Note:**
>
> By default the chart installs the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and role bindings.

### Installed components

The following components are installed:

-  [Citrix IPAM Controller](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/)

## Configuration
The following table lists the configurable parameters of the Citrix ADC CPX with Citrix ingress controller as side car chart and their default values.

| Parameters | Mandatory or Optional | Default value | Description |
| ---------- | --------------------- | ------------- | ----------- |
| image | Mandatory | `quay.io/citrix/citrix-ipam-controller` | The Citrix IPAM Contoller image. |
| tag | Mandatory | `0.0.1` | The Citrix IPAM Contoller image tag. |
| pullPolicy | Mandatory | `IfNotPresent` | The Citrix IPAM Contoller image pull policy. |
| vipRange | Mandatory | N/A | This variable allows you to define the IP address range. You can either define IP address range or an IP address range associated with a unique name. Citrix IPAM controller assigns the IP address from this IP address range to the service of type LoadBalancer. |

Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

For example:
   ```
   helm install my-release citrix/citrix-ipam-controller -f values.yaml
   ```

> **Tip:**
>
> The [values.yaml](https://github.com/citrix/citrix-helm-charts/blob/master/citrix-ipam-controller/values.yaml) contains the default values of the parameters.

## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:
   ```
   helm delete my-release
   ```

## Related documentation

- [Service Type LoadBalancer Documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/network/type_loadbalancer/)
- [Citrix ingress controller Documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/)
- [Citrix ingress controller GitHub](https://github.com/citrix/citrix-k8s-ingress-controller)
