# NetScaler CPX with inbuilt Ingress Controller

[NetScaler](https://www.citrix.com) NetScaler CPX with the NetScaler Ingress Controller running in side-car mode will configure the CPX that runs as pod in a [Kubernetes](https://kubernetes.io) Cluster or in an [Openshift](https://www.openshift.com) cluster and does N-S load balancing of Guestbook app.


## TL;DR;

### For Kubernetes
```
   git clone https://github.com/netscaler/netscaler-helm-charts.git
   cd citrix-helm-charts/examples/
   helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes,serviceType.nodePort.enabled=true
```
### For OpenShift
```
   git clone https://github.com/netscaler/netscaler-helm-charts.git
   cd citrix-helm-charts/examples/
   helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes,serviceType.nodePort.enabled=true,openshift=true
```

> Note: "license.accept" is a mandatory argument and should be set to "yes" to accept the terms of the NetScaler license.

## Introduction
This Chart deploys NetScaler CPX with inbuilt Ingress Controller in the [Kubernetes](https://kubernetes.io) Cluster or in the [Openshift](https://www.openshift.com) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version is 1.16 or later if using Kubernetes environment.
-  The [Openshift](https://www.openshift.com) version 4.8 or later if using OpenShift platform.
-  The [Helm](https://helm.sh/) version 3.x or later. You can follow instruction given [here](https://github.com/netscaler/netscaler-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.
-  You have installed [Prometheus Operator](https://github.com/coreos/prometheus-operator), if you want to view the metrics of the NetScaler CPX collected by the [metrics exporter](https://github.com/netscaler/netscaler-k8s-ingress-controller/tree/master/metrics-visualizer#visualization-of-metrics).

## Installing the Chart

### For Kubernetes:
To install the chart with the release name ```cpx```:

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

The command deploys NetScaler CPX with NetScaler Ingress Controller running in side-car mode on the Kubernetes cluster in the default configuration. The configuration section lists the parameters that can be configured during installation.

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
### Resource Quotas
There are various use-cases when resource quotas are configured on the Kubernetes cluster. If quota is enabled in a namespace for compute resources like cpu and memory, users must specify requests or limits for those values; otherwise, the quota system may reject pod creation. The resource quotas for the NSICC and CPX containers can be provided explicitly in the helm chart.

To set requests and limits for the NSIC container, use the variables `cic.resources.requests` and `cic.resources.limits` respectively.
Similarly, to set requests and limits for the CPX container, use the variable `resources.requests` and `resources.limits` respectively.

Below is an example of the helm command that configures

A) For NSIC container:

  CPU request for 500milli CPUs

  CPU limit at 1000m

  Memory request for 512M
  
  Memory limit at 1000M

B) For CPX container:
  
  CPU request for 250milli CPUs
  
  CPU limit at 500m
  
  Memory request for 256M

  Memory limit at 512M

```
helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes --set cic.resources.requests.cpu=500m,cic.resources.requests.memory=512Mi --set cic.resources.limits.cpu=1000m,cic.resources.limits.memory=1000Mi --set resources.limits.cpu=500m,resources.limits.memory=512Mi --set resources.requests.cpu=250m,resources.requests.memory=256Mi
```

### Analytics Configuration
#### Analytics Configuration required for ADM

If NetScaler CPX needs to send data to the ADM for analytics purpose, then the below steps can be followed to install NetScaler CPX with ingress controller. NSIC configures the NetScaler CPX with the configuration required for analytics.

1. Create secret using ADM Agent credentials, which will be used by NetScaler CPX to communicate with ADM Agent:

```
kubectl create secret generic admlogin --from-literal=username=<adm-agent-username> --from-literal=password=<adm-agent-password>
```

|Note: If you have installed container based `adm-agent` using [this](https://github.com/netscaler/netscaler-helm-charts/tree/master/adm-agent) helm chart, above step is not required, you just need to tag the namespace where the CPX is being deployed with `citrix-cpx=enabled`.

2. Deploy NetScaler CPX with NSIC using helm command:

```
helm install cpx citrix-cpx-with-ingress-controller--set license.accept=yes,analyticsConfig.required=true,analyticsConfig.distributedTracing.enable=true,analyticsConfig.endpoint.service=<Namespace/ADM_ServiceName-logstream>,ADMSettings.ADMIP=<ADM-Agent-IP_OR_FQDN>,ADMSettings.loginSecret=<Secret-for-ADM-Agent-credentials>,analyticsConfig.transactions.enable=true,analyticsConfig.transactions.port=5557
```
|Note: For container based ADM agent, please provide the logstream service FQDN in `analyticsConfig.endpoint.service`. The `logstream` service will be running on port `5557`.

#### Analytics Configuration required for NSOE

If NetScaler CPX needs to send data to the NSOE for observability, then the below steps can be followed to install NetScaler CPX with ingress controller. NSIC configures NetScaler CPX with the configuration required.

Deploy NetScaler CPX with NSIC using helm command:

```
helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes,analyticsConfig.required=true,analyticsConfig.timeseries.metrics.enable=true,analyticsConfig.timeseries.port=5563,analyticsConfig.timeseries.metrics.mode=prometheus,analyticsConfig.transactions.enable=true,analyticsConfig.transactions.port=5557,analyticsConfig.distributedTracing.enable=true,analyticsConfig.endpoint.server=<NSOE_SERVICE_IP>,analyticsConfig.endpoint.service=<Namespace/NSOE_SERVICE_NAME>
```

#### Analytics Configuration required for export of metrics to Prometheus

If NetScaler CPX needs to send data to Prometheus directly without an exporter resource in between, then the below steps can be followed to install NetScaler CPX with ingress controller. NSIC configures NetScaler CPX with the configuration required.

1. Create secret to enable read-only access for a user, which will be required by NetScaler CPX to export metrics to Prometheus.

```
kubectl create secret generic prom-user --from-literal=username=<prometheus-username> --from-literal=password=<prometheus-password>
```

2. Deploy NetScaler CPX with NSIC using helm command:

```
helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes,cic.prometheusCredentialSecret=<Secret-for-read-only-user-creation>,analyticsConfig.required=true,analyticsConfig.timeseries.metrics.enable=true,analyticsConfig.timeseries.port=5563,analyticsConfig.timeseries.metrics.mode=prometheus,analyticsConfig.timeseries.metrics.enableNativeScrape=true
```

3. To setup Prometheus in order to scrape natively from NetScaler CPX pod, a new scrape job is required to be added under scrape_configs in the prometheus [configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/). For more details, check kubernetes_sd_config [here](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config). A sample of the Prometheus job is given below -

```
    - job_name: 'kubernetes-cpx'
      scheme: http
      metrics_path: /nitro/v1/config/systemfile
      params:
        args: ['filename:metrics_prom_ns_analytics_time_series_profile.log,filelocation:/var/nslog']
        format: ['prometheus']
      basic_auth:
        username:  # Prometheus username set in cic.prometheusCredentialSecret
        password:  # Prometheus password set in cic.prometheusCredentialSecret
      scrape_interval: 30s
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_netscaler_prometheus_scrape]
        action: keep
        regex: true
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_netscaler_prometheus_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name
```

> **Note:**
>
> For more details on Prometheus integration, please refer to [this](https://docs.netscaler.com/en-us/citrix-adc/current-release/observability/prometheus-integration)

### NetScaler CPX License Provisioning
#### Bandwidth based licensing

By default, CPX runs with 20 Mbps bandwidth called as [CPX Express](https://www.netscaler.com/platform/cpx-container). However, for better performance and production deployments, customer needs licensed CPX instances. [NetScaler ADM](https://docs.netscaler.com/en-us/citrix-application-delivery-management-service/) is used to check out licenses for NetScaler CPX. For more detail on CPX licensing please refer [this](https://docs.netscaler.com/en-us/citrix-adc-cpx/current-release/cpx-licensing.html).

For provisioning licensing on NetScaler CPX, it is mandatory to provide License Server information to CPX. This can be done by setting **ADMSettings.licenseServerIP** as License Server IP. In addition to this, **ADMSettings.bandWidthLicense** needs to be set true and desired bandwidth capacity in Mbps should be set **ADMSettings.bandWidth**.
For example, to set 2Gbps as bandwidth capacity, below command can be used.

 ```
helm install cpx citrix-cpx-with-ingress-controller--set license.accept=yes --set ADMSettings.licenseServerIP=<LICENSESERVER_IP_OR_FQDN>,ADMSettings.bandWidthLicense=True --set ADMSettings.bandWidth=2000,ADMSettings.licenseEdition="ENTERPRISE"
```

#### vCPU based licensing

For vCPU based licensing on NetScaler CPX, set `ADMSettings.vCPULicense` as True and `ADMSettings.cpxCores` with the number of cores that can be allocated for the CPX.

```
helm install cpx citrix-cpx-with-ingress-controller --set license.accept=yes --set ADMSettings.licenseServerIP=<LICENSESERVER_IP_OR_FQDN>,ADMSettings.vCPULicense=True --set ADMSettings.cpxCores=4,ADMSettings.licenseEdition="ENTERPRISE"
```

### Bootup Configuration for NetScaler CPX
To add bootup config on NetScaler CPX, add commands below `cpxCommands` and `cpxShellCommands` in the values.yaml file. The commands will be executed in order.

For e.g. to add `X-FORWARDED-PROTO` header in all request packets processed by the CPX, add below commands under `cpxCommands` in the `values.yaml` file.

```
cpxCommands: |
  add rewrite action rw_act_x_forwarded_proto insert_http_header X-Forwarded-Proto "\"https\""
  add rewrite policy rw_pol_x_forwarded_proto CLIENT.SSL.IS_SSL rw_act_x_forwarded_proto
  bind rewrite global rw_pol_x_forwarded_proto 10 -type REQ_OVERRIDE
```

Commands that needs to be executed in shell of CPX should be kept under `cpxShellCommands` in the `values.yaml` file.

```
cpxShellCommands: |
  touch /etc/a.txt
  echo "this is a" > /etc/a.txt
  echo "this is the file" >> /etc/a.txt
  ls >> /etc/a.txt
```

## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:
```
helm delete --purge my-release
```
The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration
The following table lists the configurable parameters of the NetScaler CPX with NetScaler ingress controller as side car chart and their default values.

| Parameters | Mandatory or Optional | Default value | Description |
| ---------- | --------------------- | ------------- | ----------- |
| license.accept | Mandatory | no | Set `yes` to accept the NetScaler ingress controller end user license agreement. |
| imageRegistry                   | Mandatory  |  `quay.io`               |  The NetScaler CPX image registry             |  
| imageRepository                 | Mandatory  |  `citrix/citrix-k8s-cpx-ingress`              |   The NetScaler CPX image repository             | 
| imageTag                  | Mandatory  |  `13.1-51.15`               |   The NetScaler CPX image tag            | 
| pullPolicy | Mandatory | IfNotPresent | The NetScaler CPX image pull policy. |
| cic.imageRegistry                   | Mandatory  |  `quay.io`               |  The NetScaler ingress controller image registry             |  
| cic.imageRepository                 | Mandatory  |  `citrix/citrix-k8s-ingress-controller`              |   The NetScaler ingress controller image repository             | 
| cic.imageTag                  | Mandatory  |  `1.37.5`               |   The NetScaler ingress controller image tag            | 
| cic.pullPolicy | Mandatory | IfNotPresent | The NetScaler ingress controller image pull policy. |
| cic.required | Mandatory | true | NSIC to be run as sidecar with NetScaler CPX |
| cic.resources | Optional | {} |	CPU/Memory resource requests/limits for NetScaler Ingress Controller container |
| cic.prometheusCredentialSecret  | Optional |  N/A  |  The secret key required to create read only user for native export of metrics using Prometheus. |
| imagePullSecrets | Optional | N/A | Provide list of Kubernetes secrets to be used for pulling the images from a private Docker registry or repository. For more information on how to create this secret please see [Pull an Image from a Private Registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/). |
| nameOverride | Optional | N/A | String to partially override deployment fullname template with a string (will prepend the release name) |
| fullNameOverride | Optional | N/A | String to fully override deployment fullname template with a string |
| resources | Optional | {} |	CPU/Memory resource requests/limits for NetScaler CPX container |
| logLevel | Optional | INFO | The loglevel to control the logs generated by NSIC. The supported loglevels are: CRITICAL, ERROR, WARNING, INFO, DEBUG and TRACE. For more information, see [Logging](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/configure/log-levels.md).|
| jsonLog | Optional | false | Set this argument to true if log messages are required in JSON format | 
| nsConfigDnsRec | Optional | false | To enable/disable DNS address Record addition in NetScaler through Ingress |
| nsSvcLbDnsRec | Optional | false | To enable/disable DNS address Record addition in NetScaler through Type Load Balancer Service |
| nsDnsNameserver | Optional | N/A | To add DNS Nameservers in NetScaler |
| rbacRole  | Optional |  false  |  To deploy NSIC with RBAC Role set rbacRole=true; by default NSIC gets installed with RBAC ClusterRole(rbacRole=false)) |
| optimizeEndpointBinding | Optional | false | To enable/disable binding of backend endpoints to servicegroup in a single API-call. Recommended when endpoints(pods) per application are large in number. Applicable only for NetScaler Version >=13.0-45.7  |
| defaultSSLCertSecret | Optional | N/A | Provide Kubernetes secret name that needs to be used as a default non-SNI certificate in NetScaler. |
| nsHTTP2ServerSide | Optional | OFF | Set this argument to `ON` for enabling HTTP2 for NetScaler service group configurations. |
| nsCookieVersion | Optional | 0 | Specify the persistence cookie version (0 or 1). |
| profileSslFrontend | Optional | N/A | Specify the frontend SSL profile. For Details see [Configuration using FRONTEND_SSL_PROFILE](https://docs.netscaler.com/en-us/citrix-k8s-ingress-controller/configure/profiles.html#global-front-end-profile-configuration-using-configmap-variables) |
| profileTcpFrontend | Optional | N/A | Specify the frontend TCP profile. For Details see [Configuration using FRONTEND_TCP_PROFILE](https://docs.netscaler.com/en-us/citrix-k8s-ingress-controller/configure/profiles.html#global-front-end-profile-configuration-using-configmap-variables) |
| profileHttpFrontend | Optional | N/A | Specify the frontend HTTP profile. For Details see [Configuration using FRONTEND_HTTP_PROFILE](https://docs.netscaler.com/en-us/citrix-k8s-ingress-controller/configure/profiles.html#global-front-end-profile-configuration-using-configmap-variables) |
| logProxy | Optional | N/A | Provide Elasticsearch or Kafka or Zipkin endpoint for NetScaler observability exporter. |
| nsProtocol | Optional | http | Protocol http or https used for the communication between NetScaler Ingress Controller and CPX |
| cpxLicenseAggregator | Optional | N/A | IP/FQDN of the CPX License Aggregator if it is being used to license the CPX. |
| nitroReadTimeout | Optional | 20 | The nitro Read timeout in seconds, defaults to 20 |
| cpxBgpRouter | Optional | false| If set to true, this CPX is deployed as daemonset in BGP controller mode wherein BGP advertisements are done for attracting external traffic to Kubernetes clusters |
| nsIP | Optional | 192.168.1.2 | NSIP used by CPX for internal communication when run in Host mode, i.e when cpxBgpRouter is set to true. A /24 internal network is created in this IP range which is used for internal communications withing the network namespace. |
| nsGateway | Optional | 192.168.1.1 | Gateway used by CPX for internal communication when run in Host mode, i.e when cpxBgpRouter is set to true. If not specified, first IP in the nsIP network is used as gateway. It must be in same network as nsIP |
| bgpPort | Optional | 179 | BGP port used by CPX for BGP advertisement if cpxBgpRouter is set to true|
| ingressIP | Optional | N/A | External IP address to be used by ingress resources if not overriden by ingress.com/frontend-ip annotation in Ingress resources. This is also advertised to external routers when pxBgpRouter is set to true|
| entityPrefix | Optional | k8s | The prefix for the resources on the NetScaler CPX. |
| ingressClass | Optional | NetScaler | If multiple ingress load balancers are used to load balance different ingress resources. You can use this parameter to specify NetScaler ingress controller to configure NetScaler associated with specific ingress class. For more information on Ingress class, see [Ingress class support](https://docs.netscaler.com/en-us/citrix-k8s-ingress-controller/configure/ingress-classes/). For Kubernetes version >= 1.19, this will create an IngressClass object with the name specified here  |
| setAsDefaultIngressClass | Optional | False | Set the IngressClass object as default. New Ingresses without an "ingressClassName" field specified will be assigned the class specified in ingressClass. Applicable only for kubernetes versions >= 1.19 |
| updateIngressStatus | Optional | False | Set this argument if you want to update ingress status of the ingress resources exposed via CPX. This is only applicable if servicetype of CPX service is LoadBalancer. |
| disableAPIServerCertVerify | Optional | False | Set this parameter to True for disabling API Server certificate verification. |
| openshift | Optional | false | Set this argument if OpenShift environment is being used. |
| disableOpenshiftRoutes | Optional | false | By default Openshift routes are processed in openshift environment, this variable can be used to disable Ingress controller processing the openshift routes. |
| crds.retainOnDelete | Optional | false | Set this argument if you want to retain CustomResourceDefinitions even after uninstalling NSIC. This will avoid data-loss of Custom Resource Objects created before uninstallation. |
bels | Optional | N/A | You can use this parameter to provide the route labels selectors to be used by NetScaler Ingress Controller for routeSharding in OpenShift cluster. |
| namespaceLabels | Optional | N/A | You can use this parameter to provide the namespace labels selectors to be used by NetScaler Ingress Controller for routeSharding in OpenShift cluster. |
| sslCertManagedByAWS | Optional | False | Set this argument if SSL certs used is managed by AWS while deploying NetScaler CPX in AWS. |
| nodeSelector.key | Optional | N/A | Node label key to be used for nodeSelector option for CPX-NSIC deployment. |
| nodeSelector.value | Optional | N/A | Node label value to be used for nodeSelector option in CPX-NSIC deployment. |
| podAnnotations | Optional | N/A | Map of annotations to add to the pods. |
| affinity | Optional | N/A | Affinity labels for pod assignment. |
| tolerations | Optional | N/A | Specify the tolerations for the CPX-NSIC deployment. |
| serviceType.loadBalancer.enabled | Optional | False | Set this argument if you want servicetype of CPX service to be LoadBalancer. |
| serviceType.nodePort.enabled | Optional | False | Set this argument if you want servicetype of CPX service to be NodePort. |
| serviceType.nodePort.httpPort | Optional | N/A | Specify the HTTP nodeport to be used for NodePort CPX service. |
| serviceType.nodePort.httpsPort | Optional | N/A | Specify the HTTPS nodeport to be used for NodePort CPX service. |
| serviceAnnotations | Optional | N/A | Dictionary of annotations to be used in CPX service. Key in this dictionary is the name of the annotation and Value is the required value of that annotation. |
| serviceSpec.loadBalancerSourceRanges | Optional | N/A | Provide the list of IP Address or range which should be allowed to access the Network Load Balancer. For details, see [Network Load Balancer support on AWS](https://kubernetes.io/docs/concepts/services-networking/service/#aws-nlb-support). |
| servicePorts | Optional | N/A | List of port. Each element in this list is a dictionary that contains information about the port. |
| ADMSettings.licenseServerIP | Optional | N/A | Provide the NetScaler Application Delivery Management (ADM) IP address to license NetScaler CPX. For more information, see [Licensing]( https://docs.netscaler.com/en-us/citrix-k8s-ingress-controller/licensing/). |
| ADMSettings.licenseServerPort | Optional | 27000 | NetScaler ADM port if non-default port is used. |
| ADMSettings.ADMIP | Optional | N/A |  NetScaler Application Delivery Management (ADM) IP address. |
| ADMSettings.loginSecret | Optional | N/A | The secret key to login to the ADM. For information on how to create the secret keys, see [Prerequisites](#prerequistes). |
| ADMSettings.bandWidthLicense | Optional | False | Set to true if you want to use bandwidth based licensing for NetScaler CPX. |
| ADMSettings.bandWidth | Optional | 1000 | Desired bandwidth capacity to be set for NetScaler CPX in Mbps. |
| ADMSettings.vCPULicense | Optional | N/A | Set to true if you want to use vCPU based licensing for NetScaler CPX. |
| ADMSettings.cpxCores | Optional | 1 | Desired number of vCPU to be set for NetScaler CPX. |
| ADMSettings.licenseEdition| Optional | PLATINUM | License edition that can be Standard, Platinum and Enterprise . By default, Platinum is selected.|
| exporter.required | Optional | false | Use the argument if you want to run the [Exporter for NetScaler Stats](https://github.com/netscaler/netscaler-adc-metrics-exporterporter) along with NetScaler ingress controller to pull metrics for the NetScaler CPX|
| exporter.imageRegistry                   | Optional  |  `quay.io`               |  The Exporter for NetScaler Stats image registry             |  
| exporter.imageRepository                 | Optional  |  `citrix/citrix-adc-metrics-exporter`              |   The Exporter for NetScaler Stats image repository             | 
| exporter.imageTag                  | Optional  |  `1.4.9`               |  The Exporter for NetScaler Stats image tag            | 
| exporter.pullPolicy | Optional | IfNotPresent | The Exporter for NetScaler Stats image pull policy. |
| exporter.ports.containerPort | Optional | 8888 | The Exporter for NetScaler Stats container port. |
| analyticsConfig.required | Mandatory | false | Set this to true if you want to configure NetScaler to send metrics and transaction records to analytics service. |
| exporter.serviceMonitorExtraLabels | Optional |  | Extra labels for service monitor whem NetScaler-adc-metrics-exporter is enabled. |
| analyticsConfig.distributedTracing.enable | Optional | false | Set this value to true to enable OpenTracing in NetScaler. |
| analyticsConfig.distributedTracing.samplingrate | Optional | 100 | Specifies the OpenTracing sampling rate in percentage. |
| analyticsConfig.endpoint.server | Optional | N/A | Set this value as the IP address or DNS address of the  analytics server. |
| analyticsConfig.endpoint.service | Optional | N/A | Set this value as the IP address or service name with namespace of the analytics service deployed in Kubernetes. Format: namespace/servicename|
| analyticsConfig.timeseries.port | Optional | 5563 | Specify the port used to expose analytics service for timeseries endpoint. |
| analyticsConfig.timeseries.metrics.enable | Optional | Set this value to true to enable sending metrics from NetScaler. |
| analyticsConfig.timeseries.metrics.mode | Optional | avro |  Specifies the mode of metric endpoint. |
| analyticsConfig.timeseries.metrics.exportFrequency | Optional | 30 |  Specifies the time interval for exporting time-series data. Possible values range from 30 to 300 seconds. |
| analyticsConfig.timeseries.metrics.schemaFile | Optional | schema.json |  Specifies the name of a schema file with the required Netscaler counters to be added and configured for metricscollector to export. A reference schema file reference_schema.json with all the supported counters is also available under the path /var/metrics_conf/. This schema file can be used as a reference to build a custom list of counters. |
| analyticsConfig.timeseries.metrics.enableNativeScrape | Optional | false |  Set this value to true for native export of metrics. |
| analyticsConfig.timeseries.auditlogs.enable | Optional | false | Set this value to true to export audit log data from NetScaler. |
| analyticsConfig.timeseries.events.enable | Optional | false | Set this value to true to export events from the NetScaler. |
| analyticsConfig.transactions.enable | Optional | false | Set this value to true to export transactions from NetScaler. |
| analyticsConfig.transactions.port | Optional | 5557 | Specify the port used to expose analytics service for transaction endpoint. |
| crds.install | Optional | False | Unset this argument if you don't want to install CustomResourceDefinitions which are consumed by NSIC. |
| crds.retainOnDelete | Optional | false | Set this argument if you want to retain CustomResourceDefinitions even after uninstalling NSIC. This will avoid data-loss of Custom Resource Objects created before uninstallation. |
| bgpSettings.required | Optional | false | Set this argument if you want to enable BGP configurations for exposing service of Type Loadbalancer through BGP fabric|
| bgpSettings.bgpConfig | Optional| N/A| This represents BGP configurations in YAML format. For the description about individual fields, please refer the [documentation](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/network/bgp-enhancement.md) |
| nsLbHashAlgo.required | Optional | false | Set this value to set the LB consistent hashing Algorithm |
| nsLbHashAlgo.hashFingers | Optional | 256 | Specifies the number of fingers to be used for hashing algorithm. Possible values are from 1 to 1024, Default value is 256 |
| nsLbHashAlgo.hashAlgorithm | Optional | 'default' | Specifies the supported algorithm. Supported algorithms are "default", "jarh", "prac", Default value is 'default' |
| cpxCommands| Optional | N/A | This argument accepts user-provided bootup NetScaler config that is applied as soon as the CPX is instantiated. Please note that this is not a dynamic config, and any subsequent changes to the configmap don't reflect in the CPX config unless the pod is restarted. For more info, please refer the [documentation](https://docs.netscaler.com/en-us/citrix-adc-cpx/current-release/configure-cpx-kubernetes-using-configmaps.html).  |
| cpxShellCommands| Optional | N/A | This argument accepts user-provided bootup config that is applied as soon as the CPX is instantiated. Please note that this is not a dynamic config, and any subsequent changes to the configmap don't reflect in the CPX config unless the pod is restarted. For more info, please refer the [documentation](https://docs.netscaler.com/en-us/citrix-adc-cpx/current-release/configure-cpx-kubernetes-using-configmaps.html). |

> **Tip:**
>
> The [values.yaml](https://github.com/netscaler/netscaler-helm-charts/blob/master/examples/citrix-cpx-with-ingress-controller/values.yaml) contains the default values of the parameters.

## RBAC
By default the chart will install the recommended [RBAC](https://kubernetes.io/docs/admin/authorization/rbac/) roles and rolebindings.

## Exporter
[Exporter](https://github.com/netscaler/netscaler-adc-metrics-exporterporter) is running as sidecar with the CPX and pulling metrics from the CPX. It exposes the metrics using Kubernetes NodePort.

## Ingress Class
To know more about Ingress Class refer [this](https://github.com/netscaler/netscaler-k8s-ingress-controller/blob/master/docs/configure/ingress-classes.md).

## For More Info: https://github.com/netscaler/netscaler-k8s-ingress-controller

