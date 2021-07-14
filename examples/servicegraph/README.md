
# Observability using Citrix ADM for Citrix ADC deployed in dual tier topology

The aim of this example is to help visualising the request flow between different microservices using Citrix ADM.

# Table of Contents

   [Prerequisites](#prerequisite)

  A. [Topology](#topology)

  B. [Deploying Citrix ADM Agent](#onboarding)

  C. [Deploy Netflix application on Kubernetes Cluster ](#deploy-application)

  D. [Citrix Cloud Native Dual Tier Topology ](#deploy-citrix-cloud-native-stack)

  E. [Send Traffic](#send-traffic)

  F. [Visualize Servicegraph in Citrix ADM](#servicegraph)

  G. [Tracing](#trace)

  H. [Clean Up the deployment](#clean-up)

  I. [Debugging](#debugging)

# <a name="prerequisite">Prerequisites</a>
 - Ensure that you have a Citrix ADM account. To use Citrix ADM, you must create a [Citrix Cloud account](https://docs.citrix.com/en-us/citrix-cloud/overview/signing-up-for-citrix-cloud/signing-up-for-citrix-cloud).

    To manage Citrix ADM with an Express account, see [Getting Started](https://docs.citrix.com/en-us/citrix-application-delivery-management-service/getting-started.html#install-an-agent-as-a-microservice).

 - Ensure that you have installed Kubernetes version 1.19 or later. For information about Kubernetes, see  [Kubernetes](https://kubernetes.io/).
 - Ensure that you have Citrix ADC VPX version 13.0-76.31 or later.
 - For deploying Citrix ADC VPX or MPX as an Tier-1 ingress, you should establish the connectivity between Citrix ADC VPX or MPX and cluster nodes. This connectivity can be established by configuring routes on Citrix ADC as described in the [Static routing](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network/staticrouting.md) document or by deploying [Citrix Node Controller](https://github.com/citrix/citrix-k8s-node-controller).
 - Ensure that hhe Helm with version 3.x is installed. For information, see [Helm installation](https://github.com/citrix/citrix-helm-charts/blob/master/Helm_Installation_version_3.md).
 - Ensure that the ports that described in the [Ports](https://docs.citrix.com/en-us/citrix-application-delivery-management-service/system-requirements.html#ports) document are open.


# <a name="topology">A) Topology</a>

Consider the Netflix application topology having Citrix ADC to deliver best user experience in North-South and East-West load balancing.

   ![](images/topology.png)

In this topology, two types of Citrix ADCs have been deployed. One is VPX (non-container proxy) for routing the North-South traffic for microservices. In this topology, VPX is deployed as Tier 1 ADC. Second is Citrix ADC CPX (container proxy) for routing North-South Tier 1 traffic and East-West microservice traffic.

This deployment has its own advantages over service mesh deployment. The advantages include:

 - Citrix ADC Service Mesh lite topology eliminates the need of Citrix ADC CPX as sidecar proxy for each microservices.

 - One Citrix ADC CPX proxy can frontend more than one microservice application as shown in the preceding topology diagram.

Let us deploy the Netflix application in Service mesh lite deployment where:

 - Tier 1 ADC - VPX to ingress secure North-South traffic. You can have MPX/BLX as Tier 1 ADC also.

 - Tier 2 ADC - CPX to route North-South traffic from Tier 1 ADC to frontend Netflix microservice application

 - Tier 2 ADC - CPX to route East-West traffic from Netflix application.

# <a name="onboarding"> B) Onboarding of ADM agent</a>
You can deploy a Citrix ADM agent as a microservice in the Kubernetes cluster to view service graph in Citrix ADM. [ADM agent onboarding](../../adm-agent-onboarding) as a Kubernetes Job helps you to deploy container-based Citrix ADM agent and also performs all the necessary settings in Citrix ADM for generating service graph. This Job also registers the Tier-1 ADC in the Citrix ADM.
To deploy ADM agent onboarding, you need to Kubernetes Secret with Access ID and Secret for accssing Citrix ADM.

## **Get Access ID and Secret to access Citrix ADM**</a> 

Perform the following steps to get access ID and secret for accessing Citrix ADM:

1. Log in to Citrix Cloud account. 

2. On the left Menu panel, select **Identity and Access Management**.

   ![](../../adm-agent-onboarding/images/menu.png)

3. Go to **API Access**.

    ![](../../adm-agent-onboarding/images/apiaccess.png)

4. Specify the client name and click **Create Client**.

    ![](../../adm-agent-onboarding/images/client-detail.png)

5. Download and save the `access-id` and `access-secret` generated.

    ![](../../adm-agent-onboarding/images/downloads-secret.png)

 Now, you can generate `authorization bearer token` using access ID and access secret using below script: 

	python https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/generate_token.py --accessID=<accessID> --accessSecret=<accessSecret>

**NOTE**: The bearer token expires in an hour (3600 seconds).
	  
## Deploy ADM agent onboarding as Kubernetes Job
**NOTE** For deploying Citrix ADC VPX or MPX as an Tier-1 ingress, you should establish the connectivity between Citrix ADC VPX or MPX and cluster nodes. This connectivity can be established by configuring routes on Citrix ADC as described in the [Static routing](https://github.com/citrix/citrix-k8s-ingress-controller/blob/master/docs/network/staticrouting.md) document or by deploying [Citrix Node Controller](https://github.com/citrix/citrix-k8s-node-controller).

To register Tier-1 ADC in Citrix ADM with the agent getting deployed, you need to create Kubernetes Secret containing credentials of Tier-1 ADC VPX/MPX using the following command:

    kubectl create secret generic nslogin --from-literal=username=<username> --from-literal=password=<adc-password>

### To create ADM Agent login Secret automatically and register Tier-1 ADC , use the following command:

    helm repo add citrix https://citrix.github.io/citrix-helm-charts

	helm install citrix-adm citrix/adm-agent-onboarding --set token=<Token> --set adc.IP=<ADC ManagementIP>,adc.loginSecret=nslogin

**Note:** You can label the namespace with `citrix-cpx=enabled` in which Citrix ADC CPX is deployed.

You can check the logs of pod deployed as part of Kubernetes Job adm-agent-onboarding.

![](images/log-adm-agent-onboarding-job.png)

# <a name="deploy-application"> C) Deploy Netflix application on Kubernetes cluster </a>

Use the following command to deploy Netflix application on your Kubernetes cluster:

    kubectl create -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/servicegraph/manifest/netflix.yaml

# <a name="deploy-citrix-cloud-native-stack"> D) Citrix Cloud Native Dual Tier Topology </a>

## To configure the Tier 1 ADC VPX using Citrix Ingress Controller (CIC):

The Citrix ADC appliance needs to have system user account (non-default) with certain privileges so that Citrix ingress controller (CIC) can configure the Citrix ADC VPX. For instructions to create the system user account on Citrix ADC, see [Create System User Account for CIC in Citrix ADC](#create-system-user-account-for-cic-in-citrix-adc).

Create a Kubernetes secret for the user name and password using the following command:

    kubectl create secret generic nscred --from-literal=username=`cic` --from-literal=password='<password>'

Download the consolidated YAML file which can deploy Citrix ingress controller to configure Tier-1 ADC and Tier 2 CPX.

    wget https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/servicegraph/manifest/values.yaml

Update `cic.nsIP` with the Citrix ADC device/management IP address in `values.yaml`.

**Update**  `cic.coeConfig.endpoint.server` with the `Citrix ADM agent POD IP` in `values.yaml`.

To get the Citrix ADM Agent pod IP address, use the following command:

    kubectl get endpoints admagent

## To configure the Tier-2 ADC CPX using CIC:

Citrix ADC CPX is used to route North-South traffic from Tier 1 ADC to frontend Netflix microservice application and route East-West traffic from Netflix microservices. 

Use the following command to list the service IP address for Citrix ADM Agent.

    kubectl get svc admagent -o wide 

Update the `cpx.coeConfig.endpoint.server`  and `ADMIP` with the `Cluster IP` of Citrix ADM agent in `values.yaml`.

After updating the `values.yaml`, deploy Citrix dual Tier deployment using the following commands:
  
    helm repo add citrix https://citrix.github.io/citrix-helm-charts/
    helm install adc-netflix citrix/citrix-cloud-native -f values.yaml 

## Create Ingress and Services for Netflix application

    wget https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/servicegraph/manifest/vpx_ingress.yaml

  **Update**  `ingress.citrix.com/frontend-ip` in `vpx_ingress.yaml` with the virtual IP address with which you want to expose Netflix application.

    kubectl apply -f vpx_ingress.yaml
    kubectl create -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/servicegraph/manifest/cpx_ingress.yaml
    kubectl create -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/servicegraph/manifest/smlite_services.yaml

# <a name="send-traffic"> E) Send Traffic </a>

Send traffic using helper script:

    wget https://raw.githubusercontent.com/citrix/cloud-native-getting-started/master/servicegraph/manifest/traffic.sh

Provide VIP which has been used to expose the Netflix application in `traffic.sh` and start traffic.

    nohup sh traffic.sh <VIP> > log &

# <a name="servicegraph"> F) Visualize Service Graph in Citrix ADM</a>

Before visualizing the Service Graph, you can check if the vservers configured in ADC are properly discovered and licensed. For this, check the section [debugging](#debugging).

In ADM, navigate  `Application > Service Graph > MicroServices` .

  ![](images/servicegraph.png)


  ![](images/servicegraph-detail.png)

You can view **transation logs** as well in the servicegraph.

  ![](images/transactionlog.png)

# <a name="trace">G) Tracing </a>

A user can select **See Trace Details** to visualize the entire trace in the form of a chart of all transactions which are part of the trace.

  ![](images/tracing.png)

# <a name="clean-up">H) Clean up the deployment </a>

    kubectl delete -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/servicegraph/manifest/cpx_ingress.yaml
    kubectl delete -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/servicegraph/manifest/smlite_services.yaml
    kubectl delete -f https://raw.githubusercontent.com/citrix/citrix-helm-charts/master/examples/servicegraph/manifest/netflix.yaml
    kubectl delete -f vpx_ingress.yaml
    helm uninstall adc-netflix
    helm uninstall citrix-adm
    kubectl delete deployment admagent
	kubectl delete secret admagent
	kubectl delete configmaps admagent
	kubectl delete svc admagent
	kubectl delete secret admlogin
    kubectl delete secret nslogin
    kubectl delete sa admagent
    kubectl delete clusterroles admagent
    kubectl delete clusterrolebindings admagent

**Note:** You need to remove the Cluster and Agent from Citrix ADM UI manually.

# <a name="debugging">I) Debugging </a>

Service Graph will not be populated if vserver configuration of Tier 2 ADC are not populated in ADM. Also, the vserver in Tier-1 ADC need to be licensed. Following sections guide on licensing vserver in Tier-1 Citrix ADC VPX and discovering the vserver configuration on Tier 2 Citrix ADC CPX.

## Licensing vserver of Tier-1 Citrix ADC VPX

1. Navigate to `Networks > Instances > Citrix ADC` and choose `VPX` in Citrix ADM.

2. Select the `VPX IP` of your Tier-1 ADC and choose `Configure Analytics` under `Select Action`.

   ![](images/vpx-analytics.png)

3. Vserver configured on the VPX is displayed.

4. License the vserver with name `netflix-<VIP IP>_80_http`, if it is not licensed. To license, select the `vserver` and click `License`.

   ![](images/vserver-list.png)

   ![](images/licensed-vserver.png)


## Disovering Vserver Configuration of Tier-2 Citrix ADC CPX

1. Navigate to `Networks > Instances > Citrix ADC` and choose `CPX` instance with the name prefix with `adc-netflix-cpx` in Citrix ADM.

2. Select the `CPX` from the list and choose `Configure Analytics` under `Select Action`.

   ![](images/cpx-analytics.png)

3. Citrix ADM polls the CPX in the interval of 10 mins. If the page does not list vserver, then you can manually poll the CPX.

   ![](images/cpx-analytics-blank.png)

4. For manual polling CPX:

    a. Navigate to `Networks > Networking Functions` and click `Poll Now`.
   
    ![](images/poll-page.png)

    b. Click `Select Instances`. You will get list of instances. 
   
    ![](images/poll-now.png)

    c. Choose the `CPX` instance from the list.

    ![](images/poll-cpx.png)

    d. Click `Start Polling`.
    
    ![](images/polling.png)

    e. Polling takes a couple of minutes to complete.

    ![](images/poll-successful.png)

     Once polling is completed, navigate to `Networks > Instances > Citrix ADC` and choose `CPX` instance with the name prefix with `adc-netflix-cpx` in Citrix ADM. 
     
     Select the `CPX` from the list and choose `Configure Analytics` under `Select Action`. 
     
     Now you will get the list of Vservers configured on CPX.

    ![](images/cpx-vservers.png)

    You can now view the servicegraph by navigating to `Applications > Service Graph > Microservices ` in Citrix ADM.

# <a name="create-system-user-account-for-cic-in-citrix-adc"> Create system user account for Citrix ingress controller in Citrix ADC</a>

Citrix ingress controller configures the Citrix ADC using a system user account of the Citrix ADC. The system user account should have certain privileges so that the CIC has permission to configure the following on the Citrix ADC:

 - Add, Delete, or View Content Switching (CS) virtual server
 - Configure CS policies and actions
 - Configure Load Balancing (LB) virtual server
 - Configure Service groups
 - Cofigure SSL certkeys
 - Configure routes
 - Configure user monitors
 - Add system file (for uploading SSL certkeys from Kubernetes)
 - Configure Virtual IP address (VIP)
 - Check the status of the Citrix ADC appliance

**Note:**
> The system user account would have privileges based on the command policy that you define.

To create the system user account, perform the following:

 1. Log on to the Citrix ADC appliance.
 2. Use an SSH client, such as PuTTy, to open an SSH connection to the Citrix ADC appliance.
 3. Log on to the appliance by using the administrator credentials.
 4. Create the system user account using the following command:

        add system user <username> <password>

 For example:

    add system user cic mypassword

 5. Create a policy to provide required permissions to the system user account. Use the following command:

        add cmdpolicy cic-policy ALLOW "(^\S+\s+cs\s+\S+)|(^\S+\s+lb\s+\S+)|(^\S+\s+service\s+\S+)|(^\S+\s+servicegroup\s+\S+)|(^stat\s+system)|(^show\s+ha)|(^\S+\s+ssl\s+certKey)|(^\S+\s+ssl)|(^\S+\s+route)|(^\S+\s+monitor)|(^show\s+ns\s+ip)|(^\S+\s+system\s+file)"

 6. Bind the policy to the system user account using the following command:

        bind system user cic cic-policy 0
