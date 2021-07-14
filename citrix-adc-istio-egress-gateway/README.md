
# Deploy Citrix ADC as an egress Gateway in Istio environment using Helm charts

Citrix Application Delivery Controller (ADC) can be deployed as an Istio Egress Gateway to control the egress traffic to Istio service mesh.

# Table of Contents
1. [TL; DR;](#tldr)
2. [Introduction](#introduction)
3. [Deploy Citrix ADC VPX or MPX as an Egress Gateway](#deploy-citrix-adc-vpx-or-mpx-as-an-egress-gateway)
4. [Deploy Citrix ADC CPX as an Egress Gateway](#deploy-citrix-adc-cpx-as-an-egress-gateway)
5. [Visualizing statistics of Citrix ADC Egress Gateway with Metrics Exporter](#visualizing-statistics-of-citrix-adc-Egress-gateway-with-metrics-exporter)
6. [Citrix ADC CPX License Provisioning](#citrix-adc-cpx-license-provisioning)
7. [Service Graph configuration](#configuration-for-servicegraph)
8. [Generate Certificate for Egress Gateway](#generate-certificate-for-egress-gateway)
9. [Citrix ADC as Egress Gateway: a sample deployment](#citrix-adc-as-egress-gateway-a-sample-deployment)
10. [Uninstalling the Helm chart](#uninstalling-the-helm-chart)
11. [Configuration Parameters](#configuration-parameters)
## <a name="tldr">TL; DR;</a>
  
### To deploy Citrix ADC VPX or MPX as an Egress Gateway:

       kubectl create secret generic nsloginegress --from-literal=username=<citrix-adc-user> --from-literal=password=<citrix-adc-password> -n citrix-system

       helm repo add citrix https://citrix.github.io/citrix-helm-charts/

**For Istio v1.9/v1.8**

       helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=YES --set egressGateway.netscalerUrl=https://<nsip>[:port] --set egressGateway.vserverIP=<IPv4 Address> --set secretName=nsloginegress

**For Istio v1.6.4**

       helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=YES --set egressGateway.netscalerUrl=https://<nsip>[:port] --set egressGateway.vserverIP=<IPv4 Address> --set secretName=nsloginegress --version 1.6.4

### To deploy Citrix ADC CPX as an Egress Gateway:

       helm repo add citrix https://citrix.github.io/citrix-helm-charts/

**For Istio v1.9/v1.8**

       helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=true --set citrixCPX=true

**For Istio v1.6.4**

       helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=true --set citrixCPX=true --version 1.6.4


## <a name="introduction">Introduction</a>

    This chart deploys Citrix CPX as an Egress Gateway. An egress gateway defines the exit point from the mesh. It provides features like load balancing at the edge of the mesh, monitoring, and routing rules to exiting the mesh. 

### Prerequisites

The following prerequisites are required for deploying Citrix ADC as an Egress Gateway in Istio service mesh:

- Ensure that **Istio version 1.6.0 onwards**  is installed
- Ensure that Helm with version 3.x is installed. Follow this [step](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md) to install the same.
- **For deploying Citrix ADC VPX or MPX as an Egress gateway:**

  Create a Kubernetes secret for the Citrix ADC user name and password using the following command:
  
        kubectl create secret generic nsloginegress --from-literal=username=<citrix-adc-user> --from-literal=password=<citrix-adc-password> -n citrix-system
- Ensure that your cluster has Kubernetes version 1.14.0 or later and the `admissionregistration.k8s.io/v1beta1` API is enabled

- **Registration of Citrix ADC CPX in ADM**

Create a secret for ADM username and password

        kubectl create secret generic admloginegress --from-literal=username=<adm-username> --from-literal=password=<adm-password> -n citrix-system

- **Important Note:** For deploying Citrix ADC VPX or MPX as egress gateway, you should establish the connectivity between Citrix ADC VPX or MPX and cluster nodes. This connectivity can be established by configuring routes on Citrix ADC as mentioned [here](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network/staticrouting.md) or by deploying [Citrix Node Controller](https://github.com/citrix/citrix-k8s-node-controller).

## <a name="deploy-citrix-adc-vpx-or-mpx-as-an-egress-gateway">Deploy Citrix ADC VPX or MPX as an Egress Gateway</a>

 To deploy Citrix ADC VPX or MPX as an Egress Gateway in the Istio service mesh, do the following step. In this example, release name is specified as `citrix-adc-istio-egress-gateway` and namespace as `citrix-system`.

        kubectl create secret generic nsloginegress --from-literal=username=<citrix-adc-user> --from-literal=password=<citrix-adc-password> -n citrix-system
        
        helm repo add citrix https://citrix.github.io/citrix-helm-charts/

        helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=YES,egressGateway.netscalerUrl=https://<nsip>[:port],egressGateway.vserverIP=<IPv4 Address> --set secretName=nsloginegress
## <a name="deploy-citrix-adc-cpx-as-an-egress-gateway">Deploy Citrix ADC CPX as an Egress Gateway</a>

 To deploy Citrix ADC CPX as an egress Gateway, do the following step. In this example, release name is specified as `citrix-adc-istio-egress-gateway` and namespace is used as `citrix-system`.

        helm repo add citrix https://citrix.github.io/citrix-helm-charts/

        helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=true --set citrixCPX=true

## <a name="visualizing-statistics-of-citrix-adc-Egress-gateway-with-metrics-exporter">Visualizing statistics of Citrix ADC Egress Gateway with Metrics Exporter</a>

By default, [Citrix ADC Metrics Exporter](https://github.com/citrix/citrix-adc-metrics-exporter) is also deployed along with Citrix ADC Egress Gateway. Citrix ADC Metrics Exporter fetches statistical data from Citrix ADC and exports it to Prometheus running in Istio service mesh. When you add Prometheus as a data source in Grafana, you can visualize this statistical data in the Grafana dashboard.

Metrics Exporter requires the IP address of Citrix ADC CPX or VPX as Egress Gateway. It is retrieved from the value specified for `EgressGateway.netscalerUrl`.

When Citrix ADC CPX is deployed as Egress Gateway, Metrics Exporter runs along with Citrix CPX Egress Gateway in the same pod and specifying IP address is optional.

To deploy Citrix ADC CPX as Egress Gateway without Metrics Exporter, set the value of `metricExporter.required` as false.

  
        helm repo add citrix https://citrix.github.io/citrix-helm-charts/

        helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=YES --set citrixCPX=true --set metricExporter.required=false

To deploy Citrix ADC VPX or MPX as Egress Gateway without Metrics Exporter, set the value of `metricExporter.required` as false.


        kubectl create secret generic nsloginegress --from-literal=username=<citrix-adc-user> --from-literal=password=<citrix-adc-password> -n citrix-system
    
        helm repo add citrix https://citrix.github.io/citrix-helm-charts/

        helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=YES,egressGateway.netscalerUrl=https://<nsip>[:port],egressGateway.vserverIP=<IPv4 Address>,metricExporter.required=false,secretName=nsloginegress

"Note:" To remotely access telemetry addons such as Prometheus and Grafana, see [Remotely Accessing Telemetry Addons](https://istio.io/docs/tasks/telemetry/gateways/).

## <a name="generate-certificate-for-egress-gateway">Generate Certificate for Egress Gateway </a>

Citrix Egress gateway needs TLS certificate-key pair for establishing secure communication channel with applications. Earlier these certificates were issued by Istio Citadel and bundled in Kubernetes secret. Certificate was loaded in the application pod by doing volume mount of secret. Now `xDS-Adaptor` can generate its own certificate and get it signed by the Istio Citadel (Istiod). This eliminates the need of secret and associated [risks](https://kubernetes.io/docs/concepts/configuration/secret/#risks). 

xDS-Adaptor needs to be provided with details Certificate Authority (CA) for successful signing of Certificate Signing Request (CSR). By default, CA is `istiod.istio-system.svc` which accepts CSRs on port 15012. 
To skip this process, don't provide any value (empty string) to `certProvider.caAddr`.
```
        helm repo add citrix https://citrix.github.io/citrix-helm-charts/

        helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=YES --set citrixCPX=true --set certProvider.caAddr=""
```
### <a name="using-third-party-service-account-tokens">Configure Third Party Service Account Tokens</a>

In order to generate certificate for application workload, xDS-Adaptor needs to send valid service account token along with Certificate Signing Request (CSR) to the Istio control plane (Citadel CA). Istio control plane authenticates the xDS-Adaptor using this JWT. 
Kubernetes supports two forms of these tokens:

* Third party tokens, which have a scoped audience and expiration.
* First party tokens, which have no expiration and are mounted into all pods.
 
 If Kubernetes cluster is installed with third party tokens, then the same information needs to be provided for automatic sidecar injection by passing `--set certProvider.jwtPolicy="third-party-jwt"`. By default, it is `first-party-jwt`.

```
        helm repo add citrix https://citrix.github.io/citrix-helm-charts/

        helm install cpx-sidecar-injector citrix/citrix-cpx-istio-sidecar-injector --namespace citrix-system --set cpxProxy.EULA=YES --set certProvider.caAddr="istiod.istio-system.svc" --set certProvider.jwtPolicy="third-party-jwt"

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

## <a name="citrix-adc-cpx-license-provisioning">**Citrix ADC CPX License Provisioning**</a>
By default, CPX runs with 20 Mbps bandwidth called as [CPX Express](https://www.citrix.com/en-in/products/citrix-adc/cpx-express.html) however for better performance and production deployment customer needs licensed CPX instances. [Citrix ADM](https://www.citrix.com/en-in/products/citrix-application-delivery-management/) is used to check out licenses for Citrix ADC CPX.

**Bandwidth based licensing**
For provisioning licensing on Citrix ADC CPX, it is mandatory to provide License Server information to CPX. This can be done by setting **ADMSettings.licenseServerIP** as License Server IP. In addition to this, **ADMSettings.bandWidthLicense** needs to be set true and desired bandwidth capacity in Mbps should be set **ADMSettings.bandWidth**.
For example, to set 2Gbps as bandwidth capacity, below command can be used.

    helm repo add citrix https://citrix.github.io/citrix-helm-charts/

    helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=YES --set ADMSettings.licenseServerIP=<Licenseserver_IP>,ADMSettings.bandWidthLicense=True --set ADMSettings.bandWidth=2000 --set citrixCPX=true

## <a name="configuration-for-servicegraph">**Service Graph configuration**</a>
   Citrix ADM Service graph is an observability tool that allows user to analyse service to service communication. The service graph is generated by ADM post collection of transactional data from registered Citrix ADC instances. More details about it can be found [here](https://docs.citrix.com/en-us/citrix-application-delivery-management-service/application-analytics-and-management/service-graph.html).
   Citrix ADC needs to be provided with ADM details for registration and data export. This section lists the steps needed to deploy Citrix ADC and register it with ADM.

**Deploy Citrix ADC CPX as egress gateway**
   1. Create secret using Citrix ADM Agent credentials, which will be used by Citrix ADC CPX to communicate with Citrix ADM Agent:

	kubectl create secret generic admlogin --from-literal=username=<adm-agent-username> --from-literal=password=<adm-agent-password>

   2. Deploy Citrix ADC CPX as egress gateway using helm command with `ADM` deatils:

	helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=true --set citrixCPX=true --set ADMSettings.ADMIP=<ADM-Agent-IP>

> **Note:**
> If container agent is being used here for Citrix ADM, specify `PodIP` of container agent in the `ADMSettings.ADMIP` parameter.

**Deploy Citrix ADC VPX/MPX as egress gateway**

   Deploy Citrix ADC VPX/MPX as egress gateway using the following helm command and set analytics settings on Citrix ADC VPX/MPX for sending transaction metrics to Citrix ADM
	
	helm install citrix-adc-istio-egress-gateway citrix/citrix-adc-istio-egress-gateway --namespace citrix-system --set egressGateway.EULA=YES --set egressGateway.netscalerUrl=https://<nsip>[:port] --set egressGateway.vserverIP=<IPv4 Address> --set secretName=nsloginegress	

   Add the following configurations in Citrix ADC VPX/MPX

        en ns mode ulfd

        en ns feature appflow

        add appflow collector logproxy_lstreamd -IPAddress <ADM-AGENT-IP/POD-IP> -port 5557 -Transport logstream

        set appflow param -templateRefresh 3600 -httpUrl ENABLED -httpCookie ENABLED -httpReferer ENABLED -httpMethod ENABLED -httpHost ENABLED -httpUserAgent ENABLED -httpContentType ENABLED -httpAuthorization ENABLED -httpVia ENABLED -httpXForwardedFor ENABLED -httpLocation ENABLED -httpSetCookie ENABLED -httpSetCookie2 ENABLED -httpDomain ENABLED -httpQueryWithUrl ENABLED  metrics ENABLED -events ENABLED -auditlogs ENABLED

        add appflow action logproxy_lstreamd -collectors logproxy_lstreamd

        add appflow policy logproxy_policy true logproxy_lstreamd

        bind appflow global logproxy_policy 10 END -type REQ_DEFAULT

        bind appflow global logproxy_policy 10 END -type OTHERTCP_REQ_DEFAULT


> **Note:**
> If container agent is being used here for Citrix ADM, please provide `PodIP` of container agent.


## <a name="citrix-adc-as-egress-gateway-a-sample-deployment">Citrix ADC as Egress Gateway: a sample deployment</a>

A sample deployment of Citrix ADC as an Egress gateway to excess external services is provided [here](https://github.com/citrix/citrix-helm-charts/tree/master/examples/citrix-adc-egress-in-istio).

## <a name="uninstalling-the-helm-chart">Uninstalling the Helm chart</a>

To uninstall or delete a chart with release name as `citrix-adc-istio-egress-gateway`, do the following step.

        helm uninstall citrix-adc-istio-egress-gateway -n citrix-system

The command removes all the Kubernetes components associated with the chart and deletes the release.

## <a name="configuration-parameters">Configuration parameters</a>

The following table lists the configurable parameters in the Helm chart and their default values.

| Parameter                      | Description                   | Default                   | Optional/Mandatory                  |
|--------------------------------|-------------------------------|---------------------------|---------------------------|
| `citrixCPX`                    | Citrix ADC CPX                    | FALSE                  | Mandatory for Citrix ADC CPX |
| `xDSAdaptor.image`            | Image of the Citrix xDS adaptor container |quay.io/citrix/citrix-xds-adaptor:0.9.8 | Mandatory|
| `xDSAdaptor.imagePullPolicy`   | Image pull policy for xDS adaptor | IfNotPresent       | Optional|
| `xDSAdaptor.secureConnect`     | If this value is set to true, xDS-adaptor establishes secure gRPC channel with Istio Pilot   | TRUE                       | Optional|
| `xDSAdaptor.logLevel`   | Log level to be set for xDS-adaptor log messages. Possible values: TRACE (most verbose), DEBUG, INFO, WARN, ERROR (least verbose) | DEBUG       | Optional|
| `xDSAdaptor.jsonLog`   | Set this argument to true if log messages are required in JSON format | false       | Optional|
| `coe.coeURL`          | Name of [Citrix Observability Exporter](https://github.com/citrix/citrix-observability-exporter) Service in the form of "<servicename>.<namespace>"  | null            | Optional|
| `coe.coeTracing`          | Use COE to send appflow transactions to Zipkin endpoint. If it is set to true, ADM servicegraph (if configured) can be impacted.  | false           | Optional|
| `ADMSettings.ADMIP `          | Citrix Application Delivery Management (ADM) IP address  | null            | Mandatory for Citrix ADC CPX |
| `ADMSettings.licenseServerIP `          | Citrix License Server IP address  | null            | Optional |
| `ADMSettings.licenseServerPort` | Citrix ADM port if a non-default port is used                                                                                        | 27000                                                                 | Optional|
| `ADMSettings.bandWidth`          | Desired bandwidth capacity to be set for Citrix ADC CPX in Mbps  | null            | Optional |
| `ADMSettings.bandWidthLicense`          | To specify bandwidth based licensing  | false            | Optional |
 `egressGateway.netscalerUrl`       | URL or IP address of the Citrix ADC which Istio-adaptor configures (Mandatory if citrixCPX=false)| null   |Mandatory for Citrix ADC MPX or VPX|
| `egressGateway.vserverIP`       | Virtual server IP address on Citrix ADC (Mandatory if citrixCPX=false) | null | Mandatory for Citrix ADC MPX or VPX|
| `egressGateway.adcServerName `          | Citrix ADC ServerName used in the Citrix ADC certificate  | null            | Optional |
| `egressGateway.image`             | Image of Citrix ADC CPX designated to run as egress Gateway                                                                       |quay.io/citrix/citrix-k8s-cpx-ingress:13.0-79.64 |   Mandatory for Citrix ADC CPX |
| `egressGateway.imagePullPolicy`   | Image pull policy                                                                                                                  | IfNotPresent                                                          | Optional|
| `egressGateway.mgmtHttpPort`      | Management port of the Citrix ADC CPX                                                                                              | 9080                                                                  | Optional|
| `egressGateway.mgmtHttpsPort`    | Secure management port of Citrix ADC CPX                                                                                           | 9443                                                                  | Optional|
| `egressGateway.EULA`             | End User License Agreement(EULA) terms and conditions. If yes, then user agrees to EULA terms and conditions.                                     | false                                                                    | Mandatory for Citrix ADC CPX
| `egressGateway.label` | Custom label for the egress Gateway service                                                                                       | citrix-egressgateway                                                                 |Optional|
| `istioPilot.name`                 | Name of the Istio Pilot (Istiod) service                                                                                                        | istiod                                                           |Optional|
| `istioPilot.namespace`     | Namespace where Istio Pilot is running                                                                                        | istio-system                                                          |Optional|
| `istioPilot.secureGrpcPort`       | Secure GRPC port where Istiod (Istio Pilot) is listening (default setting)                                                                  | 15012                                                                 |Optional|
| `istioPilot.insecureGrpcPort`      | Insecure GRPC port where Istio Pilot is listening                                                                                  | 15010                                                                 |Optional|
| `istioPilot.SAN`                 | Subject alternative name for Istio Pilot which is the secure production identity framework for everyone (SPIFFE) ID of Istio Pilot                                                        | null |Optional|
| `metricExporter.required`          | Metrics exporter for Citrix ADC                                                                                                    | TRUE                                                                  |Optional|
| `metricExporter.image`             | Image of the Citrix ADC Metrics Exporter                                                                                   | quay.io/citrix/citrix-adc-metrics-exporter:1.4.8                             |Optional|
| `metricExporter.port`              | Port over which Citrix ADC Metrics Exporter collects metrics of Citrix ADC.                                                      | 8888                                                                  |Optional|
| `metricExporter.secure`            | Enables collecting metrics over TLS                                                                                                | YES                                                                    |Optional|
| `metricExporter.logLevel`          | Level of logging in Citrix ADC Metrics Exporter. Possible values are: DEBUG, INFO, WARNING, ERROR, CRITICAL                                       | ERROR                                                                 |Optional|
| `metricExporter.imagePullPolicy`   | Image pull policy for Citrix ADC Metrics Exporter                                                                                       | IfNotPresent|
| `certProvider.caAddr`   | Certificate Authority (CA) address issuing certificate to application                           | istiod.istio-system.svc                          | Optional |
| `certProvider.caPort`   | Certificate Authority (CA) port issuing certificate to application                              | 15012 | Optional |
| `certProvider.trustDomain`   | SPIFFE Trust Domain                         | cluster.local | Optional |
| `certProvider.certTTLinHours`   | Validity of certificate generated by xds-adaptor and signed by Istiod (Istio Citadel) in hours. Default is 30 days validity              | 720 | Optional |
| `certProvider.jwtPolicy`   | Service Account token type. Kubernetes platform supports First party tokens and Third party tokens.  | first-party-jwt | Optional |
| `secretName`   | Name of the Kubernetes secret holding Citrix ADC credentials | nsloginegress | Mandatory for Citrix ADC VPX/MPX |

