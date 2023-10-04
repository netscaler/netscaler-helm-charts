# Deploy NetScaler CPX as a sidecar in Istio environment using Helm charts

NetScaler CPX can be deployed as a sidecar proxy in an application pod in the Istio service mesh.


# Table of Contents
1. [TL; DR;](#tldr)
2. [Introduction](#introduction)
3. [Deploy Sidecar Injector for NetScaler CPX using Helm chart](#deploy-sidecar-injector-for-citrix-adc-cpx-using-helm-chart)
4. [Observability using NetScaler Observability Exporter](#observability-using-coe)
5. [NetScaler CPX License Provisioning](#citrix-adc-cpx-license-provisioning)
6. [Service Graph Configuration](#configuration-for-servicegraph)
7. [Generate Certificate for Application](#generate-certificate-for-application)
8. [Limitations](#limitations)
9. [Clean Up](#clean-up)
10. [Configuration Parameters](#configuration-parameters)


## <a name="tldr">TL; DR;</a>

    kubectl create namespace netscaler-system
    
    helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/
    
    helm install cpx-sidecar-injector netscaler/citrix-cloud-native --namespace netscaler-system --set iaSidecar.enabled=true --set iaSidecar.cpxProxy.EULA=YES
## <a name="introduction">Introduction</a>

NetScaler CPX can act as a sidecar proxy to an application container in Istio. You can inject the NetScaler CPX manually or automatically using the [Istio sidecar injector](https://istio.io/docs/setup/kubernetes/additional-setup/sidecar-injection/). Automatic sidecar injection requires resources including a Kubernetes [mutating webhook admission](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/) controller, and a service. Using this Helm chart, you can create resources required for automatically deploying NetScaler CPX as a sidecar proxy.

In Istio servicemesh, the namespace must be labelled before applying the deployment yaml for [automatic sidecar injection](https://istio.io/docs/setup/kubernetes/additional-setup/sidecar-injection/#automatic-sidecar-injection). Once the namespace is labelled, sidecars (envoy or CPX) will be injected while creating pods.
- For CPX, namespace must be labelled `cpx-injection=enabled`
- For Envoy, namespace must be labelled `istio-injection=enabled`

__Note: If a namespace is labelled with both `istio-injection` and `cpx-injection`, Envoy injection takes a priority! NetScaler CPX won't be injected on top of the already injected Envoy sidecar. For using NetScaler as sidecar, ensure that `istio-injection` label is removed from the namespace.__

For detailed information on different deployment options, see [Deployment Architecture](https://github.com/netscaler/netscaler-xds-adaptor/blob/master/docs/istio-integration/architecture.md).

### Compatibility Matrix between NetScaler xDS-adaptor and Istio version

Below table provides info about recommended NetScaler xDS-Adaptor version to be used for various Istio versions.

| NetScaler xDS-Adaptor version | Istio version |
|----------------------------|---------------|
| quay.io/citrix/citrix-xds-adaptor:0.10.3 | Istio v1.14+ |
| quay.io/citrix/citrix-xds-adaptor:0.10.1 | Istio v1.12 to Istio v1.13 |
| quay.io/citrix/citrix-xds-adaptor:0.9.9 | Istio v1.10 to Istio v1.11 |
| quay.io/citrix/citrix-xds-adaptor:0.9.8 | Istio v1.8 to Istio v1.9 |
| quay.io/citrix/citrix-xds-adaptor:0.9.5 | Istio v1.6 |

### Prerequisites

The following prerequisites are required for deploying NetScaler as a sidecar to an application pod.

- Ensure that **Istio version 1.8 onwards** is installed
- Ensure that Helm with version 3.x is installed. Follow this [step](https://github.com/netscaler/netscaler-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.
- Ensure that your cluster Kubernetes version should be 1.16 onwards and the `admissionregistration.k8s.io/v1`, `admissionregistration.k8s.io/v1beta1` API is enabled

You can verify the API by using the following command:

        kubectl api-versions | grep admissionregistration.k8s.io/v1

The following output indicates that the API is enabled:

        admissionregistration.k8s.io/v1
        admissionregistration.k8s.io/v1beta1

- Create namespace `netscaler-system`
        
        kubectl create namespace netscaler-system
        
- **Registration of NetScaler CPX in ADM**

Create a secret containing ADM username and password in each application namespace.

        kubectl create secret generic admlogin --from-literal=username=<adm-username> --from-literal=password=<adm-password> -n netscaler-system


## <a name="deploy-sidecar-injector-for-citrix-adc-cpx-using-helm-chart">Deploy Sidecar Injector for NetScaler CPX using Helm chart</a>

**Before you Begin**

To deploy resources for automatic installation of NetScaler CPX as a sidecar in Istio, perform the following step. In this example, release name is specified as `cpx-sidecar-injector`  and namespace is used as `netscaler-system`.


    helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

    helm install cpx-sidecar-injector netscaler/citrix-cloud-native --namespace netscaler-system --set iaSidecar.enabled=true,iaSidecar.cpxProxy.EULA=YES

This step installs a mutating webhook and a service resource to application pods in the namespace labeled as `cpx-injection=enabled`.

*"Note:" The `cpx-injection=enabled` label is mandatory for injecting sidecars.*

An example to deploy application along with NetScaler CPX sidecar is provided [here](https://github.com/netscaler/netscaler-helm-charts/tree/master/examples/citrix-adc-in-istio).


# <a name="observability-using-coe"> Observability using NetScaler Observability Exporter </a>

### Pre-requisites

1. NetScaler Observability Exporter (NSOE) should be deployed in the cluster.

2. NetScaler CPX should be running with versions 13.0-48+ or 12.1-56+.

NetScaler CPXes serving East West traffic send its metrics and transaction data to NSOE which has a support for Prometheus and Zipkin. 

Metrics data can be visualized in Prometheus dashboard. 

Zipkin enables users to analyze tracing for East-West service to service communication.

*Note*: Istio should be [installed](https://istio.io/docs/tasks/observability/distributed-tracing/zipkin/#before-you-begin) with Zipkin as tracing endpoint.

```
helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

helm install cpx-sidecar-injector netscaler/citrix-cloud-native --namespace netscaler-system --set iaSidecar.enabled=true,iaSidecar.cpxProxy.EULA=YES,iaSidecar.coe.coeURL=<coe-service-name>.<namespace>
```

By default, NSOE is primarily used for Prometheus integration. Servicegraph and tracing is handled by NetScaler ADM appliance. To enable Zipkin tracing, set argument `coe.coeTracing=true` in helm command. Default value of coeTracing is set to false.

```
helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

helm install cpx-sidecar-injector netscaler/citrix-cloud-native --namespace netscaler-system --set iaSidecar.enabled=true,iaSidecar.cpxProxy.EULA=YES,iaSidecar.coe.coeURL=<coe-service-name>.<namespace>,iaSidecar.coe.coeTracing=true

```

For example, if NSOE is deployed as `coe` in `netscaler-system` namespace, then below helm command will deploy sidecar injector webhook which will be deploying NetScaler CPX sidecar proxies in application pods, and these sidecar proxies will be configured to establish communication channels with NSOE.

```
helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

helm install cpx-sidecar-injector netscaler/citrix-cloud-native --namespace netscaler-system --set iaSidecar.enabled=true,iaSidecar.cpxProxy.EULA=YES,iaSidecar.coe.coeURL=coe.netscaler-system
```

*Important*: Apply below mentioned annotations on NSOE deployment so that Prometheus can scrape data from NSOE.
```
        prometheus.io/scrape: "true"
        prometheus.io/port: "5563" # Prometheus port
```
## <a name="citrix-adc-cpx-license-provisioning">**NetScaler CPX License Provisioning**</a>
By default, CPX runs with 20 Mbps bandwidth called as [CPX Express](https://www.netscaler.com/platform/cpx-containerter performance and production deployment customer needs licensed CPX instances. [NetScaler ADM](https://docs.netscaler.com/en-us/citrix-application-delivery-management-service/ce/ce/ce/ce/) is used to check out licenses for NetScaler CPX.

**Bandwidth based licensing**
For provisioning licensing on NetScaler CPX, it is mandatory to provide License Server information to CPX. This can be done by setting **iaSidecar.ADMSettings.licenseServerIP** as License Server IP. In addition to this, **iaSidecar.ADMSettings.bandWidthLicense** needs to be set true and desired bandwidth capacity in Mbps should be set **iaSidecar.ADMSettings.bandWidth**.
For example, to set 2Gbps as bandwidth capacity, below command can be used.

```
helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

helm install cpx-sidecar-injector netscaler/citrix-cpx-istio-sidecar-injector --namespace netscaler-system --set iaSidecar.enabled=true,iaSidecar.cpxProxy.EULA=YES --set iaSidecar.ADMSettings.licenseServerIP=<licenseServer_IP>,iaSidecar.ADMSettings.bandWidthLicense=True --set iaSidecar.ADMSettings.bandWidth=2000

```
## <a name="configuration-for-servicegraph">**Service Graph Configuration**</a>
   NetScaler ADM Service graph is an observability tool that allows user to analyse service to service communication. The service graph is generated by ADM post collection of transactional data from registered NetScaler instances. More details about it can be found [here](https://docs.netscaler.com/en-us/citrix-application-delivery-management-service/application-analytics-and-management/service-graph.html).
   NetScaler needs to be provided with ADM details for registration and data export. This section lists the steps needed to deploy NetScaler and register it with ADM.

   1. Create secret using NetScaler ADM Agent credentials, which will be used by NetScaler as CPX to communicate with NetScaler ADM Agent:
	
	kubectl create secret generic admlogin --from-literal=username=<adm-agent-username> --from-literal=password=<adm-agent-password>

   2. Deploy NetScaler CPX sidecar injector using helm command with `ADM` details:

	helm install cpx-sidecar-injector netscaler/citrix-cloud-native --namespace netscaler-system --set iaSidecar.enabled=true --set iaSidecar.cpxProxy.EULA=YES --set iaSidecar.ADMSettings.ADMIP=<ADM-Agent-IP>

> **Note:**
> If container agent is being used here for NetScaler ADM, specify `serviceIP` of container agent in the `iaSidecar.ADMSettings.ADMIP` parameter.


## <a name="generate-certificate-for-application">Generate Certificate for Application </a>

Application needs TLS certificate-key pair for establishing secure communication channel with other applications. Earlier these certificates were issued by Istio Citadel and bundled in Kubernetes secret. Certificate was loaded in the application pod by doing volume mount of secret. Now `xDS-Adaptor` can generate its own certificate and get it signed by the Istio Citadel (Istiod). This eliminates the need of secret and associated [risks](https://kubernetes.io/docs/concepts/configuration/secret/#risks). 

xDS-Adaptor needs to be provided with details Certificate Authority (CA) for successful signing of Certificate Signing Request (CSR). By default, CA is `istiod.istio-system.svc` which accepts CSRs on port 15012. 
To skip this process, don't provide any value (empty string) to `iaSidecar.certProvider.caAddr`.
```
	helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

        helm install cpx-sidecar-injector netscaler/citrix-cpx-istio-sidecar-injector --namespace netscaler-system --set iaSidecar.enabled=true,iaSidecar.cpxProxy.EULA=YES --set iaSidecar.certProvider.caAddr=""
```

### <a name="using-third-party-service-account-tokens">Configure Third Party Service Account Tokens</a>

In order to generate certificate for application workload, xDS-Adaptor needs to send valid service account token along with Certificate Signing Request (CSR) to the Istio control plane (Citadel CA). Istio control plane authenticates the xDS-Adaptor using this JWT. 
Kubernetes supports two forms of these tokens:

* Third party tokens, which have a scoped audience and expiration.
* First party tokens, which have no expiration and are mounted into all pods.
 
 If Kubernetes cluster is installed with third party tokens, then the same information needs to be provided for automatic sidecar injection by passing `--set iaSidecar.certProvider.jwtPolicy="third-party-jwt"`. By default, it is `first-party-jwt`.

```
        helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/

        helm install cpx-sidecar-injector netscaler/citrix-cpx-istio-sidecar-injector --namespace netscaler-system --set iaSidecar.cpxProxy.EULA=YES --set iaSidecar.certProvider.caAddr="istiod.istio-system.svc" --set iaSidecar.certProvider.jwtPolicy="third-party-jwt"

```

To determine if your cluster supports third party tokens, look for the TokenRequest API using below command. If there is no output, then it is `first-party-jwt`. In case of `third-party-jwt`, output will be like below.

```
# kubectl get --raw /api/v1 | jq '.resources[] | select(.name | index("serviceaccounts/token"))'

{
    "name": "serviceaccounts/token",
    "singularName": "",
    "namespaced": true,
    "group": "authentication.k8s.io",
    "version": "v1",
    "kind": "TokenRequest",
    "verbs": [
        "create"
    ]
}

```

## <a name="limitations">Limitations</a>

NetScaler CPX occupies certain ports for internal usage. This makes application service running on one of these restricted ports incompatible with the NetScaler CPX.
The list of ports is mentioned below. NetScaler is working on delisting some of the major ports from the given list, and same shall be available in future releases.

#### Restricted Ports

| Sr No |Port Number|
|-------|-----------|
| 1 | 80 |
| 2 | 3010 |
| 3 | 5555 |
| 4 | 8080 |

## <a name="clean-up">Clean Up</a>

To delete the resources created for automatic injection with the release name  `cpx-sidecar-injector`, perform the following step.

    helm delete cpx-sidecar-injector

## <a name="configuration-parameters">Configuration parameters</a>

The following table lists the configurable parameters and their default values in the Helm chart.


| Parameter                      | Description                   | Default                   |
|--------------------------------|-------------------------------|---------------------------|
| `iaSidecar.enabled` | Mandatory | False | Set to "True" for deploying NetScaler CPX as a sidecar in Istio environment. |
| `iaSidecar.xDSAdaptor.imageRegistry`                | Image registry of the NetScaler xDS adaptor container               | `quay.io`               |     Mandatory                  |
| `iaSidecar.xDSAdaptor.imageRepository`              | Image repository of the NetScaler xDS adaptor container               | `citrix/citrix-xds-adaptor`               |    Mandatory                  |
| `iaSidecar.xDSAdaptor.imageTag`                     | Image tag of the NetScaler xDS adaptor container               | `0.10.3`               |   Mandatory                  |
| `iaSidecar.xDSadaptor.imagePullPolicy`   | Image pull policy for xDS-adaptor | IfNotPresent        |
| `iaSidecar.xDSadaptor.secureConnect`     | If this value is set to true, xDS-adaptor establishes secure gRPC channel with Istio Pilot   | TRUE                       |
| `iaSidecar.xDSAdaptor.logLevel`   | Log level to be set for xDS-adaptor log messages. Possible values: TRACE (most verbose), DEBUG, INFO, WARN, ERROR (least verbose) | DEBUG       | Optional|
| `iaSidecar.xDSAdaptor.jsonLog`   | Set this argument to true if log messages are required in JSON format | false       | Optional|
| `iaSidecar.xDSAdaptor.defaultSSLListenerOn443` | Create SSL vserver by default for LDS resource for 0.0.0.0 and port 443. If set to false, TCP vserver will be created in absence of TLSContext in tcp_proxy filter | true | Optional |
| `iaSidecar.coe.coeURL`          | Name of [NetScaler Observability Exporter](https://github.com/netscaler/netscaler-observability-exporter) Service in the form of _servicename.namespace_  | NIL            | Optional|
| `iaSidecar.coe.coeTracing`          | Use NSOE to send appflow transactions to Zipkin endpoint. If it is set to true, ADM servicegraph (if configured) can be impacted.  | false           | Optional|
| `iaSidecar.ADMSettings.ADMIP`     | Provide the NetScaler Application Delivery Management (ADM) IP address | NIL                       |
| `iaSidecar.ADMSettings.licenseServerIP `          | NetScaler License Server IP address  | NIL            | Optional |
| `iaSidecar.ADMSettings.licenseServerPort`   | NetScaler ADM port if a non-default port is used                                                                                      | 27000                                                          
|
| `iaSidecar.ADMSettings.bandWidth`          | Desired bandwidth capacity to be set for NetScaler CPX in Mbps  | 1000            | Optional |
| `iaSidecar.ADMSettings.bandWidthLicense`          | To specify bandwidth based licensing  | false            | Optional |
| `iaSidecar.ADMSettings.licenseEdition`| License edition that can be Standard, Platinum and Enterprise . By default, Platinum is selected | PLATINUM | optional |
| `iaSidecar.ADMSettings.analyticsServerPort` | Port used for Analytics in ADM. Required to plot ServiceGraph. | 5557   | Optional |
| `iaSidecar.istioPilot.name`                 | Name of the Istio Pilot (Istiod) service     | istiod                                                           |
| `iaSidecar.istioPilot.namespace`     | Namespace where Istio Pilot is running       | istio-system                                                          |
| `iaSidecar.istioPilot.secureGrpcPort`       | Secure GRPC port where Istio Pilot is listening (Default setting)                                                                  | 15012                                                                 |
| `iaSidecar.istioPilot.insecureGrpcPort`      | Insecure GRPC port where Istio Pilot is listening                                                                                  | 15010                                                                 |
| `iaSidecar.istioPilot.proxyType`      | Type of NetScaler associated with the xDS-adaptor. Possible values are: sidecar and router.                                                                              |   sidecar|
| `iaSidecar.istioPilot.SAN`                 | Subject alternative name for Istio Pilot which is the Secure Production Identity Framework For Everyone (SPIFFE) ID of Istio Pilot.                                   | null |
| `iaSidecar.cpxProxy.netscalerUrl`   |    URL or IP address of the NetScaler which will be configured by xDS-adaptor.                                                            | http://127.0.0.1 |
| `iaSidecar.cpxProxy.imageRegistry`                   | Image registry of NetScaler CPX designated to run as sidecar proxy              | `quay.io`               | 
| `iaSidecar.cpxProxy.imageRepository`                 | Image repository of NetScaler CPX designated to run as sidecar proxy             | `citrix/citrix-k8s-cpx-ingress`               |
| `iaSidecar.cpxProxy.imageTag`                  | Image tag of NetScaler CPX designated to run as sidecar proxy             | `13.1-30.52`               | 
| `iaSidecar.cpxProxy.imagePullPolicy`           | Image pull policy for NetScaler                                                                                  | IfNotPresent                                                               |
| `iaSidecar.cpxProxy.EULA`              |  End User License Agreement(EULA) terms and conditions. If yes, then user agrees to EULA terms and conditions.                                                     | NO |
| `iaSidecar.cpxProxy.cpxSidecarMode`            | Environment variable for NetScaler CPX. It indicates that NetScaler CPX is running as sidecar mode or not.                                                                                               | YES                                                                    |
| `iaSidecar.cpxProxy.cpxDisableProbe`            | Environment variable for NetScaler CPX. It indicates that NetScaler CPX will disable probing dynamic services. It should be enabled for multicluster setup. Possible values: YES/NO.                    | YES   |
| `iaSidecar.cpxProxy.cpxLicenseAggregator`            | IP/FQDN of the CPX License Aggregator if it is being used to license the CPX.                                                                                               | Null                                                                    | optional |
| `iaSidecar.cpxProxy.enableLabelsFeature` | If this variable is true, Istio's [subset](https://istio.io/latest/docs/reference/config/networking/destination-rule/#Subset) of the service and some metadata of the service such as servicename, namespace etc will be stored in the NetScaler that might be used for analytics purpose.                                                                                   | FALSE                                                                 |Optional|
| `iaSidecar.sidecarWebHook.webhookImageRegistry`                | Image registry of sidecarWebHook. Mutating webhook associated with the sidecar injector. It invokes a service `cpx-sidecar-injector` to inject sidecar proxies in the application pod.               | `quay.io`               | 
| `iaSidecar.sidecarWebHook.webhookImageRepository`              | Image repository of sidecarWebHook. Mutating webhook associated with the sidecar injector. It invokes a service `cpx-sidecar-injector` to inject sidecar proxies in the application pod.               | `citrix/cpx-istio-sidecar-injector`               |
| `iaSidecar.sidecarWebHook.webhookImageTag`                     | Image tag of sidecarWebHook. Mutating webhook associated with the sidecar injector. It invokes a service `cpx-sidecar-injector` to inject sidecar proxies in the application pod.               | `1.3.0`               |
| `iaSidecar.sidecarWebHook.imagePullPolicy`   | Image pull policy                                                                          |IfNotPresent|
| `iaSidecar.sidecarCertsGenerator.imageRegistry`                | Image registry of sidecarCertsGenerator. Certificate genrator image associated with sidecar injector. This image generates certificate and key needed for CPX sidecar injection.               | `quay.io`               | 
| `iaSidecar.sidecarCertsGenerator.imageRepository`              | Image repository of sidecarCertsGenerator. Certificate genrator image associated with sidecar injector. This image generates certificate and key needed for CPX sidecar injection.               | `citrix/cpx-sidecar-injector-certgen`               |
| `iaSidecar.sidecarCertsGenerator.imageTag`                     | Image tag of sidecarCertsGenerator. Certificate genrator image associated with sidecar injector. This image generates certificate and key needed for CPX sidecar injection.               | `1.2.0`               |
| `iaSidecar.sidecarCertsGenerator.imagePullPolicy`   | Image pull policy                                                                          |IfNotPresent|
| `iaSidecar.webhook.injectionLabelName` |  Label of namespace where automatic NetScaler CPX sidecar injection is required. | cpx-injection |
| `iaSidecar.certProvider.caAddr`   | Certificate Authority (CA) address issuing certificate to application                           | istiod.istio-system.svc                          | Optional |
| `iaSidecar.certProvider.caPort`   | Certificate Authority (CA) port issuing certificate to application                              | 15012 | Optional |
| `iaSidecar.certProvider.trustDomain`   | SPIFFE Trust Domain                         | cluster.local | Optional |
| `iaSidecar.certProvider.certTTLinHours`   | Validity of certificate generated by xds-adaptor and signed by Istiod (Istio Citadel) in hours. Default is 30 days validity              | 720 | Optional |
| `iaSidecar.certProvider.certTTLinHours`   | Validity of certificate generated by xds-adaptor and signed by Istiod (Istio Citadel) in hours. Default is 30 days validity              | 720 | Optional |
| `iaSidecar.certProvider.clusterId`   | clusterId is the ID of the cluster where Istiod CA instance resides (default Kubernetes). It can be different value on some cloud platforms or in multicluster environments. For example, in Anthos servicemesh, it might be of the format of `cn<project-name>-<region>-<cluster_name>`. In multiCluster environments, it is the value of global.multiCluster.clusterName provided during servicemesh control plane installation           | Kubernetes  | Optional |
| `iaSidecar.certProvider.jwtPolicy`   | Service Account token type. Kubernetes platform supports First party tokens and Third party tokens.  | first-party-jwt | Optional |
| `iaSidecar.certProvider.jwtPolicy`   | Service Account token type. Kubernetes platform supports First party tokens and Third party tokens. Usually public cloud based Kubernetes has third-party-jwt | null | Optional |

**Note:** You can use the `values.yaml` file packaged in the chart. This file contains the default configuration values for the chart.
