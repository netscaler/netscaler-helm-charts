# Citrix ADC as Egress Gateways for sample application

# Table of Contents
1. [Deploying Citrix ADC as Egress Gateway](#citrix-Egress-gateway)
2. [Deploying Citrix ADC Sidecar Injector](#citrix-sidecar-injector)
3. [Deploying Sample Example](#deploying-sample-example)
4. [Verification](#verification)
5. [Clean Up](#cleanup)


## <a name="citrix-egress-gateway">A) Deploying Citrix ADC as egress Gateway</a>

Follow the link "Deploy Citrix ADC as an Egress Gateway using Helm charts" in [deployment guide](https://github.com/citrix/citrix-istio-adaptor/tree/master/docs/istio-integration#deployment-options).  

## <a name="citrix-sidecar-injector">B) Deploying Citrix ADC Sidecar Injector </a>

Follow the link "Deploy Citrix ADC CPX as a sidecar using Helm charts" in [deployment guide](https://github.com/citrix/citrix-istio-adaptor/tree/master/docs/istio-integration#deployment-options).

## <a name="deploying-sample-example">C) Deploying Sample Example</a>
Deploy any sample application. In this example, `sleep` is deployed as sample application.


#### Enable Namespace for Sidecar Injection:

```
kubectl create namespace egressgateway-test
kubectl label ns egressgateway-test cpx-injection=enabled
```
_**NOTE:** To deploy sample application with Citrix ADC CPX as a sidecar automatically, label namespace with cpx-injection-enabled.
#### Deploy sleep appplication using yaml:
```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/sleep.yaml
```

### Egress gateway for HTTPS traffic

#### Configure ServiceEntry to allow direct traffic to external service.
```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/serviceentry_tls.yaml
```


#### Configure Egress Gateway 
Create egress gateways for _edition.cnn.com_, port 443, and a destination rule for traffic directed to the egress gateway.

```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/gateway_tls.yaml
```     

#### Traffic Management using VirtualService and DestinationRule
Deploy virtual service to direct traffic from the sidecars to the egress gateway and from egress gateway to the external service. 

```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/virtual_service_tls.yaml
```


### Egress gateway for HTTP traffic

#### Configure ServiceEntry for HTTP
```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/serviceentry.yaml
```
    
#### Configure HTTP Gateway
```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/gateway.yaml
```

#### Configure VirtualService and DestinationRule
```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/virtual_service.yaml
```
*Note*: Aforementioned yaml files refer to _citrix-adc-istio-egress-gateway-citrix-egress-svc.citrix-system.svc.cluster.local_ as the host representating citrix-egressgateway service. The name of service depends on the helm-chart release name. Default name of release name is _citrix-adc-istio-egress-gateway_. In case of different release name, change the name of _host_ field accordingly.

    
## <a name="verification">D) Verification</a>
- Set the `SOURCE_POD` enviorment variable to the name of your source pod
```
    export SOURCE_POD=$(kubectl get pod -l app=sleep -o jsonpath={.items..metadata.name} -n egressgateway-test)
```    

### Verification for HTTPS traffic

- Verify that service is accessing external services via Citrix ADC CPX Egress Gateway

    ``` kubectl exec -it $SOURCE_POD -c sleep -n egressgateway-test -- curl -sL -o /dev/null -D - https://edition.cnn.com/politics ```

    ```
    ...
    HTTP/1.1 301 Moved Permanently
    ...
    location: https://edition.cnn.com/politics
    ...

    HTTP/2 200
    Content-Type: text/html; charset=utf-8
    ...
    ```
    
### Verification for HTTP traffic
- Verify that service is accessing external services via Citrix ADC CPX Egress Gateway

    ``` kubectl exec -it $SOURCE_POD -c sleep -n egressgateway-test -- curl -sL -o /dev/null -D - http://edition.cnn.com/politics ```

    ```
    ...
    HTTP/1.1 301 Moved Permanently
    ...
    location: http://edition.cnn.com/politics
    ...

    HTTP/2 200
    Content-Type: text/html; charset=utf-8
    ...
    ```
    


## <a name="cleanup">E) Clean Up </a>


### Cleanup using yaml files

Delete the Gateway configuration, VirtualService, DestinationRule and the secret, and shutdown the sleep application.

#### Cleanup HTTPS Gateway

```
kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/sleep.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/serviceentry_tls.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/gateway_tls.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/virtual_service_tls.yaml

kubectl delete ns egressgateway-test

```

#### Cleanup HTTP Gateway

```
kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/sleep.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/serviceentry.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/gateway.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/virtual_service.yaml

kubectl delete ns egressgateway-test

```

