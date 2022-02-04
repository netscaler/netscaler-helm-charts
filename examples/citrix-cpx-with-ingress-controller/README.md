# Citrix ADC CPX with inbuilt Ingress Controller  

[Citrix](https://www.citrix.com) ADC CPX with the Citrix Ingress Controller running in side-car mode will configure the CPX that runs as pod in a [Kubernetes](https://kubernetes.io) Cluster or in an [Openshift](https://www.openshift.com) cluster and does N-S load balancing of Guestbook app.


## TL;DR;

### For Kubernetes
```
   git clone https://github.com/citrix/citrix-helm-charts.git
   cd citrix-helm-charts/examples/
   helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes,serviceType.nodePort.enabled=true
```
### For OpenShift
``` 
   git clone https://github.com/citrix/citrix-helm-charts.git
   cd citrix-helm-charts/examples/
   helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes,serviceType.nodePort.enabled=true,openshift=true
```

> Note: "license.accept" is a mandatory argument and should be set to "yes" to accept the terms of the Citrix license.

## Introduction
This Chart deploys Citrix ADC CPX with inbuilt Ingress Controller in the [Kubernetes](https://kubernetes.io) Cluster or in the [Openshift](https://www.openshift.com) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version is 1.16 or later if using Kubernetes environment.
-  The [Openshift](https://www.openshift.com) version 4.8 or later if using OpenShift platform.
-  The [Helm](https://helm.sh/) version 3.x or later. You can follow instruction given [here](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.
-  You have installed [Prometheus Operator](https://github.com/coreos/prometheus-operator), if you want to view the metrics of the Citrix ADC CPX collected by the [metrics exporter](https://github.com/citrix/citrix-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics).

## Installing the Chart

### For Kubernetes:
To install the chart with the release name ``` my-release```:

```helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes,serviceType.nodePort.enabled=true,ingressClass[0]=<ingressClassName>```

To run the exporter as sidecar with CPX, please install prometheus operator first and then use the following command:

```helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes,serviceType.nodePort.enabled=true,ingressClass=<ingressClassName>,exporter.required=true```

### For OpenShift:
Add the name of the service account created when the chart is deployed to the privileged Security Context Constraints of OpenShift:

   ```
   oc adm policy add-scc-to-user privileged system:serviceaccount:<namespace>:<service-account-name>
   ```

To install the chart with the release name ``` my-release```:

```helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes,serviceType.nodePort.enabled=true,ingressClass[0]=<ingressClassName>,openshift=true```

To run the exporter as sidecar with CPX, please install prometheus operator first and then use the following command:

```helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes,serviceType.nodePort.enabled=true,ingressClass=<ingressClassName>,exporter.required=true,openshift=true```

The command deploys Citrix ADC CPX with Citrix Ingress Controller running in side-car mode on the Kubernetes cluster in the default configuration. The configuration section lists the parameters that can be configured during installation.

## Tolerations

Taints are applied on cluster nodes whereas tolerations are applied on pods. Tolerations enable pods to be scheduled on node with matching taints. For more information see [Taints and Tolerations in Kubernetes](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/).

For example, if the node is tainted using command:
```
kubectl taint nodes worker1 key1=value1:NoSchedule
```

And if user wants to enable CPX with ingress controller pod to be scheduled on node `worker1` then the following command can be used to add matching toleration in CPX with ingress controller while deploying it using Helm:
```
helm install my-release citrix-cpx-with-ingress-controller --set license.accept=yes,tolerations[0].key=key1,tolerations[0].value=value1,tolerations[0].operator=Equal,tolerations[0].effect=NoSchedule
```
 
## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:
```
helm delete --purge my-release
```
The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration
The following table lists the configurable parameters of the Citrix ADC CPX with Citrix ingress controller as side car chart and their default values.

| Parameters | Mandatory or Optional | Default value | Description |
| ---------- | --------------------- | ------------- | ----------- |
| license.accept | Mandatory | no | Set `yes` to accept the Citrix ingress controller end user license agreement. |
| image | Mandatory | `quay.io/citrix/citrix-k8s-cpx-ingress:13.0-83.27` | The Citrix ADC CPX image. |
| pullPolicy | Mandatory | IfNotPresent | The Citrix ADC CPX image pull policy. |
| cic.image | Mandatory | `quay.io/citrix/citrix-k8s-ingress-controller:1.22.7` | The Citrix ingress controller image. |
| cic.pullPolicy | Mandatory | IfNotPresent | The Citrix ingress controller image pull policy. |
| cic.required | Mandatory | true | CIC to be run as sidecar with Citrix ADC CPX |
| imagePullSecrets | Optional | N/A | Provide list of Kubernetes secrets to be used for pulling the images from a private Docker registry or repository. For more information on how to create this secret please see [Pull an Image from a Private Registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/). |
| logLevel | Optional | DEBUG | The loglevel to control the logs generated by CIC. The supported loglevels are: CRITICAL, ERROR, WARNING, INFO, DEBUG and TRACE. For more information, see [Logging](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/log-levels.md).|
| defaultSSLCertSecret | Optional | N/A | Provide Kubernetes secret name that needs to be used as a default non-SNI certificate in Citrix ADC. |
| nsHTTP2ServerSide | Optional | OFF | Set this argument to `ON` for enabling HTTP2 for Citrix ADC service group configurations. |
| nsCookieVersion | Optional | 0 | Specify the persistence cookie version (0 or 1). |
| logProxy | Optional | N/A | Provide Elasticsearch or Kafka or Zipkin endpoint for Citrix observability exporter. |
| nsProtocol | Optional | http | Protocol http or https used for the communication between Citrix Ingress Controller and CPX |
| cpxBgpRouter | Optional | false| If set to true, this CPX is deployed as daemonset in BGP controller mode wherein BGP advertisements are done for attracting external traffic to Kubernetes clusters |
| nsIP | Optional | 192.168.1.2 | NSIP used by CPX for internal communication when run in Host mode, i.e when cpxBgpRouter is set to true. A /24 internal network is created in this IP range which is used for internal communications withing the network namespace. |
| nsGateway | Optional | 192.168.1.1 | Gateway used by CPX for internal communication when run in Host mode, i.e when cpxBgpRouter is set to true. If not specified, first IP in the nsIP network is used as gateway. It must be in same network as nsIP |
| bgpPort | Optional | 179 | BGP port used by CPX for BGP advertisement if cpxBgpRouter is set to true|
| ingressIP | Optional | N/A | External IP address to be used by ingress resources if not overriden by ingress.com/frontend-ip annotation in Ingress resources. This is also advertised to external routers when pxBgpRouter is set to true|
| entityPrefix | Optional | k8s | The prefix for the resources on the Citrix ADC CPX. |
| ingressClass | Optional | Citrix | If multiple ingress load balancers are used to load balance different ingress resources. You can use this parameter to specify Citrix ingress controller to configure Citrix ADC associated with specific ingress class. For more information on Ingress class, see [Ingress class support](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/configure/ingress-classes/). For Kubernetes version >= 1.19, this will create an IngressClass object with the name specified here  |
| setAsDefaultIngressClass | Optional | False | Set the IngressClass object as default. New Ingresses without an "ingressClassName" field specified will be assigned the class specified in ingressClass. Applicable only for kubernetes versions >= 1.19 |
| updateIngressStatus | Optional | False | Set this argument if you want to update ingress status of the ingress resources exposed via CPX. This is only applicable if servicetype of CPX service is LoadBalancer. |
| disableAPIServerCertVerify | Optional | False | Set this parameter to True for disabling API Server certificate verification. |
| openshift | Optional | false | Set this argument if OpenShift environment is being used. |
| crds.retainOnDelete | Optional | false | Set this argument if you want to retain CustomResourceDefinitions even after uninstalling CIC. This will avoid data-loss of Custom Resource Objects created before uninstallation. |
bels | Optional | N/A | You can use this parameter to provide the route labels selectors to be used by Citrix Ingress Controller for routeSharding in OpenShift cluster. |
| namespaceLabels | Optional | N/A | You can use this parameter to provide the namespace labels selectors to be used by Citrix Ingress Controller for routeSharding in OpenShift cluster. |
| sslCertManagedByAWS | Optional | False | Set this argument if SSL certs used is managed by AWS while deploying Citrix ADC CPX in AWS. |
| nodeSelector.key | Optional | N/A | Node label key to be used for nodeSelector option for CPX-CIC deployment. |
| nodeSelector.value | Optional | N/A | Node label value to be used for nodeSelector option in CPX-CIC deployment. |
| tolerations | Optional | N/A | Specify the tolerations for the CPX-CIC deployment. |
| serviceType.loadBalancer.enabled | Optional | False | Set this argument if you want servicetype of CPX service to be LoadBalancer. |
| serviceType.nodePort.enabled | Optional | False | Set this argument if you want servicetype of CPX service to be NodePort. |
| serviceType.nodePort.httpPort | Optional | N/A | Specify the HTTP nodeport to be used for NodePort CPX service. |
| serviceType.nodePort.httpsPort | Optional | N/A | Specify the HTTPS nodeport to be used for NodePort CPX service. |
| serviceAnnotations | Optional | N/A | Dictionary of annotations to be used in CPX service. Key in this dictionary is the name of the annotation and Value is the required value of that annotation. |
| serviceSpec.loadBalancerSourceRanges | Optional | N/A | Provide the list of IP Address or range which should be allowed to access the Network Load Balancer. For details, see [Network Load Balancer support on AWS](https://kubernetes.io/docs/concepts/services-networking/service/#aws-nlb-support). |
| servicePorts | Optional | N/A | List of port. Each element in this list is a dictionary that contains information about the port. |
| ADMSettings.licenseServerIP | Optional | N/A | Provide the Citrix Application Delivery Management (ADM) IP address to license Citrix ADC CPX. For more information, see [Licensing](https://developer-docs.citrix.com/projects/citrix-k8s-ingress-controller/en/latest/licensing/). |
| ADMSettings.licenseServerPort | Optional | 27000 | Citrix ADM port if non-default port is used. |
| ADMSettings.ADMIP | Optional | N/A |  Citrix Application Delivery Management (ADM) IP address. |
| ADMSettings.loginSecret | Optional | N/A | The secret key to login to the ADM. For information on how to create the secret keys, see [Prerequisites](#prerequistes). |
| ADMSettings.bandWidthLicense | Optional | False | Set to true if you want to use bandwidth based licensing for Citrix ADC CPX. |
| ADMSettings.bandWidth | Optional | N/A | Desired bandwidth capacity to be set for Citrix ADC CPX in Mbps. |
| ADMSettings.vCPULicense | Optional | N/A | Set to true if you want to use vCPU based licensing for Citrix ADC CPX. |
| ADMSettings.cpxCores | Optional | 1 | Desired number of vCPU to be set for Citrix ADC CPX. |
| exporter.required | Optional | false | Use the argument if you want to run the [Exporter for Citrix ADC Stats](https://github.com/citrix/citrix-adc-metrics-exporter) along with Citrix ingress controller to pull metrics for the Citrix ADC CPX|
| exporter.image | Optional | `quay.io/citrix/citrix-adc-metrics-exporter:1.4.9` | The Exporter for Citrix ADC Stats image. |
| exporter.pullPolicy | Optional | IfNotPresent | The Exporter for Citrix ADC Stats image pull policy. |
| exporter.ports.containerPort | Optional | 8888 | The Exporter for Citrix ADC Stats container port. |
| coeConfig.required | Mandatory | false | Set this to true if you want to configure Citrix ADC to send metrics and transaction records to COE. |
| coeConfig.distributedTracing.enable | Optional | false | Set this value to true to enable OpenTracing in Citrix ADC. |
| coeConfig.distributedTracing.samplingrate | Optional | 100 | Specifies the OpenTracing sampling rate in percentage. |
| coeConfig.endpoint.server | Optional | N/A | Set this value as the IP address or DNS address of the  analytics server. |
| coeConfig.timeseries.port | Optional | 5563 | Specify the port used to expose COE service for timeseries endpoint. |
| coeConfig.timeseries.metrics.enable | Optional | Set this value to true to enable sending metrics from Citrix ADC. |
| coeConfig.timeseries.metrics.mode | Optional | avro |  Specifies the mode of metric endpoint. |
| coeConfig.timeseries.auditlogs.enable | Optional | false | Set this value to true to export audit log data from Citrix ADC. |
| coeConfig.timeseries.events.enable | Optional | false | Set this value to true to export events from the Citrix ADC. |
| coeConfig.transactions.enable | Optional | false | Set this value to true to export transactions from Citrix ADC. |
| coeConfig.transactions.port | Optional | 5557 | Specify the port used to expose COE service for transaction endpoint. |
| crds.install | Optional | False | Unset this argument if you don't want to install CustomResourceDefinitions which are consumed by CIC. |
| crds.retainOnDelete | Optional | false | Set this argument if you want to retain CustomResourceDefinitions even after uninstalling CIC. This will avoid data-loss of Custom Resource Objects created before uninstallation. |
| bgpSettings.required | Optional | false | Set this argument if you want to enable BGP configurations for exposing service of Type Loadbalancer through BGP fabric|
| bgpSettings.bgpConfig | Optional| N/A| This represents BGP configurations in YAML format. For the description about individual fields, please refer the [documentation](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network/cpx-bgp-router.md) |

> **Tip:**
>
> The [values.yaml](https://github.com/citrix/citrix-helm-charts/blob/master/examples/citrix-cpx-with-ingress-controller/values.yaml) contains the default values of the parameters.

## RBAC
By default the chart will install the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and rolebindings.

## Exporter
[Exporter](https://github.com/citrix/citrix-adc-metrics-exporter) is running as sidecar with the CPX and pulling metrics from the CPX. It exposes the metrics using Kubernetes NodePort.

## Ingress Class
To know more about Ingress Class refer [this](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/configure/ingress-classes.md).

## For More Info: https://github.com/citrix/citrix-k8s-ingress-controller

