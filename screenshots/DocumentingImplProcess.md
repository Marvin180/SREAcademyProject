
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





