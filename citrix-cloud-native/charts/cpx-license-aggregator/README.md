# NetScaler CPX License Aggregator

NetScaler CPX license aggregator reserves bulk license capacity for given cluster from License server and license the NetScaler CPX deployed in a Kubernetes Cluster.


## TL;DR;

   ```
   helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/
   ```

### 1 Installing NetScaler CPX License Aggregator to serve Pooled Licenses

#### 1.1 For Platinum Bandwidth Edition

   ```
   helm install demo netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.instanceQuantum=<QUANTUM>,cla.licenseInfo.instanceLowWatermark=<LOW WATERMARK>,cla.licenseInfo.bandwidthPlatinumQuantum=<QUANTUM-in-Mbps>,cla.licenseInfo.bandwidthPlatinumLowWatermark=<LLOW WATERMARK-in-Mbps>
   ```

#### 1.2 For Enterprise Bandwidth Edition

   ```
   helm install demo netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.instanceQuantum=<QUANTUM>,cla.licenseInfo.instanceLowWatermark=<LOW WATERMARK>,cla.licenseInfo.bandwidthEnterpriseQuantum=<QUANTUM-in-Mbps>,cla.licenseInfo.bandwidthEnterpriseLowWatermark=<LOW WATERMARK-in-Mbps>
   ```

#### 1.3 For Standard Bandwidth Edition

   ```
   helm install demo netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.instanceQuantum=<QUANTUM>,cla.licenseInfo.instanceLowWatermark=<LOW WATERMARK>,cla.licenseInfo.bandwidthStandardQuantum=<QUANTUM-in-Mbps>,cla.licenseInfo.bandwidthStandardLowWatermark=<LOW WATERMARK-in-Mbps>
   ```

### Installing NetScaler CPX License Aggregator to serve VCPU Licenses

#### 2.1 For Platinum VCPU Edition

   ```
   helm install demo netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.vcpuPlatinumQuantum=<QUANTUM>,cla.licenseInfo.vcpuPlatinumLowWatermark=<LOW WATERMARK>
   ```

#### 2.2 For Enterprise VCPU Edition
   
   ```
   helm install demo netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.vcpuEnterpriseQuantum=<QUANTUM>,cla.licenseInfo.vcpuEnterpriseLowWatermark=<LOW WATERMARK>
   ```

#### 2.3 For Standard VCPU Edition

   ```
   helm install demo netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.vcpuStandardQuantum=<QUANTUM>,cla.licenseInfo.vcpuStandardLowWatermark=<LOW WATERMARK>
   ```

> **Note:**
>
> In the above command, username represents the handler of license aggregator. In the ADM license server, the details of this instance of CPX License Aggregator would be associated with the provided username.

>Above commands deploy CPX License Aggregator for a particular type of license. If multiple types of licenses need to be managed by CLA, then relevant arguments of those licenses should be specified in the helm command.
For example, to deploy CLA for "Pooled Platinum Bandwidth Edition" and "vCPU Platinum Edition" licenses, below command should be fired.

   ```
   helm install demo netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.instanceQuantum=<QUANTUM>,cla.licenseInfo.instanceLowWatermark=<LOW WATERMARK>,cla.licenseInfo.bandwidthPlatinumQuantum=<QUANTUM-in-Mbps>,cla.licenseInfo.bandwidthPlatinumLowWatermark=<LOW WATERMARK-in-Mbps>,cla.licenseInfo.vcpuPlatinumQuantum=<QUANTUM>,cla.licenseInfo.vcpuPlatinumLowWatermark=LOW WATERMARKs>
   ```

## Introduction
This Helm chart deploys NetScaler CPX License Aggregator in the [Kubernetes](https://kubernetes.io) or in the [Openshift](https://www.openshift.com) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

- The [Kubernetes](https://kubernetes.io/) version should be 1.16 and above if using Kubernetes environment.
- The [Openshift](https://www.openshift.com) version 4.8 or later if using OpenShift platform.
- The [Helm](https://helm.sh/) version 3.x or later. You can follow instruction given [here](https://github.com/netscaler/netscaler-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.
- You determine the address (IP or FQDN) of the NetScaler ADM License Server having license for NetScaler CPX.
- You need to provide password that will be used for the Redis DB in CLA. You can provide DB password using Kubernetes secret and following command can be used to create the secret:

    kubectl create secret generic dbsecret --from-literal=password=<DB-Password> -n <namespaceName>

## Installing the Chart
Add the NetScaler CPX License Aggregator helm chart repository using command:

```
   helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/
```

To install the chart with the release name, `my-release`, use the following command:

### 1 Installing NetScaler CPX License Aggregator to serve Pooled Licenses

#### 1.1 For Platinum Bandwidth Edition

   ```
   helm install my-release netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.instanceQuantum=<QUANTUM>,cla.licenseInfo.instanceLowWatermark=<LOW WATERMARK>,cla.licenseInfo.bandwidthPlatinumQuantum=<QUANTUM-in-Mbps>,cla.licenseInfo.bandwidthPlatinumLowWatermark=<LOW WATERMARK-in-Mbps>
   ```

#### 1.2 For Enterprise Bandwidth Edition

   ```
   helm install my-release netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.instanceQuantum=<QUANTUM>,cla.licenseInfo.instanceLowWatermark=<LOW WATERMARK>,cla.licenseInfo.bandwidthEnterpriseQuantum=<QUANTUM-in-Mbps>,cla.licenseInfo.bandwidthEnterpriseLowWatermark=<LOW WATERMARK-in-Mbps>
   ```

#### 1.3 For Standard Bandwidth Edition

   ```
   helm install my-release netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.instanceQuantum=<QUANTUM>,cla.licenseInfo.instanceLowWatermark=<LOW WATERMARK>,cla.licenseInfo.bandwidthStandardQuantum=<QUANTUM-in-Mbps>,cla.licenseInfo.bandwidthStandardLowWatermark=<LOW WATERMARK-in-Mbps
   ```

### Installing NetScaler CPX License Aggregator to serve VCPU Licenses

#### 2.1 For Platinum VCPU Edition

   ```
   helm install my-release netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.vcpuPlatinumQuantum=<QUANTUM>,cla.licenseInfo.vcpuPlatinumLowWatermark=<LOW WATERMARK>
   ```

#### 2.2 For Enterprise VCPU Edition
   
   ```
   helm install my-release netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.vcpuEnterpriseQuantum=<QUANTUM>,cla.licenseInfo.vcpuEnterpriseLowWatermark=<LOW WATERMARK>
   ```

#### 2.3 For Standard VCPU Edition

   ```
   helm install my-release netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.vcpuStandardQuantum=<QUANTUM>,cla.licenseInfo.vcpuStandardLowWatermark=<LOW WATERMARK>
   ```

> **Note:**
> In the above command, username represents the handler of license aggregator. In the ADM license server, the details of this instance of CPX License Aggregator would be associated with the provided username.

>Above commands deploy CPX License Aggregator for a particular type of license. If multiple types of licenses need to be managed by CLA, then relevant arguments of those licenses should be specified in the helm command.
For example, to deploy CLA for "Pooled Platinum Bandwidth Edition" and "vCPU Platinum Edition" licenses, below command should be fired.

   ```
   helm install demo netscaler/cpx-license-aggregator --set cla.licenseServer.address=<License-Server-IP-or-FQDN>,cla.redis.secretName=<Kubernetes-Secret-for-DB-password>,cla.licenseAggregator.username=<unique-ID-for-CLA>,cla.licenseInfo.instanceQuantum=<QUANTUM>,cla.licenseInfo.instanceLowWatermark=<LOW WATERMARK>,cla.licenseInfo.bandwidthPlatinumQuantum=<QUANTUM-in-Mbps>,cla.licenseInfo.bandwidthPlatinumLowWatermark=<LOW WATERMARK-in-Mbps>,cla.licenseInfo.vcpuPlatinumQuantum=<QUANTUM>,cla.licenseInfo.vcpuPlatinumLowWatermark=LOW WATERMARK>
   ```

> By default the chart installs the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and role bindings.

The command deploys NetScaler CPX License Aggregator on Kubernetes cluster with the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

### Configuration

The following table lists the mandatory and optional parameters that you can configure during installation:

| Parameters | Mandatory or Optional | Default value | Description |
| --------- | --------------------- | ------------- | ----------- |
| cla.licenseAggregator.imageRegistry                   | Mandatory  |  `quay.io`               |  The CLA image registry             |  
| cla.licenseAggregator.imageRepository                 | Mandatory  |  `citrix/cpx-license-aggregator`              |   The CLA image repository             | 
| cla.licenseAggregator.imageTag                  | Mandatory  |  `1.0.0`               |  The CLA image tag            | 
| cla.licenseAggregator.pullPolicy | Mandatory | IfNotPresent | The CLA image pull policy. |
| cla.licenseAggregator.service.type | Mandatory | NodePort | Type of service used to expose CLA. |
| cla.licenseAggregator.service.nodePort | Optional | N/A | The port on the cluster node to be used to expose CLA service if the type of CLA service is NodePort. Make sure the parameter `licenseAggregator.service.type` has value `NodePort` for using this option. |
| cla.licenseAggregator.username | Mandatory | N/A | Please provide the username/clustername that can uniquely identify this license aggregator service with the NetScaler ADM License server. CLA would register itself with <username>.<servicename>.<namespace> with the NetScaler ADM. It helps NetScaler ADM in keeping track of various License Aggregator instances. |
| cla.licenseAggregator.securityContext |  Optional | N/A | Security context for license-aggregator container. |
| cla.licenseAggregator.resources | Optional | N/A | Resouces restrictions for license-aggregator container. |
| cla.licenseAggregator.loglevel | Optional | INFO | Log level of the CLA service. Default value: INFO. Possible values: TRACE, DEBUG, INFO, WARN, ERROR |
| cla.licenseAggregator.jsonlog | Optional | FALSE | Logs to be generated in the JSON format. Default: False. Possible values: TRUE, FALSE |
| cla.nslped.image | Mandatory | quay.io/citrix/nslped:1.0.0 | The nslped image. |
| cla.nslped.imageRegistry                   | Mandatory  |  `quay.io`               |  The nslped image registry             |  
| cla.nslped.imageRepository                 | Mandatory  |  `citrix/nslped`              |   The nslped image repository             | 
| cla.nslped.imageTag                  | Mandatory  |  `1.0.0`               |  The nslped image tag            | 
| cla.nslped.pullPolicy | Mandatory | IfNotPresent | The nslped image pull policy. |
| cla.nslped.securityContext |  Optional | N/A | Security context for nslped container. |
| cla.nslped.resources | Optional | N/A | Resouces restrictions for nslped container. |
| cla.redis.image | Mandatory | redis:7.0.4 | The redis image. |
| cla.redis.pullPolicy | Mandatory | IfNotPresent | The redis image pull policy. |
| cla.redis.secretName | Mandatory | N/A | Kubernetes secret name created for Redis DB password. |
| cla.redis.securityContext |  Optional | N/A | Security context for redis container. |
| cla.redis.resources | Optional | N/A | Resouces restrictions for redis container. |
| cla.sidecarCertsGenerator.imageRegistry                | Mandatory | `quay.io`               | The sidecarCertsGenerator image registry |
| cla.sidecarCertsGenerator.imageRepository              | Mandatory | `citrix/cpx-sidecar-injector-certgen`               |  The sidecarCertsGenerator image repository             |
| cla.sidecarCertsGenerator.imageTag                     | Mandatory | `1.2.0`               |  The sidecarCertsGenerator image tag |
| cla.sidecarCertsGenerator.pullPolicy | Mandatory | IfNotPresent | The sidecarCertsGenerator image pull policy. |
| cla.serviceAccount.annotations |  Optional | N/A | Annotations to be used for serviceaccount that is being used by CLA. |
| cla.licenseServer.address | Mandatory | N/A | IP or FQDN of License Server. |
| cla.licenseServer.port | Mandatory | 27000 | Port to be used for making connection to License Server. |
| cla.licenseInfo.instanceQuantum | Optional | 0 | Quantum of Instance licenses to be checked-out from license server. |
| cla.licenseInfo.instanceLowWatermark | Optional | 0 | If available instance licenses fall below this watermark, check-out additional license-quantum. |
| cla.licenseInfo.bandwidthPlatinumQuantum | Optional | 0 | Quantum of Platinum category bandwidth throughput to be checked out from license server in Mbps. |
| cla.licenseInfo.bandwidthPlatinumLowWatermark | Optional | 0 |If available Platinum category bandwidth (Mbps) licenses fall below this watermark, check-out additional license-quantum. |
| cla.licenseInfo.bandwidthEnterpriseQuantum | Optional | 0 | Quantum of Enterprise category bandwidth throughput to be checked out from license server in Mbps. |
| cla.licenseInfo.bandwidthEnterpriseLowWatermark | Optional | 0 | If available Enterprise category bandwidth (Mbps) licenses fall below this watermark, check-out additional license-quantum.|
| cla.licenseInfo.bandwidthStandardQuantum | Optional | 0 | Quantum of Standard category vCPU licenses to be checked-out from license server. |
| cla.licenseInfo.bandwidthStandardLowWatermark | Optional | 0 | If available Standard category bandwidth (Mbps) licenses fall below this watermark, check-out additional license-quantum. |
| cla.licenseInfo.vcpuPlatinumQuantum | Optional | 0 | Quantum of Platinum category vCPU licenses to be checked-out from license server. |
| cla.licenseInfo.vcpuPlatinumLowWatermark | Optional | 0 | If available Platinum category vCPU licenses fall below this watermark, check-out additional license-quantum. |
| cla.licenseInfo.vcpuEnterpriseQuantum | Optional | 0 | Quantum of Enterprise category vCPU licenses to be checked-out from license server. |
| cla.licenseInfo.vcpuEnterpriseLowWatermark | Optional | 0 | If available Enterprise category vCPU licenses fall below this watermark, check-out additional license-quantum.|
| cla.licenseInfo.vcpuStandardQuantum | Optional | 0 | Quantum of Standard category vCPU licenses to be checked-out from license server. |
| cla.licenseInfo.vcpuStandardLowWatermark | Optional | 0 | If available Standard category vCPU licenses fall below this watermark, check-out additional license-quantum. |
| cla.licenseInfo.dbExpireTime | Mandatory | 172800 | Time to keep NetScaler CPX data in Redis DB without any heartbeat from NetScaler CPX in seconds. |
| cla.adcInfo.selectorLabel.key | Mandatory | adc | CLA will use this as key in the selector label for monitoring NetScaler CPX pod. |
| cla.adcInfo.selectorLabel.value | Mandatory | citrix | CLA will use this as value in the selector label for monitoring NetScaler CPX pod. |
| cla.podAnnotations | Optional | N/A | Annotation to be used in CLA pod. |
| cla.podSecurityContext | Optional | N/A | Security Context to be used for CLA pod. |
| cla.nodeSelector | Optional | N/A | Node selector to be used for CLA pod. |
| cla.tolerations | Optional | N/A | Tolerations to be used for CLA pod. |
| cla.affinity | Optional | N/A | Node Affinity to be used for CLA pod. |
| cla.imagePullSecrets | Optional | N/A | Provide list of Kubernetes secrets to be used for pulling the images from a private Docker registry or repository. For more information on how to create this secret please see [Pull an Image from a Private Registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/). |

Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

For example:
   ```
   helm install my-release netscaler/citrix-cloud-native -f values.yaml
   ```

> **Tip:**
>
> The [values.yaml](https://github.com/netscaler/netscaler-helm-charts/blob/master/citrix_cloud_native_values.yaml) contains the default values of the parameters.

### NetScaler CPX License Aggregator Services:

1. To see the CLA stats use the following URL in the browser:

   `https://<K8s-node-ip>:<cla-svc-nodeport>/stats`

2. To see the NetScaler CPX information running in the cluster use the following URL in the browser:

   `https://<NodeIP:Nodeport>/cpxinfo`
   > **Note:** HTTP request to this URL must contain HTTP header named x-cla with value 1.0.0

## Uninstalling the Chart
We are using persistent volume for CLA to store and retain the Licensed NetScaler CPX information in case of any failures. As part of Helm install one persistent volume claim get created for the stateful set which needs to be deleted manually afterwards.
 
So, to uninstall the chart with release name `my-release`:

1. Uninstall/delete the `my-release` deployment:
   ```
   helm delete my-release
   ```
2. Delete the pvc:
   ```
   kubectl delete pvc data-my-release-citrix-cloud-native-0 -n <Release-Namespace>
   ```

The command removes all the Kubernetes components associated with the chart and deletes the release.
