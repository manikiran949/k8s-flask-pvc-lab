# Kubernetes Flask Persistence Lab (Helm + CSI)

This project demonstrates how to deploy a stateful Flask application on Kubernetes using **Helm** and the **Container Storage Interface (CSI)**. It ensures application data survives even when pods are deleted or restarted.

---

## Overview
By default, container storage is ephemeral—meaning data is lost when the pod restarts. This lab utilizes a **PersistentVolumeClaim (PVC)** and a **StorageClass** to attach a persistent volume to the Flask container, allowing it to store a permanent log of site visits in the `/data` directory.


---

## Tech Stack
* **Python/Flask**: Web application logic.
* **Docker**: Containerization (Image: `manibatchu/flask-pvc-app:v1`).
* **Helm**: Package management and Infrastructure-as-Code.
* **Kind/WSL2**: Local Kubernetes environment.
* **CSI Hostpath Driver**: The storage provisioner (`csi-hostpath-sc`).

---

## Project Structure
* **/flask-pvc-app**: Python source and Dockerfile.
* **/my-flask-app**: Helm chart containing:
    * `values.yaml`: Image and persistence settings.
    * `templates/storage-class.yaml`: Storage driver configuration.
    * `templates/pvc.yaml`: The storage request logic.
    * `templates/deployment.yaml`: Application deployment.
    * `templates/service.yaml`: NodePort network configuration.

---

## Deployment Steps

### 1. Deploy via Helm
Run the following command from your project root to deploy the entire stack:
```bash
helm install flask-pvc-release ./my-flask-app
```
### 2. Access the Application
Since this is running in a WSL2/Kind environment, use port-forwarding to bridge the cluster network to your local host:

```Bash
kubectl port-forward svc/flask-service 5000:5000
```
Visit http://localhost:5000 in your web browser.

## Persistence Validation (The "Crash Test")
To prove the CSI driver and PVC are working correctly, perform the following verification steps:

**Generate Data:** Open the app in your browser and refresh the page multiple times to generate several visit timestamps.

**Delete the Pod:** Simulate a failure by manually killing the pod:

```Bash
kubectl delete pod -l app=flask-app
```
**Wait for Self-Healing:** Watch Kubernetes automatically spin up a replacement pod:

```Bash
kubectl get pods -w
```
**Verify Persistence:** Once the new pod is Running, refresh the browser. All previous timestamps remain visible, confirming the data is stored on the Persistent Volume and not inside the pod's temporary memory.
