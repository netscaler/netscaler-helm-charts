# Citrix Observability Exporter  

Citrix Observability Exporter is a container which collects metrics and transactions from Citrix ADCs and transforms them to suitable formats (such as JSON, AVRO) for supported endpoints like Elasticsearch, Kafka, Tracer, Prometheus. You can export the data collected by Citrix Observability Exporter to the desired endpoint. By analyzing the data exported to the endpoint, you can get valuable insights at a microservices level for applications proxied by Citrix ADCs.

### TL; DR; 
```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/
   
   For Kafka as endpoint with timeseries enabled:
   helm install coe citrix/citrix-cloud-native --set coe.enabled=true --set coe.kafka.enabled=true --set coe.kafka.broker="X.X.X.X\,Y.Y.Y.Y" --set coe.kafka.topic=HTTP --set coe.timeseries.enabled=true

   For Elasticsearch as endpoint and Tracing enabled:
   helm install coe citrix/citrix-cloud-native --set coe.enabled=true --set coe.elasticsearch.enabled=true --set coe.elasticsearch.server=elasticsearch.9200 --set coe.ns_tracing.enabled=true

```

## Introduction
This Helm chart deploys Citrix Observability Exporter in the [Kubernetes](https://kubernetes.io) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version 1.6 or later if using Kubernetes environment.
-  The [Helm](https://helm.sh/) version is 3.x or later. You can follow instruction given [here](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md) to install Helm in Kubernetes environment.

   - To enable Tracing, set coe.ns_tracing.enabled to true and coe.ns_tracing.server to the tracer endpoint like `zipkin.default.cluster.svc.local:9411/api/v1/spans`. Default value for Zipkin server is `zipkin:9411/api/v1/spans`. 

   - To enable Elasticsearch endpoint for transactions, set coe.elasticsearch.enabled to true and server to the elasticsearch endpoint like `elasticsearch.default.svc.cluster.local:9200`. Default value for Elasticsearch endpoint is `elasticsearch:9200`.

   - To enable Kafka endpoint for transactions, set coe.kafka.enabled to true, coe.kafka.broker to kafka broker IPs and kafka.topic. Default value for kafka topic is `HTTP`.

   - To enable Timeseries data upload in prometheus format, set coe.timeseries.enabled to true

## Installing the Chart
Add the Citrix Observability Exporter helm chart repository using command:

   ```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/
   ```

### For Kubernetes:
#### 1. Citrix Observability Exporter
To install the chart with the release name, `my-release`, use the following command, after setting the required endpoint in values.yaml:
   ```
   helm install my-release citrix/citrix-cloud-native --set coe.enabled=true
   ```

> **Important:**
>
> Citrix Observability Exporter is exposed using Nodeport 30001 and 30002 by default. Please make sure these ports are available for use in your cluster before deploying this helm chart.

### Configuration

The following table lists the mandatory and optional parameters that you can configure during installation:

| Parameters | Mandatory or Optional | Default value | Description |
| --------- | --------------------- | ------------- | ----------- |
| coe.enabled | Mandatory | False | Set to "True" for deploying Citrix Observability Exporter. |
| coe.license.accept | Mandatory | no | Set `yes` to accept the CIC end user license agreement. |
| coe.image | Mandatory | `quay.io/citrix/citrix-observability-exporter:1.1.001` | The COE image. |
| coe.pullPolicy | Mandatory | IfNotPresent | The COE image pull policy. |
| coe.transaction.nodePort | Optional | 30001 | Specify the port used to expose COE service outside cluster for transaction endpoint. |
| coe.ns_tracing.enabled | Optional | false | Set true to enable sending trace data to tracing server. |
| coe.ns_tracing.server | Optional | `zipkin:9411/api/v1/spans` | The tracing server api endpoint. |
| coe.elasticsearch.enabled | Optional | false | Set true to enable sending transaction data to elasticsearch server. |
| coe.elasticsearch.server | Optional | `elasticsearch:9200` | The Elasticsearch server api endpoint. |
| coe.kafka.enabled | Optional | false | Set true to enable sending transaction data to kafka server. |
| coe.kafka.broker | Optional |  | The kafka broker IP details. |
| coe.kafka.topic | Optional | `HTTP` | The kafka topic details to upload data. |
| coe.timeseries.enabled | Optional | false | Set true to enable sending timeseries data to prometheus. |
| coe.timeseries.nodePort | Optional | 30002 | Specify the port used to expose COE service outside cluster for timeseries endpoint. |

Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

For example:
   ```
   helm install my-release citrix/citrix-cloud-native -f values.yaml
   ```

> **Tip:**
>
> The [values.yaml](https://github.com/citrix/citrix-helm-charts/blob/master/citrix_cloud_native_values.yaml) contains the default values of the parameters.

## Uninstalling the Chart
To uninstall/delete the ```my-release``` deployment:

   ```
   helm delete my-release
   ```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Related documentation

-  [Citrix Observability Exporter Documentation](https://github.com/citrix/citrix-observability-exporter)
