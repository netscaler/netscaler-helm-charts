# Citrix Observability Exporter  

Citrix Observability Exporter is a container which collects metrics and transactions from Citrix ADCs and transforms them to suitable formats (such as JSON, AVRO) for supported endpoints. You can export the data collected by Citrix Observability Exporter to the desired endpoint for analysis and get valuable insights at a microservices level for applications proxied by Citrix ADCs.

Citrix Observability Exporter supports collecting transactions and streaming them to Elasticsearch, Kafka or Splunk.

Citrix Observability Exporter implements distributed tracing for Citrix ADC and currently supports Zipkin as the distributed tracer.

Citrix Observability Exporter supports collecting timeseries data (metrics) from Citrix ADC instances and exports them to Prometheus.

We can configure Citrix Observability Exporter helm chart to export transactional, tracing and timeseries (metrics) data to their corresponding endpoints.

### TL; DR; 
```
   helm repo add citrix https://citrix.github.io/citrix-helm-charts/

   For streaming transactions to Kafka, timeseries to Prometheus and tracing to zipkin:   
     helm install coe citrix/citrix-cloud-native --set coe.enabled=true --set coe.kafka.enabled=true --set coe.kafka.broker="X.X.X.X\,Y.Y.Y.Y" --set coe.kafka.topic=HTTP --set coe.kafka.dataFormat=AVRO --set coe.timeseries.enabled=true --set coe.ns_tracing.enabled=true --set coe.ns_tracing.server="zipkin:9411/api/v1/spans"

   For streaming transactions to Elasticsearch, timeseries to Prometheus and tracing to zipkin:
     helm install coe citrix/citrix-cloud-native --set coe.enabled=true --set coe.elasticsearch.enabled=true --set coe.elasticsearch.server=elasticsearch:9200 --set coe.timeseries.enabled=true --set coe.ns_tracing.enabled=true --set coe.ns_tracing.server="zipkin:9411/api/v1/spans"

   For streaming transactions to Splunk, timeseries to Prometheus and tracing to zipkin:
     helm install coe citrix/citrix-cloud-native --set coe.enabled=true --set coe.splunk.enabled=true --set coe.splunk.server="splunkServer:port" --set coe.splunk.authtoken="authtoken" --set coe.timeseries.enabled=true --set coe.ns_tracing.enabled=true --set coe.ns_tracing.server="zipkin:9411/api/v1/spans"

   For streaming timeseries data to Prometheus:
     helm install coe citrix/citrix-cloud-native --set coe.enabled=true --set coe.timeseries.enabled=true

   For streaming tracing data to Zipkin:
     helm install coe citrix/citrix-cloud-native --set coe.enabled=true --set coe.ns_tracing.enabled=true --set coe.ns_tracing.server="zipkin:9411/api/v1/spans"
   
```

## Introduction
This Helm chart deploys Citrix Observability Exporter in the [Kubernetes](https://kubernetes.io) cluster using [Helm](https://helm.sh) package manager.

### Prerequisites

-  The [Kubernetes](https://kubernetes.io/) version 1.6 or later if using Kubernetes environment.
-  The [Helm](https://helm.sh/) version is 3.x or later. You can follow instruction given [here](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md) to install Helm in Kubernetes environment.

   - To enable Tracing, set coe.ns_tracing.enabled to true and coe.ns_tracing.server to the tracer endpoint like `zipkin.default.cluster.svc.local:9411/api/v1/spans`. Default value for Zipkin server is `zipkin:9411/api/v1/spans`. 

   - To enable Elasticsearch endpoint for transactions, set coe.elasticsearch.enabled to true and server to the elasticsearch endpoint like `elasticsearch.default.svc.cluster.local:9200`. Default value for Elasticsearch endpoint is `elasticsearch:9200`.

   - To enable Kafka endpoint for transactions, set coe.kafka.enabled to true, coe.kafka.broker to kafka broker IPs, kafka.topic, and kafka.dataFormat . Default value for kafka topic is `HTTP`. Default value for kafka.dataFormat is `AVRO`.

   - To enable Timeseries data upload in prometheus format, set coe.timeseries.enabled to true. Currently Prometheus is the only timeseries endpoint supported. 

   - To enable Splunk endpoint for transactions, set splunk.enabled to true, splunk.server to Splunk server with port, splunk.authtoken to the token and splunk.indexprefix to the index prefix to upload the transactions. Default value for splunk.indexprefix is adc_coe .

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
| coe.imageRegistry                   | Mandatory  |  `quay.io`               |  The COE image registry             |  
| coe.imageRepository                 | Mandatory  |  `citrix/citrix-observability-exporter`              |   The COE image repository             | 
| coe.imageTag                  | Mandatory  |  `1.5.001`               |   The COE image tag            | 
| coe.pullPolicy | Mandatory | IfNotPresent | The COE image pull policy. |
| coe.nodePortRequired | Optional | false | Set true to create a nodeport COE service. |
| coe.headless | Optional | false | Set true to create Headless service. |
| coe.transaction.nodePort | Optional | 30001 | Specify the port used to expose COE service outside cluster for transaction endpoint. |
| coe.ns_tracing.enabled | Optional | false | Set true to enable sending trace data to tracing server. |
| coe.ns_tracing.server | Optional | `zipkin:9411/api/v1/spans` | The tracing server api endpoint. |
| coe.elasticsearch.enabled | Optional | false | Set true to enable sending transaction data to elasticsearch server. |
| coe.elasticsearch.server | Optional | `elasticsearch:9200` | The Elasticsearch server api endpoint. |
| coe.elasticsearch.indexprefix | Optional | adc_coe | The elasticsearch index prefix. |
| coe.splunk.enabled | Optional | false | Set true to enable sending transaction data to splunk server. |
| coe.splunk.authtoken | Optional |  | Set the authtoken for splunk. |
| coe.splunk.indexprefix | Optional | adc_coe | The splunk index prefix. |
| coe.kafka.enabled | Optional | false | Set true to enable sending transaction data to kafka server. |
| coe.kafka.broker | Optional |  | The kafka broker IP details. |
| coe.kafka.topic | Optional | `HTTP` | The kafka topic details to upload data. |
| kafka.dataFormat | Optional | `AVRO` | The format of the data exported to Kafka -- can be either JSON or AVRO, and defaults to AVRO
| coe.timeseries.enabled | Optional | false | Set true to enable sending timeseries data to prometheus. |
| coe.timeseries.nodePort | Optional | 30002 | Specify the port used to expose COE service outside cluster for timeseries endpoint. |
| coe.json_trans_rate_limiting.enabled | Optional | false | Set true to enable rate-limiting of transactions for JSON-based endpoints: Splunk, ElasticSearch and Zipkin. |
| coe.json_trans_rate_limiting.limit | Optional | 100 | Specify the rate-limit: 100 means approximately 800 TPS. |
| coe.json_trans_rate_limiting.queuelimit | Optional | 1000 | The amount of transactional data that can pile up, before COE starts shedding them. For Zipkin, 1000 is approximately 64 MB of data; For Splunk and ElasticSearch, this is approximately 32 MB of data. |
| coe.json_trans_rate_limiting.window | Optional | 5 | The recalculation window in seconds-  the lower the window size ( must be greater than 0), the more effective will be the rate-limiting but it will have CPU overhead |

Alternatively, you can define a YAML file with the values for the parameters and pass the values while installing the chart.

For example:
   ```
   helm install my-release citrix/citrix-cloud-native -f values.yaml
   ```
> **Note:**
> 1. It might be required to expose COE using nodePort. In such case, nodePort service can also be created additionally using the set option 'coe.nodePortRequired=true'
> 3. It might be required to stream only transactional data, without streaming timeseries or tracing data:
>      - For disabling timeseries, set the option 'coe.timeseries.enabled=false'
>      - For disabling tracing, set the option 'coe.ns_tracing.enabled=false' and do not set 'coe.ns_tracing.server'

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
