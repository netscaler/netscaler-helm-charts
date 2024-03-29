# NetScaler Cloud Native 

[NetScaler Cloud Native solutions]((https://docs.netscaler.com/en-us/citrix-adc/current-release/cloud-native-solution.html)) empower establishments to modernize their application delivery as well as application architecture. They leverage the advanced traffic management, observability, and comprehensive security features of NetScalers to ensure enterprise grade reliability and security. This helm chart enables user to do one touch deployment of one or more cloud native products created and managed by NetScaler in [Kubernetes](https://kubernetes.io/) or in [OpenShift](https://www.openshift.com) cluster.

This helm chart can be used to:
1. [Deploy NetScaler Ingress Controller for NetScaler VPX/MPX](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/citrix-ingress-controller/README.md)
2. [Deploy NetScaler CPX with NetScaler Ingress Controller running as sidecar](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/citrix-cpx-with-ingress-controller/README.md)
3. [Deploy NetScaler Node Controller](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/citrix-node-controller/README.md)
4. [Deploy NetScaler IPAM Controller](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/citrix-ipam-controller/README.md)
5. [Deploy Observability Exporter](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/citrix-observability-exporter/README.md)
6. [Deploy NetScaler as an Ingress Gateway in Istio environment](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/citrix-adc-istio-ingress-gateway/README.md)
7. [Deploy NetScaler CPX as a sidecar in Istio environment](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/citrix-cpx-istio-sidecar-injector/README.md)
8. [Deploy NetScaler GSLB Controller for NetScaler VPX/MPX](https://github.com/netscaler/netscaler-helm-charts/blob/master/citrix-cloud-native/charts/citrix-gslb-controller/README.md)
9. [Deploy NetScaler as an Egress Gateway in Istio environment](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/citrix-adc-istio-egress-gateway/README.md)
10. [Deploy ADM agent onboarding as Kubernetes Job](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/adm-agent-onboarding/README.md)

Depending on the architecture, it is sometimes needed to deploy multiple products in NetScaler portfolio together. This can be achieved by setting required parameters for all products together while installing those products using this helm chart.
For example, both NetScaler Ingress Controller and NetScaler CPX with NetScaler Ingress Controller as side car can be deployed using single helm install command as:

  Add the Helm Chart Repo:
  ```
  helm repo add netscaler https://netscaler.github.io/netscaler-helm-charts/
  ```
  Install:
  There are two ways to install this chart, either by providing all parameters required in the `helm install` command itself, for example:
  ```
  helm install cloud-native netscaler/citrix-cloud-native --set cic.enabled=true,cic.nsIP=<NSIP of NetScaler VPX/MPX>,cic.adcCredentialSecret=<Secret-for-NetScaler-credentials>,cic.license.accept=yes,cpx.enabled=true,cpx.license.accept=yes
  ```
  or all the required parameters can be set in [citrix_cloud_native_values.yaml](https://github.com/netscaler/netscaler-helm-charts/blob/master/citrix_cloud_native_values.yaml) and this yaml can be used to install the chart using command:
  ```
  helm install cloud-native netscaler/citrix-cloud-native -f citrix_cloud_native_values.yaml
  ```

For upgrading any existing deployment via this helm chart all the parameters that configures the desired state of system needs to be provided in the helm upgrade command.
For example, if NetScaler Ingress Controller is already deployed in the cluster using command:

  ```
  helm install citrix-ingress-controller netscaler/citrix-cloud-native --set cic.enabled=true,cic.nsIP=1.1.1.1,cic.adcCredentialSecret=nslogin,cic.license.accept=yes,cic.ingressClass[0]=citrix
  ```
then the NetScaler Ingress Controller image can be updated in the already existing deployment using command:

  ```
  helm upgrade citrix-ingress-controller netscaler/citrix-cloud-native --set cic.enabled=true,cic.nsIP=1.1.1.1,cic.adcCredentialSecret=nslogin,cic.license.accept=yes,cic.ingressClass[0]=citrix,cic.image=<new-image>
  ```
Alternatively, it is recommended to use same [citrix_cloud_native_values.yaml](https://github.com/netscaler/netscaler-helm-charts/blob/master/citrix_cloud_native_values.yaml) and modify the parameters necessary for upgrade. The yaml file can be used for upgrade like:

  ```
  helm upgrade citrix-ingress-controller netscaler/citrix-cloud-native -f citrix_cloud_native_values.yaml
  ```

-> **Important::**
-> Both the charts [NetScaler Ingress Controller](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/citrix-ingress-controller/R
EADME.md) and [NetScaler CPX with NetScaler Ingress Controller](https://github.com/netscaler/netscaler-helm-charts/tree/master/citrix-cloud-native/charts/citrix-cpx-w
ith-ingress-controller/README.md) contains all the CRDs that are supported by NetScaler. So whenever you are installing both these charts together please make sure you are deploying CRDs only once. You can do this either by setting `cic.crds.install=false` or by setting `cpx.crds.install=false`.
