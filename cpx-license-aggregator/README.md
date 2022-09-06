# Citrix ADC CPX License Aggregator

Citrix ADC CPX license aggregator reserves bulk license capacity for given cluster from License server and license the Citrix ADC CPX deployed in a Kubernetes Cluster.


## TL;DR;

   ```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/

   helm install demo citrix/cpx-license-aggregator --set licenseServer.address=<License-Server-IP-or-FQDN>,redis.secretName=<Kubernetes-Secret-for-DB-password>,licenseAggregator.username=<unique-ID-for-CLA>
   ```

> **Note:**
>
> In the above command, username represents the handler of license aggregator. In the ADM license server, the details of this instance of CPX License Aggregator would be associated with the provided username.

## Introduction
This Helm chart deploys Citrix ADC CPX License Aggregator in the [Kubernetes](https://kubernetes.io) or in the [Openshift](https://www.openshift.com) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

- The [Kubernetes](https://kubernetes.io/) version should be 1.16 and above if using Kubernetes environment.
- The [Openshift](https://www.openshift.com) version 4.8 or later if using OpenShift platform.
- The [Helm](https://helm.sh/) version 3.x or later. You can follow instruction given [here](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.
- You determine the address (IP or FQDN) of the Citrix ADM License Server having license for Citrix ADC CPX.
- You need to provide password that will be used for the Redis DB in CLA. You can provide DB password using Kubernetes secret and following command can be used to create the secret:

    kubectl create secret generic dbsecret --from-literal=password=<DB-Password> -n <namespaceName>

## Installing the Chart
Add the Citrix ADC CPX License Aggregator helm chart repository using command:

```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/
```

To install the chart with the release name, `my-release`, use the following command:
   ```
   helm install my-release citrix/cpx-license-aggregator --set licenseServer.address=<License-Server-IP-or-FQDN>,redis.secretName=<Kubernetes-Secret-for-DB-password>,licenseAggregator.username=<unique-ID-for-CLA>
   ```

> **Note:**
>
> By default the chart installs the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and role bindings.

The command deploys Citrix ADC CPX License Aggregator on Kubernetes cluster with the default configuration. The [configuration](#configuration) section lists the mandatory and optional parameters that you can configure during installation.

### Configuration

The following table lists the mandatory and optional parameters that you can configure during installation:

| Parameters | Mandatory or Optional | Default value | Description |
| --------- | --------------------- | ------------- | ----------- |
| licenseAggregator.image | Mandatory | quay.io/citrix/cpx-license-aggregator:1.0.0 | The CLA image. |
| licenseAggregator.pullPolicy | Mandatory | IfNotPresent | The CLA image pull policy. |
| licenseAggregator.service.type | Mandatory | NodePort | Type of service used to expose CLA. |
| licenseAggregator.service.nodePort | Optional | N/A | The port on the cluster node to be used to expose CLA service if the type of CLA service is NodePort. Make sure the parameter `licenseAggregator.service.type` has value `NodePort` for using this option. |
| licenseAggregator.username | Mandatory | N/A | Please provide the username/clustername that can uniquely identify this license aggregator service with the Citrix ADM License server. CLA would register itself with <username>.<servicename>.<namespace> with the Citrix ADM. It helps Citrix ADM in keeping track of various License Aggregator instances. |
| licenseAggregator.securityContext |  Optional | N/A | Security context for license-aggregator container. |
| licenseAggregator.resources | Optional | N/A | Resouces restrictions for license-aggregator container. |
| nslped.image | Mandatory | quay.io/citrix/nslped:1.0.0 | The nslped image. |
| nslped.pullPolicy | Mandatory | IfNotPresent | The nslped image pull policy. |
| nslped.securityContext |  Optional | N/A | Security context for nslped container. |
| nslped.resources | Optional | N/A | Resouces restrictions for nslped container. |
| redis.image | Mandatory | redis:7.0.4 | The redis image. |
| redis.pullPolicy | Mandatory | IfNotPresent | The redis image pull policy. |
| redis.secretName | Mandatory | N/A | Kubernetes secret name created for Redis DB password. |
| redis.securityContext |  Optional | N/A | Security context for redis container. |
| redis.resources | Optional | N/A | Resouces restrictions for redis container. |
| sidecarCertsGenerator.image | Mandatory | quay.io/citrix/cpx-sidecar-injector-certgen:1.2.0 | The sidecarCertsGenerator image. |
| sidecarCertsGenerator.pullPolicy | Mandatory | IfNotPresent | The sidecarCertsGenerator image pull policy. |
| serviceAccount.annotations |  Optional | N/A | Annotations to be used for serviceaccount that is being used by CLA. |
| licenseServer.address | Mandatory | N/A | IP or FQDN of License Server. |
| licenseServer.port | Mandatory | 27000 | Port to be used for making connection to License Server. |
| licenseInfo.quantum | Mandatory | 5 | Number of licenses to be checked-out from license server at one time. |
| licenseInfo.lowWatermark | Mandatory | 2 | If free licenses fall below this watermark, check-out additional license-quantum. |
| licenseInfo.dbExpireTime | Mandatory | 172800 | Time to keep Citrix ADC CPX data in Redis DB without any heartbeat from Citrix ADC CPX in seconds. |
| adcInfo.selectorLabel.key | Mandatory | adc | CLA will use this as key in the selector label for monitoring Citrix ADC CPX pod. |
| adcInfo.selectorLabel.value | Mandatory | citrix | CLA will use this as value in the selector label for monitoring Citrix ADC CPX pod. |
| podAnnotations | Optional | N/A | Annotation to be used in CLA pod. |
| podSecurityContext | Optional | N/A | Security Context to be used for CLA pod. |
| nodeSelector | Optional | N/A | Node selector to be used for CLA pod. |
| tolerations | Optional | N/A | Tolerations to be used for CLA pod. |
| affinity | Optional | N/A | Node Affinity to be used for CLA pod. |
| imagePullSecrets | Optional | N/A | Provide list of Kubernetes secrets to be used for pulling the images from a private Docker registry or repository. For more information on how to create this secret please see [Pull an Image from a Private Registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/). |

Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

For example:
   ```
   helm install my-release citrix/cpx-license-aggregator -f values.yaml
   ```

> **Tip:**
>
> The [values.yaml](https://github.com/citrix/citrix-helm-charts/blob/master/cpx-license-aggregator/values.yaml) contains the default values of the parameters.

### Citrix ADC CPX License Aggregator Services:

1. To see the CLA stats use the following URL in the browser:

   `https://<K8s-node-ip>:<cla-svc-nodeport>/stats`

2. To see the Citrix ADC CPX information running in the cluster use the following URL in the browser:

   `https://<NodeIP:Nodeport>/cpxinfo`
   > **Note:** HTTP request to this URL must contain HTTP header named x-cla with value 1.0.0

## Uninstalling the Chart
We are using persistent volume for CLA to store and retain the Licensed Citrix ADC CPX information in case of any failures. As part of Helm install one persistent volume claim get created for the stateful set which needs to be deleted manually afterwards.
 
So, to uninstall the chart with release name `my-release`:

1. Uninstall/delete the `my-release` deployment:
   ```
   helm delete my-release
   ```
2. Delete the pvc:
   ```
   kubectl delete pvc data-my-release-cpx-license-aggregator-0 -n <Release-Namespace>
   ```

The command removes all the Kubernetes components associated with the chart and deletes the release.
