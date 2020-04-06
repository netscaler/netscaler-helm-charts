## Introduction
Helm, the package manager for Kubernetes that contains information sufficient for installing, upgrading and managing a set of Kubernetes resources into a Kubernetes cluster. Helm packages are called charts. A Helm chart encapsulates YAML definitions, provides a mechanism for configuration at deploy-time and allows you to define metadata and documentation that might be useful when sharing the package.

## Installation
To install Helm run Helm's installer script in a terminal:

```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

There are several other ways to install Helm as well, you can find it [here](https://helm.sh/docs/intro/install/).

## Verify
You can verify that you have the correct version and that it installed properly by running:

   ```helm version ```

If helm is initialised properly you will get output for helm version something like:

   ```
   version.BuildInfo{Version:"v3.1.2", GitCommit:"d878d4d45863e42fd5cff6743294a11d28a9abce", GitTreeState:"clean", GoVersion:"go1.13.8"}
   ```
