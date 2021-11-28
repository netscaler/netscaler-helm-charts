# Citrix Multi-Cluster Ingress Controller  

[Citrix](https://www.citrix.com/en-in/) provides a multi-cluster ingress and load balancing solution which globally monitors applications, collect, and share metrics across different clusters, and provides intelligent load balancing decisions. It ensures better performance and reliability for your Kubernetes applications.[Multi-Cluster Ingress controller](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/multicluster) is the module responsible for the configuration of the Citrix ADC GSLB devices. 

## TL;DR;

### For Kubernetes
   ```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/

   helm install multi-cluster citrix/citrix-cloud-native --set mcIngress.localRegion=<local-cluster-region>,mcIngress.localCluster=<local-cluster-name>,mcIngress.sitedata[0].siteName=<site1-name>,mcIngress.sitedata[0].siteIp=<site1-ip-address>,mcIngress.sitedata[0].secretName=<site1-login-file>,mcIngress.sitedata[1].siteName=<site2-name>,mcIngress.sitedata[1].siteIp=<site2-ip-address>,mcIngress.sitedata[1].secretName=<site2-login-file>,mcIngress.license.accept=yes
   ```

   To install Citrix Provided Custom Resource Definition(CRDs) along with Citrix Ingress Controller
   ```
   helm install multi-cluster citrix/citrix-cloud-native --set mcIngress.localRegion=<local-cluster-region>,mcIngress.localCluster=<local-cluster-name>,mcIngress.sitedata[0].siteName=<site1-name>,mcIngress.sitedata[0].siteIp=<site1-ip-address>,mcIngress.sitedata[0].secretName=<site1-login-file>,mcIngress.sitedata[1].siteName=<site2-name>,mcIngress.sitedata[1].siteIp=<site2-ip-address>,mcIngress.sitedata[1].secretName=<site2-login-file>,mcIngress.license.accept=yes,mcIngress.crds.install=true
   ```

### For OpenShift

   ```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/

   helm install multi-cluster citrix/citrix-cloud-native --set mcIngress.localRegion=<local-cluster-region>,mcIngress.localCluster=<local-cluster-name>,mcIngress.sitedata[0].siteName=<site1-name>,mcIngress.sitedata[0].siteIp=<site1-ip-address>,mcIngress.sitedata[0].secretName=<site1-login-file>,mcIngress.sitedata[1].siteName=<site2-name>,mcIngress.sitedata[1].siteIp=<site2-ip-address>,mcIngress.sitedata[1].secretName=<site2-login-file>,mcIngress.license.accept=yes,mcIngress.openshift=true
   ```

  To install Citrix Provided Custom Resource Definition(CRDs) along with Citrix Ingress Controller
  ```
   helm install multi-cluster citrix/citrix-cloud-native --set mcIngress.localRegion=<local-cluster-region>,mcIngress.localCluster=<local-cluster-name>,mcIngress.sitedata[0].siteName=<site1-name>,mcIngress.sitedata[0].siteIp=<site1-ip-address>,mcIngress.sitedata[0].secretName=<site1-login-file>,mcIngress.sitedata[1].siteName=<site2-name>,mcIngress.sitedata[1].siteIp=<site2-ip-address>,mcIngress.sitedata[1].secretName=<site2-login-file>,mcIngress.license.accept=yes,mcIngress.openshift=true,mcIngress.crds.install=true
  ```
> **Important:**
>
> The `license.accept` argument is mandatory. Ensure that you set the value as `yes` to accept the terms and conditions of the Citrix license.

## Introduction
This Helm chart deploys Citrix ingress controller in the [Kubernetes](https://kubernetes.io) or in the [Openshift](https://www.openshift.com) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version 1.16 or later if using Kubernetes environment.
-  The [Openshift](https://www.openshift.com) version 4.8 or later if using OpenShift platform.
-  The [Helm](https://helm.sh/) version 3.x or later. You can follow instruction given [here](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.

-  The user name and password of the Citrix ADC VPX or MPX appliance. The Citrix ADC appliance needs to have system user account (non-default) with certain privileges so that Citrix ingress controller can configure the Citrix ADC VPX or MPX appliance. For instructions to create the system user account on Citrix ADC, see [Create System User Account for CIC in Citrix ADC](#create-system-user-account-for-cic-in-citrix-adc).

    You can pass user name and password using Kubernetes secrets. Create a Kubernetes secret for the user name and password using the following command:

    ```
       kubectl create secret generic nslogin --from-literal=username='cic' --from-literal=password='mypassword'
    ```
    - The secrets with credentials needs to be created for all the ADC Nodes.

- Following configurations needs to be done on the ADC's
  - Add a SNIP (The subnet IP address). For more information, see [IP Addressing in Citrix ADC](https://docs.citrix.com/en-us/citrix-adc/12-1/networking/ip-addressing.html).
    ```
    add ip <snip> <netmask>
    ```
  - GSLB sites needs to be configured on all the Citrix ADC which acts as the GSLB Node.
    ```
    add gslb site <sitename> <snip>
    ```
  - Features like content switching(CS),Load Balancing(LB), SSL, GSLB should be enabled on all the ADC Nodes
    ```
    en feature lb,cs,ssl,gslb
    ```
  - For static proximity, the location database has to be applied externally
    ```
    add locationfile /var/netscaler/inbuilt_db/Citrix_Netscaler_InBuilt_GeoIP_DB_IPv4
    ```
#### Create system User account for Citrix ingress controller in Citrix ADC

Citrix ingress controller configures the Citrix ADC using a system user account of the Citrix ADC. The system user account should have certain privileges so that the CIC has permission configure the following on the Citrix ADC:

-  Add, Delete, or View Content Switching (CS) virtual server
-  Add, Delete, or View GSLB virtual server
-  Configure CS policies and actions
-  Configure Load Balancing (LB) virtual server
-  Configure Service groups
-  Configure user monitors
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
Add the Citrix Multi-Cluster Ingress Controller helm chart repository using command:

```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/
```

### For Kubernetes:
#### 1. Citrix Multi-Cluster Ingress Controller
To install the chart with the release name, `my-release`, use the following command:
   ```
   helm install my-release citrix/citrix-cloud-native --set mcIngress.localRegion=<local-cluster-region>,mcIngress.localCluster=<local-cluster-name>,mcIngress.sitedata[0].siteName=<site1-name>,mcIngress.sitedata[0].siteIp=<site1-ip-address>,mcIngress.sitedata[0].secretName=<site1-login-file>,mcIngress.sitedata[1].siteName=<site2-name>,mcIngress.sitedata[1].siteIp=<site2-ip-address>,mcIngress.sitedata[1].secretName=<site2-login-file>,mcIngress.license.accept=yes

   ```

> **Note:**
>
> By default the chart installs the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and role bindings.

The command deploys Citrix Multi-Cluster Ingress controller on Kubernetes cluster with the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

### For Openshift:
#### 1. Citrix Multi-Cluster Ingress Controller
Add the service account named "mcingress-k8s-role" to the privileged Security Context Constraints of OpenShift:

   ```
   oc adm policy add-scc-to-user privileged system:serviceaccount:<namespace>:mcingress-k8s-role
   ```

To install the chart with the release name, `my-release`, use the following command:
   ```
   helm install my-release citrix/citrix-cloud-native --set mcIngress.localRegion=<local-cluster-region>,mcIngress.localCluster=<local-cluster-name>,mcIngress.sitedata[0].siteName=<site1-name>,mcIngress.sitedata[0].siteIp=<site1-ip-address>,mcIngress.sitedata[0].secretName=<site1-login-file>,mcIngress.sitedata[1].siteName=<site2-name>,mcIngress.sitedata[1].siteIp=<site2-ip-address>,mcIngress.sitedata[1].secretName=<site2-login-file>,mcIngress.license.accept=yes,mcIngress.openshift=true
   ```

The command deploys Citrix Multi-Cluster Ingress controller on your Openshift cluster in the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

### Installed components

The following components are installed:

-  [Citrix Ingress controller](https://github.com/citrix/citrix-k8s-ingress-controller) running as Multi-Cluster Ingress Controller


## CRDs configuration

CRDs can be installed/upgraded automatically when we install/upgrade Citrix Multi-Cluster Ingress controller using parameter `crds.install=true` in Helm. If you do not want to install CRDs, then set the option `crds.install` to `false`. By default, CRDs too get deleted if you uninstall through Helm. This means, even the CustomResource objects created by the customer will get deleted. If you want to avoid this data loss set `crds.retainOnDelete` to `true`.

> **Note:**
> Installing again may fail due to the presence of CRDs. Make sure that you back up all CustomResource objects and clean up CRDs before re-installing Citrix Multi-Cluster Ingress Controller.

There are a few examples of how to use these CRDs, which are placed in the folder: [Example-CRDs](https://github.com/citrix/citrix-helm-charts/tree/master/example-crds). Refer to them and install as needed, using the following command:
```kubectl create -f <crd-example.yaml>```


### Configuration

The following table lists the mandatory and optional parameters that you can configure during installation:

| Parameters | Mandatory or Optional | Default value | Description |
| --------- | --------------------- | ------------- | ----------- |
| mcIngress.license.accept | Mandatory | no | Set `yes` to accept the CIC end user license agreement. |
| mcIngress.image | Optional | `quay.io/citrix/citrix-k8s-ingress-controller:1.18.5` | The CIC image. |
| mcIngress.pullPolicy | Optional | Always | The CIC image pull policy. |
| mcIngress.nsPort | Optional | 443 | The port used by CIC to communicate with Citrix ADC. You can use port 80 for HTTP. |
| mcIngress.nsProtocol | Optional | HTTPS | The protocol used by CIC to communicate with Citrix ADC. You can also use HTTP on port 80. |
| mcIngress.logLevel | Optional | DEBUG | The loglevel to control the logs generated by CIC. The supported loglevels are: CRITICAL, ERROR, WARNING, INFO, DEBUG and TRACE. For more information, see [Logging](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/log-levels.md).|
| mcIngress.kubernetesURL | Optional | N/A | The kube-apiserver url that CIC uses to register the events. If the value is not specified, CIC uses the [internal kube-apiserver IP address](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/#accessing-the-api-from-a-pod). |
| mcIngress.entityPrefix | Optional | k8s | The prefix for the resources on the Citrix ADC VPX/MPX. |
| mcIngress.openshift | Optional | false | Set this argument if OpenShift environment is being used. |
| mcIngress.localRegion | Mandatory | N/A | The region where this controller is deployed. |
| mcIngress.localCluster | Mandatory | N/A | The Cluster Name where this controller is deployed. |
| mcIngress.sitedata | Mandatory | N/A | The list containing ADC Site details like IP, Name, Region, Secret |
| mcIngress.sitedata[0].siteName | Mandatory | N/A | The siteName of the first GSLB site |
| mcIngress.sitedata[0].siteIp | Mandatory | N/A | The siteIp of the first GSLB Site |
| mcIngress.sitedata[0].secretName | Mandatory | N/A | The secret containing login credentials of first site |
| mcIngress.sitedata[0].siteRegion | Mandatory | N/A | The SiteRegion of the first site |
| mcIngress.crds.install | Optional | False | Unset this argument if you don't want to install CustomResourceDefinitions which are consumed by CIC. |
| mcIngress.crds.retainOnDelete | Optional | false | Set this argument if you want to retain CustomResourceDefinitions even after uninstalling CIC. This will avoid data-loss of Custom Resource Objects created before uninstallation. |

Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

For example:
   ```
   helm install my-release citrix/citrix-cloud-native -f values.yaml
   ```

Your values.yaml should look something like this:
   ```
   mcIngress.license:
      accept: yes

   mcIngress.localRegion: "east"
   mcIngress.localCluster: "cluster1"

   mcIngress.entityPrefix: "k8s"

   mcIngress.sitedata:
   - siteName: "site1"
     siteIp: "x.x.x.x"
     secretName: "secret1"
     siteRegion: "east"
   - siteName: "site2"
     siteIp: "x.x.x.x"
     secretName: "secret2"
     siteRegion: "west"
   ```

## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:

   ```
   helm delete my-release
   ```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Related documentation

- [Citrix Multi-Cluster Ingress controller Documentation](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/multicluster/multi-cluster/)
- [Citrix Multi-Cluster Ingress controller GitHub](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/multicluster)
