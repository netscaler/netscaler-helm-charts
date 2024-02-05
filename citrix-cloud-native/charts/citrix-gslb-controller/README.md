# NetScaler GSLB Controller  

[NetScaler](https://www.netscaler.com) provides a GSLB controller and load balancing solution which globally monitors applications, collect, and share metrics across different clusters, and provides intelligent load balancing decisions. It ensures better performance and reliability for your Kubernetes applications.[NetScaler GSLB controller](https://github.com/netscaler/netscaler-k8s-ingress-controller/tree/master/gslb) is the module responsible for the configuration of the NetScaler GSLB devices. 

## TL;DR;

### For Kubernetes
   ```
   helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

   helm install gslb-controller netscaler/citrix-cloud-native --set gslb.enabled=true,gslb.localRegion=<local-cluster-region>,gslb.localCluster=<local-cluster-name>,gslb.sitedata[0].siteName=<site1-name>,gslb.sitedata[0].siteIp=<site1-ip-address>,gslb.sitedata[0].secretName=<site1-login-file>,gslb.sitedata[0].siteRegion=<site1-region-name>,gslb.sitedata[1].siteName=<site2-name>,gslb.sitedata[1].siteIp=<site2-ip-address>,gslb.sitedata[1].secretName=<site2-login-file>,gslb.sitedata[1].siteRegion=<site2-region-name>,gslb.license.accept=yes
   ```

   To install NetScaler Provided Custom Resource Definition(CRDs) along with NetScaler Ingress Controller
   ```
   helm install gslb-controller netscaler/citrix-cloud-native --set gslb.enabled=true,gslb.localRegion=<local-cluster-region>,gslb.localCluster=<local-cluster-name>,gslb.sitedata[0].siteName=<site1-name>,gslb.sitedata[0].siteIp=<site1-ip-address>,gslb.sitedata[0].secretName=<site1-login-file>,gslb.sitedata[0].siteRegion=<site1-region-name>,gslb.sitedata[1].siteName=<site2-name>,gslb.sitedata[1].siteIp=<site2-ip-address>,gslb.sitedata[1].secretName=<site2-login-file>,gslb.sitedata[1].siteRegion=<site2-region-name>,gslb.license.accept=yes,gslb.crds.install=true
   ```

### For OpenShift

   ```
   helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

   helm install gslb-controller netscaler/citrix-cloud-native --set gslb.enabled=true,gslb.localRegion=<local-cluster-region>,gslb.localCluster=<local-cluster-name>,gslb.sitedata[0].siteName=<site1-name>,gslb.sitedata[0].siteIp=<site1-ip-address>,gslb.sitedata[0].secretName=<site1-login-file>,gslb.sitedata[0].siteRegion=<site1-region-name>,gslb.sitedata[1].siteName=<site2-name>,gslb.sitedata[1].siteIp=<site2-ip-address>,gslb.sitedata[1].secretName=<site2-login-file>,gslb.sitedata[1].siteRegion=<site2-region-name>,gslb.license.accept=yes,gslb.openshift=true
   ```

  To install NetScaler Provided Custom Resource Definition(CRDs) along with NetScaler Ingress Controller
  ```
   helm install gslb-controller netscaler/citrix-cloud-native --set gslb.enabled=true,gslb.localRegion=<local-cluster-region>,gslb.localCluster=<local-cluster-name>,gslb.sitedata[0].siteName=<site1-name>,gslb.sitedata[0].siteIp=<site1-ip-address>,gslb.sitedata[0].secretName=<site1-login-file>,gslb.sitedata[0].siteRegion=<site1-region-name>,gslb.sitedata[1].siteName=<site2-name>,gslb.sitedata[1].siteIp=<site2-ip-address>,gslb.sitedata[1].secretName=<site2-login-file>,gslb.sitedata[1].siteRegion=<site2-region-name>,gslb.license.accept=yes,gslb.openshift=true,gslb.crds.install=true
  ```
> **Important:**
>
> The `license.accept` argument is mandatory. Ensure that you set the value as `yes` to accept the terms and conditions of the NetScaler license.

## Introduction
This Helm chart deploys NetScaler GSLB controller in the [Kubernetes](https://kubernetes.io) or in the [Openshift](https://www.openshift.com) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version 1.16 or later if using Kubernetes environment.
-  The [Openshift](https://www.openshift.com) version 4.8 or later if using OpenShift platform.
-  The [Helm](https://helm.sh/) version 3.x or later. You can follow instruction given [here](https://github.com/netscaler/netscaler-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.

-  The user name and password of the NetScaler VPX or MPX appliance. The NetScaler appliance needs to have system user account (non-default) with certain privileges so that NetScaler ingress controller can configure the NetScaler VPX or MPX appliance. For instructions to create the system user account on NetScaler, see [Create System User Account for NSIC in NetScaler](#create-system-user-account-for-cic-in-citrix-adc).

    You can pass user name and password using Kubernetes secrets. Create a Kubernetes secret for the user name and password using the following command:

    ```
       kubectl create secret generic nslogin --from-literal=username='cic' --from-literal=password='mypassword'
    ```
    - The secrets with credentials needs to be created for all the NetScaler Nodes.

- Following configurations needs to be done on the NetScaler's for manually provisioning GSLB sites
  - Add a SNIP (The subnet IP address). For more information, see [IP Addressing in NetScaler](https://docs.netscaler.com/en-us/citrix-adc/current-release/networking/ip-addressing.html).
    ```
    add ip <snip> <netmask>
    ```
  - GSLB sites needs to be configured on all the NetScaler which acts as the GSLB Node.
    ```
    add gslb site <sitename> <snip>
    ```
  - Features like content switching(CS),Load Balancing(LB), SSL, GSLB should be enabled on all the NetScaler Nodes
    ```
    en feature lb,cs,ssl,gslb

- Above configurations can be automated by the controller by supplying additional parameters
  - Use the following additional parameters:
     ```
      --set nsIP=<NSIP>,gslb.adcCredentialSecret=<Secret-for-NetScaler-credentials>
     ```
     Example:
     ```
     helm install gslb-controller netscaler/citrix-cloud-native --set gslb.enabled=true,gslb.localRegion=<local-cluster-region>,gslb.localCluster=<local-cluster-name>,gslb.sitedata[0].siteName=<site1-name>,gslb.sitedata[0].siteIp=<site1-ip-address>,gslb.sitedata[0].secretName=<site1-login-file>,gslb.sitedata[0].siteRegion=<site1-region-name>,gslb.sitedata[1].siteName=<site2-name>,gslb.sitedata[1].siteIp=<site2-ip-address>,gslb.sitedata[1].secretName=<site2-login-file>,gslb.sitedata[1].siteRegion=<site2-region-name>,gslb.license.accept=yes,gslb.crds.install=true,gslb.adcCredentialSecret=<Secret-for-NetScaler-credentials> --set nsIP=<NSIP>
     ```
  -  You determine the NS_IP IP address needed by the controller to communicate with NetScaler. The IP address might be anyone of the following depending on the type of NetScaler deployment:

   -  (Standalone appliances) NSIP - The management IP address of a standalone NetScaler appliance. For more information, see [IP Addressing in NetScaler](https://docs.netscaler.com/en-us/citrix-adc/current-release/networking/ip-addressing.html).

    -  (Appliances in High Availability mode) SNIP - The subnet IP address. For more information, see [IP Addressing in NetScaler](https://docs.netscaler.com/en-us/citrix-adc/current-release/networking/ip-addressing.htmlddressing.htmlddressing.htmlddressing.htmlddressing.html).

    -  (Appliances in Clustered mode) CLIP - The cluster management IP (CLIP) address for a clustered NetScaler deployment. For more information, see [IP addressing for a cluster](https://docs.netscaler.com/en-us/citrix-adc/current-release/clustering/cluster-overview/ip-addressing.html).

- For static proximity, the location database has to be applied externally
    ```
    add locationfile /var/netscaler/inbuilt_db/Citrix_Netscaler_InBuilt_GeoIP_DB_IPv4
    ```
#### Create system User account for NetScaler ingress controller in NetScaler

NetScaler ingress controller configures the NetScaler using a system user account of the NetScaler. The system user account should have certain privileges so that the NSIC has permission configure the following on the NetScaler:

-  Add, Delete, or View Content Switching (CS) virtual server
-  Add, Delete, or View GSLB virtual server
-  Configure CS policies and actions
-  Configure Load Balancing (LB) virtual server
-  Configure Service groups
-  Configure user monitors
-  Check the status of the NetScaler appliance

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
Add the NetScaler GSLB Controller Controller helm chart repository using command:

```
   helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/
```

### For Kubernetes:
#### 1. NetScaler GSLB Controller Controller
To install the chart with the release name, `my-release`, use the following command:
   ```
   helm install my-release netscaler/citrix-cloud-native --set gslb.enabled=true,gslb.localRegion=<local-cluster-region>,gslb.localCluster=<local-cluster-name>,gslb.sitedata[0].siteName=<site1-name>,gslb.sitedata[0].siteIp=<site1-ip-address>,gslb.sitedata[0].secretName=<site1-login-file>,gslb.sitedata[0].siteRegion=<site1-region-name>,gslb.sitedata[1].siteName=<site2-name>,gslb.sitedata[1].siteIp=<site2-ip-address>,gslb.sitedata[1].secretName=<site2-login-file>,gslb.sitedata[1].siteRegion=<site2-region-name>,gslb.license.accept=yes

   ```

> **Note:**
>
> By default the chart installs the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and role bindings.

The command deploys NetScaler GSLB Controller controller on Kubernetes cluster with the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

### For Openshift:
#### 1. NetScaler GSLB Controller Controller
Add the service account named "mcingress-k8s-role" to the privileged Security Context Constraints of OpenShift:

   ```
   oc adm policy add-scc-to-user privileged system:serviceaccount:<namespace>:mcingress-k8s-role
   ```

To install the chart with the release name, `my-release`, use the following command:
   ```
   helm install my-release netscaler/citrix-cloud-native --set gslb.enabled=true,gslb.localRegion=<local-cluster-region>,gslb.localCluster=<local-cluster-name>,gslb.sitedata[0].siteName=<site1-name>,gslb.sitedata[0].siteIp=<site1-ip-address>,gslb.sitedata[0].secretName=<site1-login-file>,gslb.sitedata[0].siteRegion=<site1-region-name>,gslb.sitedata[1].siteName=<site2-name>,gslb.sitedata[1].siteIp=<site2-ip-address>,gslb.sitedata[1].secretName=<site2-login-file>,gslb.sitedata[1].siteRegion=<site2-region-name>,gslb.license.accept=yes,gslb.openshift=true
   ```

The command deploys NetScaler GSLB Controller controller on your Openshift cluster in the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

### Installed components

The following components are installed:

-  [NetScaler Ingress controller](https://github.com/netscaler/netscaler-k8s-ingress-controller) running as GSLB Controller


## CRDs configuration

CRDs can be installed/upgraded automatically when we install/upgrade NetScaler GSLB Controller controller using parameter `crds.install=true` in Helm. If you do not want to install CRDs, then set the option `crds.install` to `false`. By default, CRDs too get deleted if you uninstall through Helm. This means, even the CustomResource objects created by the customer will get deleted. If you want to avoid this data loss set `crds.retainOnDelete` to `true`.

> **Note:**
> Installing again may fail due to the presence of CRDs. Make sure that you back up all CustomResource objects and clean up CRDs before re-installing NetScaler GSLB Controller Controller.

There are a few examples of how to use these CRDs, which are placed in the folder: [Example-CRDs](https://github.com/netscaler/netscaler-helm-charts/tree/master/example-crds). Refer to them and install as needed, using the following command:
```kubectl create -f <crd-example.yaml>```


### Resource Quotas
There are various use-cases when resource quotas are configured on the Kubernetes cluster. If quota is enabled in a namespace for compute resources like cpu and memory, users must specify requests or limits for those values; otherwise, the quota system may reject pod creation. The resource quotas for the GSLB controller containers can be provided explicitly in the helm chart.

To set requests and limits for the GSLB controller container, use the variables `gslb.resources.requests` and `gslb.resources.limits` respectively.

Below is an example of the helm command that configures
- For GSLB Controller container:
```
  CPU request for 500milli CPUs
  CPU limit at 1000m
  Memory request for 512M
  Memory limit at 1000M
```
```
helm install my-release netscaler/citrix-cloud-native --set gslb.enabled=true,gslb.localRegion=<local-cluster-region>,gslb.localCluster=<local-cluster-name>,gslb.sitedata[0].siteName=<site1-name>,gslb.sitedata[0].siteIp=<site1-ip-address>,gslb.sitedata[0].secretName=<site1-login-file>,gslb.sitedata[0].siteRegion=<site1-region-name>,gslb.sitedata[1].siteName=<site2-name>,gslb.sitedata[1].siteIp=<site2-ip-address>,gslb.sitedata[1].secretName=<site2-login-file>,gslb.sitedata[1].siteRegion=<site2-region-name>,gslb.license.accept=yes --set gslb.resources.requests.cpu=500m,gslb.resources.requests.memory=512Mi --set gslb.resources.limits.cpu=1000m,gslb.resources.limits.memory=1000Mi
```

### Configuration

The following table lists the mandatory and optional parameters that you can configure during installation:

| Parameters | Mandatory or Optional | Default value | Description |
| --------- | --------------------- | ------------- | ----------- |
| gslb.license.accept | Mandatory | no | Set `yes` to accept the NSIC end user license agreement. |
| gslb.imageRegistry                   | Optional  |  `quay.io`               |  The NetScaler ingress controller image registry             |  
| gslb.imageRepository                 | Optional  |  `citrix/citrix-k8s-ingress-controller`              |   The NetScaler ingress controller image repository             | 
| gslb.imageTag                  | Optional  |  `1.38.27`               |   The NetScaler ingress controller image tag            | 
| gslb.pullPolicy | Optional | Always | The NSIC image pull policy. |
| gslb.adcCredentialSecret | Optional | N/A | The kubernetes secret containing login credentials for the NetScaler VPX or MPX. For information on how to create the secret keys, see [Prerequisites](#prerequistes). |
| gslb.secretStore.enabled | Optional | False | Set to "True" for deploying other Secret Provider classes  |
| gslb.secretStore.username | Optional | N/A | if `gslb.secretStore.enabled`, `username` of NetScaler will be fetched from the Secret Provider  |
| gslb.secretStore.password | Optional | N/A | if `gslb.secretStore.enabled`, `password` of NetScaler will be fetched from the Secret Provider  |
| gslb.nsIP | Optional | N/A | The IP address of the NetScaler device. For details, see [Prerequisites](#prerequistes). |
| gslb.nsPort | Optional | 443 | The port used by NSIC to communicate with NetScaler. You can use port 80 for HTTP. |
| gslb.nsProtocol | Optional | HTTPS | The protocol used by NSIC to communicate with NetScaler. You can also use HTTP on port 80. |
| gslb.nitroReadTimeout | Optional | 20 | The nitro Read timeout in seconds, defaults to 20 |
| gslb.logLevel | Optional | INFO | The loglevel to control the logs generated by NSIC. The supported loglevels are: CRITICAL, ERROR, WARNING, INFO, DEBUG and TRACE. For more information, see [Logging](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/configure/log-levels.md).|
| gslb.disableAPIServerCertVerify | Optional | False | Set this parameter to True for disabling API Server certificate verification. |
| gslb.kubernetesURL | Optional | N/A | The kube-apiserver url that NSIC uses to register the events. If the value is not specified, NSIC uses the [internal kube-apiserver IP address](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/#accessing-the-api-from-a-pod). |
| gslb.entityPrefix | Optional | k8s | The prefix for the resources on the NetScaler VPX/MPX. |
| gslb.openshift | Optional | false | Set this argument if OpenShift environment is being used. |
| gslb.localRegion | Mandatory | N/A | The region where this controller is deployed. |
| gslb.localCluster | Mandatory | N/A | The Cluster Name where this controller is deployed. |
| gslb.sitedata | Mandatory | N/A | The list containing NetScaler Site details like IP, Name, Region, Secret |
| gslb.sitedata[0].siteName | Mandatory | N/A | The siteName of the first GSLB site |
| gslb.sitedata[0].siteIp | Mandatory | N/A | The siteIp of the first GSLB Site |
| gslb.sitedata[0].siteMask | Optional | "255.255.255.0" | The netmask of the first GSLB Site IP|
| gslb.sitedata[0].secretName | Mandatory | N/A | The secret containing login credentials of first site |
| gslb.sitedata[0].siteRegion | Mandatory | N/A | The SiteRegion of the first site |
| gslb.sitedata[0].sitePublicip | Optional | siteIp | The site public IP of the first GSLB Site |
| gslb.crds.install | Optional | False | Unset this argument if you don't want to install CustomResourceDefinitions which are consumed by NSIC. |
| gslb.crds.retainOnDelete | Optional | false | Set this argument if you want to retain CustomResourceDefinitions even after uninstalling NSIC. This will avoid data-loss of Custom Resource Objects created before uninstallation. |

Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

For example:
   ```
   helm install my-release netscaler/citrix-cloud-native -f values.yaml
   ```

Your values.yaml should look something like this:
   ```
   gslb.license:
      accept: yes

   gslb.localRegion: "east"
   gslb.localCluster: "cluster1"

   gslb.entityPrefix: "k8s"

   gslb.sitedata:
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

- [NetScaler GSLB controller Documentation](https://docs.netscaler.com/en-us/citrix-k8s-ingress-controller/gslb/gslb.html)
- [NetScaler GSLB Controller controller GitHub](https://github.com/netscaler/netscaler-k8s-ingress-controller/tree/master/gslb)
