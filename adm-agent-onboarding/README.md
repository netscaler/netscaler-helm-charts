# Deploy ADM agent onboarding as Kubernetes Job

[Kubernetes job](https://kubernetes.io/docs/concepts/workloads/controllers/job/) is an object that creates one or more pods and tracks the operations of pods. Kubernetes Jobs ensure that the specified number of pods are accomplished effectively. The job is considered complete when a specified number of successful run of pods is complete. 

You can deploy ADM agent onboarding as a Kubernetes Job helps you to deploy container-based Citrix ADM agent and also performs all the necessary settings in Citrix ADM for generating service graph.

# Table of Contents
1. [TL; DR;](#tldr)
2. [Introduction](#introduction)
3. [Generate authentication and authorization token from Access ID and Secret to access Citrix ADM](#generatetoken)
4. [Deploy ADM agent onboarding using Helm chart](#deploy-adm-agent-onboarding-using-helm-chart)
5. [Deploy ADM agent onboarding using Helm chart and register Citrix ADC VPX/MPX in Citrix ADM](#register-adc)
6. [Manual creating login secret for Citrix ADM Agent](#manual-secret)
7. [Automatic login secret for Citrix ADM Agent](#automatic-secret)
8. [Clean Up](#clean-up)
9. [Configuration Parameters](#configuration-parameters)


# <a name="tldr">TL; DR;</a>
**A) Deploy adm-agent-onboarding Kubernetes job**

**A.1) Generate authentication and authorization token from Access ID and Secret to access Citrix ADM** 

To generate the authentication and authorization bearer token using Access ID and secret see [this](#generatetoken).

**A.2) To create ADM Agent login Secret automatically, use the following command:**

	helm repo add citrix https://citrix.github.io/citrix-helm-charts
	helm install citrix-adm citrix/adm-agent-onboarding --namespace <namespace> --set token=<Token> 

**Note:** If you are deploying Citrix ADC CPX and Citrix ADM agent in different namespaces, please label namespace with `citrix-cpx=enabled` in which Citrix ADC CPX has been deployed. For more information, see [Create Secret automatically](#automatic-secret).

**A.2) To create Citrix ADM agent login Secret manually, use the following command:**

	kubectl create secret generic admlogin --from-literal=username=nsroot --from-literal=password=<adm-agent-password> -n <namespace>
	
	helm repo add citrix https://citrix.github.io/citrix-helm-charts
	helm install citrix-adm citrix/adm-agent-onboarding --namespace <namespace> --set admAgent.loginSecret=admlogin --set token=<Token>
	
**Note:** You must create `admlogin` in all the namespaces in which Citrix ADC CPX is deployed. 

**A.2) To create ADM Agent login Secret automatically and register Citrix ADC VPX/MPX in ADM, use the following command:**

	kubectl create secret generic nslogin  --from-literal=username=<ADC Username> --from-literal=password=<ADC password> -n <namespace>

	helm repo add citrix https://citrix.github.io/citrix-helm-charts
	helm install citrix-adm citrix/adm-agent-onboarding --namespace <namespace> --set adc.IP=<ADC ManagementIP>,adc.loginSecret=nslogin --set token=<Token>

**Note:** If you are deploying Citrix ADC CPX and Citrix ADM agent in different namespaces, please label namespace with `citrix-cpx=enabled` in which Citrix ADC CPX has been deployed. For more information, see [Create Secret automatically](#automatic-secret). `nslogin` is Kubernetes secret for credential of Citrix ADC VPX/MPX. Use the management IP address for the `adc.IP` argument.

**A.2) To create ADM Agent login Secret automatically and register Citrix ADC VPX/MPX in ADM, use the following command:**

	kubectl create secret generic nslogin  --from-literal=username=<ADC Username> --from-literal=password=<ADC password> -n <namespace>

	kubectl create secret generic admlogin --from-literal=username=nsroot --from-literal=password=<adm-agent-password> -n <namespace>
	
	helm repo add citrix https://citrix.github.io/citrix-helm-charts
	helm install citrix-adm citrix/adm-agent-onboarding --namespace <namespace> --set admAgent.loginSecret=admlogin --set adc.IP=<ADC ManagementIP>,adc.loginSecret=nslogin --set token=<Token>

**Note:** You must create `admlogin` in all the namespaces in which Citrix ADC CPX is deployed. `nslogin` is Kubernetes secret for credential of Citrix ADC VPX/MPX. Use the management IP address for the `adc.IP` argument.

# <a name="introduction">Introduction</a>

Citrix provides a Kubernetes Job known as ADM agent onboarding to simplify the container-based Citrix ADM agent deployment and ADM settings configurations required for generating service graph. This Kubernetes Job automatically downloads the YAML file required for the Citrix ADM agent, deploys it, and registers the cluster in Citrix ADM.

For example to generate Service Graph with SMLite, see [Service graph example](../examples/servicegraph). For example to generate Service Graph of Citrix intergration with Istio Service Mesh, see [Service graph with Citrix ADC Observability and ADM](../examples/servicegraph_with_coe_and_adm).

# Prerequisites

 - Ensure that you have a Citrix ADM account. To use Citrix ADM, you must create a [Citrix Cloud account](https://docs.citrix.com/en-us/citrix-cloud/overview/signing-up-for-citrix-cloud/signing-up-for-citrix-cloud). To manage Citrix ADM with an Express account, see [Getting Started](https://docs.citrix.com/en-us/citrix-application-delivery-management-service/getting-started.html#install-an-agent-as-a-microservice).

- Ensure that you  installed Kubernetes version 1.16 or later. For more information about Kubernetes installation, see [Kubernetes](https://kubernetes.io/).

- Ensure that you have installed Helm version 3.x. For information about Helm chart installation, see [Helm](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md).

 - Ensure that the ports described in the [Ports](https://docs.citrix.com/en-us/citrix-application-delivery-management-service/system-requirements.html#ports) document are open.

 - For registering Citrix ADC VPX or MPX in Citrix ADM using ADM agent onboarding, you should establish the connectivity between Citrix ADC VPX or MPX and cluster nodes. This connectivity can be established by configuring routes on Citrix ADC as described [here](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network/staticrouting.md) or by deploying [Citrix Node Controller](https://github.com/citrix/citrix-k8s-node-controller).

## <a name="generatetoken">**Generate Authentication and Authorization Token from Access ID and Secret**</a> 

Perform the following steps to get access ID and secret for accessing Citrix ADM:

1. Log in to Citrix Cloud account. 

2. On the left Menu panel, select **Identity and Access Management**.

   ![](images/menu.png)

3. Go to **API Access**.

    ![](images/apiaccess.png)

4. Specify the client name and click **Create Client**.

    ![](images/client-detail.png)

5. Download and save the `access-id` and `access-secret` generated.

    ![](images/downloads-secret.png)

  Now, you can generate `authorization bearer token` using access ID and access secret using below script: 

	wget  https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/generate_token.py
    
	python3 generate_token.py --accessID=<accessID> --accessSecret=<accessSecret>

**NOTE**: The bearer token expires in an hour (3600 seconds).

# <a name="deploy-adm-agent-onboarding-using-helm-chart">Deploy ADM agent onboarding using the Helm chart</a>

Before deploying the ADM agent onboarding, you must create a Kubernetes Secret containing the client ID and Secret to access Citrix ADM. For information about getting the access ID and secret for accessing Citrix ADM, see [Access ID and Secret to access Citrix ADM](#generatetoken). After the Secret has been created, use the following commands to deploy Citrix ADM Agent:

	helm repo add citrix https://citrix.github.io/citrix-helm-charts

	helm install citrix-adm citrix/adm-agent-onboarding --namespace <namespace>  --set token=<Token>    

It deploys the Kubernetes Job that deploys Citrix ADM Agent and registers the cluster on the Citrix ADM. it also performs the other settings required for servicegraph in Citrix ADM. It also deploys a sidecar along with Citrix ADM Agent which can create a Kubernetes Secret containing login credentials of Citrix ADM Agent automatically when namespace is labelled with `citrix-cpx=enabled`, more detail [here](#automatic-secret).

**Note:** If you do not want to run a sidecar, see [Create Secret manually for Citrix ADC agent](#manual-secret).

#  <a name="register-adc">Deploy ADM agent onboarding and register Citrix ADC VPX/MPX with Citrix ADM</a>

**Important Note:** For registering Citrix ADC VPX/MPX in Citrix ADM, you should establish the connectivity between Citrix ADC VPX or MPX and cluster nodes. This connectivity can be established by configuring routes on Citrix ADC as described in the document: [Static route on Ingress Citrix ADC](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network/staticrouting.md) or by deploying [Citrix node controller](https://github.com/citrix/citrix-k8s-node-controller).

To register Citrix ADC VPX/MPX with Citrix ADM, create a Kubernetes secret containing login credentials of Citrix ADC VPX/MPX in the namespace in which ADM agent onboarding Job will be functional. Use the following command:

	kubectl create secret generic nslogin --from-literal=username=<username> --from-literal=password=<adc-password> -n <namespace>

You have to pass the management IP address of Citrix ADC VPX/MPX as an environment variable: `adc.IP`.
	
	helm repo add citrix https://citrix.github.io/citrix-helm-charts

	helm install citrix-adm citrix/adm-agent-onboarding --namespace <namespace> --set adc.IP=<ADC ManagementIP>,adc.loginSecret=nslogin --set token=<Token>

**Note:** Using environment variables, you can specify the management HTTP port `adc.mgmtHTTPPort` and HTTPS port `adc.mgmtHTTPSPort` as 80 and 443 respectively.

#  <a name="manual-secret">Create login secret manually for Citrix ADM agent</a>

Citrix ADM agent login credentials are required by Citrix ADC CPX while registering itself to Citrix ADM. You can create it manually on all the namespaces in which Citrix ADC CPX will be deployed and also on the namespace in which the Citrix ADM agent Adaptor Kubernetes job will be created.

	kubectl create secret generic admlogin --from-literal=username=nsroot --from-literal=password=<adm-agent-password> -n <namespace> 

After the Secret has been created, you can deploy the Citrix ADM agent using the following command:

	helm install citrix-adm citrix/adm-agent-onboarding --namespace <namespace> --set admAgent.loginSecret=admlogin --set token=<Token>

# <a name="automatic-secret"> Automatic login secret for Citrix ADM agent</a>

Citrix ADM agent can create the secret for Citrix ADM agent and deploys a sidecar along with the Citrix ADM agent that creates the secret automatically whenever a namespace is labelled with `citrix-cpx=enabled`.

To label a namespace, use the following command:

	kubectl label namespace <namespace> citrix-cpx=enabled

# <a name="clean-up">Clean up</a>

To delete the resources created during the deployment of ADM agent onboarding `adm-agent-onboarding` with the release name  `citrix-adm`, use the following command:

	helm delete citrix-adm -n <namespace>

To delete Citrix ADM Agent pods and other resources use the following commands:

	kubectl delete deployment admagent -n <namespace>
	kubectl delete secret admagent -n <namespace>
	kubectl delete configmaps admagent -n <namespace>
	kubectl delete svc admagent -n <namespace>
	kubectl delete secret admlogin -n <namespace>
    kubectl delete secret nslogin -n <namespace>
    kubectl delete sa admagent -n <namespace>
    kubectl delete clusterroles admagent -n <namespace>
    kubectl delete clusterrolebindings admagent -n <namespace>

**NOTE** You need remove the Cluster and Agent from Citrix ADM UI manually.

# <a name="configuration-parameters">Configuration parameters</a>

The following table provides the configurable parameters and their default values in the Helm chart.

| Parameter                      | Description                   | Default                   |
|--------------------------------|-------------------------------|---------------------------|
| `imageRegistry`			   | Image registry of the ADM agent onboarding container               | `quay.io`               |
| `imageRepository`			   | Image repository of the ADM agent onboarding container               | `citrix/adm-agent-onboarding`               |
| `imageTag`			   | Image tag  of the ADM agent onboarding container               | `1.1.0`               |
| `pullPolicy`   | Specifies the image pull policy for ADM agent onboarding. | IfNotPresent        |
| `token`     | Authentication and authorization bearer token generated using access ID and access secret.  | nil |
| `apiURL`     | Provide Kubernetes API URL in `https://<host>:port` format  | nil |
| `clusterName`     | Kubernetes cluster name to be registered in ADM Service.  | nil |
|`admAgent.name`| Name for the ADM Agent.| "admagent" |
|`admAgent.imageRegistry`			   | Image registry of the Citrix ADM agent               | `quay.io`               |
|`admAgent.imageRepository`			   | Image repository of the Citrix ADM agent               | `citrix/adm-agent`               |
|`admAgent.imageTag`			   | Image tag  of the Citrix ADM agent               | `latest`               |
|`admAgent.helperImageRegistry`			   | Image registry of Citrix ADM agent helper               | `quay.io`               |
|`admAgent.helperImageRepository`			   | Image repository of Citrix ADM agent helper               | `citrix/adm-agent-helper`               |
|`admAgent.helperImageTag`			   | Image tag of Citrix ADM agent helper               | `1.0.0`               |
|`admAgent.loginSecret`|Specifies the login Secret of Citrix ADM agent.| Nil|
|`adc.IP`| Specifies the Citrix ADC VPX/MPS management IP address.| Nil |
|`adc.mgmtHTTPPort`| Specifies the Citrix ADC VPX/MPX management HTTP port.| 80 |
|`adc.mgmtHTTPSPort`|Specifies the Citrix ADC VPX/MPX management HTTPS port.| 443|
|`adc.loginSecret`| Specifies the the Kubernetes secret containing Citrix ADC VPX/MPX login credentials. | nslogin|

**Note:** You can use the `values.yaml` file packaged in the chart. This file contains the default configuration values for the chart.
