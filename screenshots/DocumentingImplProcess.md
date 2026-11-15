
### Deployment of the app
As a first step, i created a deployment and a service.
I use minikube service orders-app-service --url to access my project from outside.
![Deployment](image.png)

Accesing from outside:
![Localhost minikube service url](image-1.png)

### Added new code (instrumentation) and created a new image with that
![New images](image-2.png)

### Testing the new image
![New image running in a container](image-3.png)

### Deployment + service created: app deployed and accesible from outside the cluster
![App deployed and accesible](image-4.png)


### Prometheus showing some metrics
![Prometheus showing metrics](image-5.png)


### Got Grafana working, still not connected to prometheus
![Grafana UI](image-6.png)


### Successfully queried the Prometheus API
![Prometheus was queried](image-7.png)

### Testing http_request_total
![http_request_total](image-8.png)


### Golden signals dashboard
Sent traffic with the script
![Traffic in grafana](image-9.png)

### Monitoring stack so far
The requirement number 5 says "Alertmanager DEPLOYMENT", so i investigated and found there is a sofware developed by the same people who developed prometheus that allows me to deploy an alertmanager software.
![Monitorin stack](image-10.png)


### High error rate fired
![Pending](image-11.png)

![Fired](image-12.png)

![From alertmanager](image-13.png)

![From Alertmnger](image-14.png)


### Orders-app down fired
Command to trigger: kubectl scale deployment/orders-app-deployment --replicas=0

To go back healthy: 
kubectl scale deployment/orders-app-deployment --replicas=2                                                                                       

kubectl rollout status deployment/orders-app-deployment 
From prometheus:
![app down](image-15.png)

From Alertmanager: 
Tested it with the latency mode of the script
![Alert manager](image-16.png)

### High latency fired
![High latency fired](image-17.png)

![Alert manager](image-18.png)