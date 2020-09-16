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

## <a name="deploying-sample-example ">C) Deploying Sample Example</a>
Deploy any sample application. In this example, `sleep` is deployed as sample application.


##### Enable Namespace for Sidecar Injection:

```
kubectl Create namespace egressgateway-test
kubectl label ns egressgateway-test cpx-injection=enabled
```
_**NOTE:** To deploy sample application with Citrix ADC CPX as a sidecar automatically, label namespace with cpx-injection-enabled.
##### Deploy sleep appplication using yaml:
```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/sleep.yaml
```

#### Configure ServiceEntry to allow direct traffic to external service.
##### Configure ServiceEntry for HTTPS
```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/serviceentry_tls.yaml
```
##### Configure ServiceEntry for HTTP
```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/serviceentry.yaml
```

### Configure Egress Gateway 
Create egress gateways for _edition.cnn.com_, port 80/443, and a destination rule for traffic directed to the egress gateway.
##### Configure HTTPS Gateway
```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/gateway_tls.yaml
```     
    
##### Configure HTTP Gateway
```
kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/gateway.yaml
```
### Traffic Management using VirtualService and DestinationRule
Deploy virtual service to direct traffic from the sidecars to the egress gateway and from egress gateway to the external service. 
##### Configure HTTPS
```
kubectl apply -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/virtual_service_tls.yaml
```
##### Configure HTTP
```
kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/virtual_service.yaml
```
    
## <a name="verification">D) Verification</a>
1.Set the `SOURCE_POD` enviorment variable to the name of your source pod
```
    export SOURCE_POD=$(kubectl get pod -l app=sleep -o jsonpath={.items..metadata.name} -n egressgateway-test)
```    
2. kubectl exec -it $SOURCE_POD -c sleep -n egressgateway-test -- curl -sL -o /dev/null -D - http://edition.cnn.com/politics
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
3. check end point created for service inside Citrix ADC.

    kubectl exec -it <egress-gateway-pod\> -n <namspaces\> -c citrix-egressgateway bash

4. Verify that service is accessing external services via Citrix ADC CPX Egress Gateway. It can be confirmed by checking the hits of associated config entities (CS vserver, CS action) on the ADC.
 ```
root@citrix-egressgateway-77c9bb667c-ffdv7:/# cli_script.sh "sh cs action"
exec: sh cs action
1)      Name: ns_0_0_0_0_80_10
        Target LB Vserver: outbound_80__edition_cnn_com
        Hits: 1
        Undef Hits: 0
        Action Reference Count: 1

Done
```
## <a name="cleanup">E) Clean Up </a>


### Cleanup using yaml files

Delete the Gateway configuration, VirtualService, DestinationRule and the secret, and shutdown the sleep application.

```
kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/sleep.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/serviceentry_tls.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/gateway_tls.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/virtual_service_tls.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/serviceentry.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/gateway.yaml

kubectl delete -n egressgateway-test -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/citrix-adc-egress-in-istio/egress-example/deployment-yamls/virtual_service.yaml

kubectl delete ns egressgateway-test

```
