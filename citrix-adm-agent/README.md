# Citrix ADM Agent Helm chart

## Information

This Helm chart deploys Citrix ADM (Application Delivery Management) Agent to connect to Citrix Cloud.

## Prerequisites

### Citrix Cloud

* You need to setup Citrix Cloud with ADM (Application Delivery Management) and add licenses for the Citrix ADC CPXs.
* When you are in ADM, go to Networks > Agents > Set Up Agent and choose "As a Microservice"
* You need to do this once for every environment (example: DEV, QA and PROD) and set the Application ID to something like `kubernetes-<env>` (example: `kubernetes-dev`).
* Download the YAML and follow the steps below (`kubernetes-dev.yaml`)

### Managing the secrets

There are a few ways to use the secrets from the downloaded YAML:

* Upload to Azure KeyVault (or something like that) and leverage them from your automation (Ansible for example)
* Add these secrets manually to the environment
* Use the values in the helm chart

Note: The below commands assume that the secret is the third YAML-document (index 2) and the config map is the fourth (index 3) YAML-document in `kubernetes-dev.yaml`.

#### Uploading to to Azure KeyVault

This should be run once per environment.

```shell
FILENAME="kubernetes-dev"

ADM_AGENT_SECRET_DB_KEY_CONF=$(yq read ${FILENAME}.yaml -d 2 "data[db_key.conf]")
ADM_AGENT_SECRET_PRIVATE_PEM=$(yq read ${FILENAME}.yaml -d 2 "data[private.pem]")
ADM_AGENT_SECRET_PUBLIC_PEM=$(yq read ${FILENAME}.yaml -d 2 "data[public.pem]")
ADM_AGENT_SECRET_PASSWORD=$(yq read ${FILENAME}.yaml -d 2 "data[password]")
ADM_AGENT_CONFIGMAP_AGENT_CONF=$(yq read ${FILENAME}.yaml -d 3 "data[agent.conf]" | base64)
ADM_AGENT_CONFIGMAP_PROXY_CONF=$(yq read ${FILENAME}.yaml -d 3 "data[proxy.conf]" | base64)

cat <<EOF | jq -c > ${FILENAME}.json
{
    "secret": {
        "db_key_conf": "${ADM_AGENT_SECRET_DB_KEY_CONF}",
        "private_pem": "${ADM_AGENT_SECRET_PRIVATE_PEM}",
        "public_pem": "${ADM_AGENT_SECRET_PUBLIC_PEM}",
        "password": "${ADM_AGENT_SECRET_PASSWORD}"
    },
    "configmap": {
        "agent_conf": "${ADM_AGENT_CONFIGMAP_AGENT_CONF}",
        "proxy_conf": "${ADM_AGENT_CONFIGMAP_PROXY_CONF}"
    }
}
EOF

AZURE_KEYVAULT_NAME="keyvaultname"
az keyvault secret set --vault-name ${AZURE_KEYVAULT_NAME} --name citrix-adm-agent --file "${FILENAME}.json"
```

This could be read from Azure KeyVault using the following:

```YAML
- name: Get citrix-adm-agent secret from KeyVault
  shell: "az keyvault secret show --vault keyvaultname --name citrix-adm-agent --output json"
  register: citrixAdmAgentSecret

- name: Set Citrix ADM Agent facts
  set_fact:
    citrixAdmAgentConfig:
      secret:
        db_key_conf: "{{ ((citrixAdmAgentSecret.stdout | from_json).value | from_json).secret.db_key_conf }}"
        private_pem: "{{ ((citrixAdmAgentSecret.stdout | from_json).value | from_json).secret.private_pem }}"
        public_pem: "{{ ((citrixAdmAgentSecret.stdout | from_json).value | from_json).secret.public_pem }}"
        password: "{{ ((citrixAdmAgentSecret.stdout | from_json).value | from_json).secret.password }}"
      configmap:
        agent_conf: "{{ ((citrixAdmAgentSecret.stdout | from_json).value | from_json).configmap.agent_conf | b64decode }}"
        proxy_conf: "{{ ((citrixAdmAgentSecret.stdout | from_json).value | from_json).configmap.proxy_conf | b64decode }}"
```

#### Adding the secrets manually to Kubernetes

```shell
FILENAME="kubernetes-dev"
NAMESPACE="default"

yq read ${FILENAME}.yaml -d 2 | kubectl -n ${NAMESPACE} apply -f -
yq read ${FILENAME}.yaml -d 3 | kubectl -n ${NAMESPACE} apply -f -

helm install citrix-adm-agent --set secret.existingSecretName=${FILENAME} --set configMap.existingConfigMapName=${FILENAME} <repo>/citrix-adm-agent
```

#### Using values of the helm chart

```shell
FILENAME="kubernetes-dev"

ADM_AGENT_SECRET_DB_KEY_CONF=$(yq read ${FILENAME}.yaml -d 2 "data[db_key.conf]")
ADM_AGENT_SECRET_PRIVATE_PEM=$(yq read ${FILENAME}.yaml -d 2 "data[private.pem]")
ADM_AGENT_SECRET_PUBLIC_PEM=$(yq read ${FILENAME}.yaml -d 2 "data[public.pem]")
ADM_AGENT_SECRET_PASSWORD=$(yq read ${FILENAME}.yaml -d 2 "data[password]")
ADM_AGENT_CONFIGMAP_AGENT_CONF=$(yq read ${FILENAME}.yaml -d 3 "data[agent.conf]" | base64)
ADM_AGENT_CONFIGMAP_PROXY_CONF=$(yq read ${FILENAME}.yaml -d 3 "data[proxy.conf]" | base64)

cat <<EOF | yq read - -d '*' > values.yaml
secret:
  useExistingSecret: false
  db_key_conf: ${ADM_AGENT_SECRET_DB_KEY_CONF}
  private_pem: ${ADM_AGENT_SECRET_PRIVATE_PEM}
  public_pem: ${ADM_AGENT_SECRET_PUBLIC_PEM}
  password: ${ADM_AGENT_SECRET_PASSWORD}

configMap:
  useExistingConfigMap: false
  agent_conf: ${ADM_AGENT_CONFIGMAP_AGENT_CONF}
  proxy_conf: ${ADM_AGENT_CONFIGMAP_PROXY_CONF}
EOF

helm install -f values.yaml citrix-adm-agent <repo>/citrix-adm-agent
```