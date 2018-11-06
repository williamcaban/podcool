[![Docker Repository on Quay](https://quay.io/repository/redhat/podcool/status "Docker Repository on Quay")](https://quay.io/repository/redhat/podcool)
# Demo Application Used to Showcase Multiple OpenShift Concepts

This repository provides a sample Python web application implemented using the ``Flask`` web framework. It is intended to be used to demonstrate a variety of capabilities of OpenShift 3.11 and higher. The base functionality should work in prior versions but this has not been tested.

This app can be used to demonstrate the following OpenShift features or capabilities:
- s2i
    - source strategy
    - Dockerfile/docker strategy
    - Image strategy
- Blue/Green deployments
- Canary deployments
- OpenShift Service Mesh (Maistra: Istio, Envoy, Kiali, Jaeger, Grafana, Prometheus)
- OpenShift Multinetwork (Multus) [dev preview]


## Requirements

To test this apps you will need an OpenShift or OKD environment.

# Using the application

The application understand the following environment variables
- ``APP_VERSION``
- ``APP_MESSAGE``

The values of these variables are displayed as the *application version* and as a *generic message* accordingly.

- ``APP_VERSION`` between v1 to v12 will display a background image
- ``APP_VERSION`` with value of *"Blue"* or *"Green"* will display a solid Blue or Green background
- ``APP_VERSION`` with any other value will display a solid white background.

Using the basic funcitonalities of the demo app:

| APP ROUTES  	|                                     FUNCTIONALITY                                    	|                                USE CASES                                	|
|:----------:	|:------------------------------------------------------------------------------------:	|:-----------------------------------------------------------------------:	|
|   /           | Display a simple web interface with the name of the Pod, ``APP_VERSION`` and ``APP_MESSAGE`` information. | This can be used to demo from a browser |
|   /hello   	| Return a single liner text version of the Pod name and ``APP_VERSION``.                  	| This can be used to demo from a ``curl`` command or similar             	|
| /healthz   	| Return a JSON formatted status of the app, the container name and container version. 	| This can be used for health checks or pod readiness checks              	|
| /net      	| Return a JSON formatted list of the network interfaces seen by the pod.              	| This can be used to demo Multus/OpenShift Multinetwork functionalities.	|
| /net/\<ifname>      	| Return a JSON formatted list of IPv4 addresses of ``ifname`` Pod interface.              	| This can be used to demo Multus/OpenShift Multinetwork functionalities.	|
| /ping/\<dhost>      	| Return a JSON formatted list tcp_ping result to port 80 of ``dhost``.              	| This can be used to demo Istio and Multus/OpenShift Multinetwork functionalities.	|
| /ping/\<dhost>/\<dport>      	| Return a JSON formatted list tcp_ping result to port ``dport`` of ``dhost``.              	| This can be used to demo Istio and Multus/OpenShift Multinetwork functionalities.	|

# DEMOS & LABS

Some demos and labs that use this application are available at [https://github.com/williamcaban/podcool-docs](https://github.com/williamcaban/podcool-docs)

- Deploying an App using the Developer Console
- Deploying an App using the OpenShift Client CLI
- Testing Pod Resiliency
- Deployment Strategies
- Splitting Traffic
- CI/CD Pipelines
- Quay Enterprise Registry
- OpenShift Service Mesh [Tech Prev] -- (Maistra, Isitio, Envoy, Kiali, Prometheus, Grafana, Jaeger)
- OpenShift Multi-network [Dev Prev] -- (Multus)

# Using a Minishift Environment

If using Red Hat CDK you can start OpenShift (Minishift) with the following command:
```
$ minishift start
oc login -u developer
```

Some additional Minishft commands if considering the use of privileged containers.

**NOTE**: THESE ARE NOT REQUIRED FOR THIS DEMO BUT GOOD TO KEEP IN MIND FOR DEMO ENVIRONMENTS
```
oc adm policy add-scc-to-group anyuid system:authenticated
$ minishift addons enable anyuid
$ minishift addons enable admin-user
$ minishift start --ocp-tag v3.11.16
```

To explore additional Minishift addons
```
$ minishift addons list
```

Additional details about Minishift can be found at
- https://docs.okd.io/latest/minishift/using/basic-usage.html


# Implementation Notes

This sample Python application relies on the support provided by the default S2I builder for deploying a WSGI application using the ``gunicorn`` WSGI server. The requirements which need to be satisfied for this to work are:

* The WSGI application code file needs to be named ``wsgi.py``.
* The WSGI application entry point within the code file needs to be named ``application``.
* The ``gunicorn`` package must be listed in the ``requirements.txt`` file for ``pip``.

In addition, the ``.s2i/environment`` file has been created to allow environment variables to be set to override the behaviour of the default S2I builder for Python.

The environment variable ``APP_CONFIG`` has been set to declare the name of the config file for ``gunicorn`` .
