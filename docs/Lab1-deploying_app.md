# Lab 1: Deploying an App

To deploy this sample Python web application from the OpenShift developer console and using the _Add to project_ button, you should select ``python:2.7``, ``python:3.3``, ``python:3.4`` or ``python:latest``. Use of ``python:latest`` is the same as having selected the most up to date Python version available, which at this time is ``python:3.4``.

The HTTPS URL of this code repository which should be supplied to the _Git Repository URL_ field when using _Add to project_ is:

* https://github.com/williamcaban/podcool.git

If using the ``oc`` command line tool instead of the OpenShift web console, to deploy this sample Python web application, you can run:

```
oc new-project demo-app --display-name='My Demo App'
```

To deploy it from git run the following command

* NOTE: Since this demo repo contains a ``Dockerfile``, by default, OpenShift will try to use the ``docker build strategy``. By specifying the *strategy* flag we force OpenShift to use ``s2i build strategy``.

```
oc new-app https://github.com/williamcaban/podcool.git --name=myapp1 --strategy=source
```


To create a URL route
```
oc expose svc/myapp1 --name=myroute

oc get route
```

To get the text output displaying the name use the /hello path. Run the following command in another terminal:
```
$ while sleep 1; do curl http://$(oc get route myroute --template='{{ .spec.host }}'/hello); echo; done
```

Scale to 3 replicas and validate pods have been created
```
oc get pods -l app=myapp1

oc scale --replicas=3 dc/myapp1

oc get pods -l app=myapp1
```

Destroy one of the Pods and watch the system remediate.
```
oc get pods -l app=myapp1

oc delete po/<name-of-pod>

oc get pods -l app=myapp1
```

Deploy another version of the app using ``Docker`` strategy.
- ***NOTE:*** Any key/value pair appended at the end of the CLI deployment command will be interpreted as environment variables to pass to the resulting container. In this case we force the application to run in a different version.
```
oc new-app https://github.com/williamcaban/podcool.git --name=myapp2 --strategy=docker APP_VERSION=v2
```

To deploy from local source code using ``Docker`` strategy
```
oc new-app </path/to/code> --name=<app-name> --strategy=docker APP_VERSION=v3

oc new-app ./ --name=myapp3 --strategy=docker APP_VERSION=v3
```

## About Build Strategies

In the previous example, when using the *``--strategy=source``* since no language type was specified, OpenShift will determine the language by inspecting the code repository. Because the code repository contains a ``requirements.txt``, it will subsequently be interpreted as including a Python application. When such automatic detection happens, ``python:latest`` will be used as the default image.

If needing to select a specific Python version, lets say python 2.7, when using ``oc new-app``, you should instead use the syntax:

```
oc new-app python:2.7~https://github.com/williamcaban/openshift-container-name-demo.git --name=myapp1
```

## Modifying Routes & Splitting Traffic Among Different Versions

Split traffic among the different versions and monitor the load balancing displayed in the terminal running the ``curl`` command
```
oc get route myroute

# Update for 50-25-25 distribution

oc set route-backends myroute myapp1=50% myapp2=25% myapp3=25%

oc get route

# Update for equal traffic distribution

oc set route-backends myroute --equal

oc get route

# Remove ~10% of the traffic from version 3 and watch
# the resulting balancing distribution. The difference
# between requested vs actual is due to weight distribution.

oc set route-backends myroute --adjust myapp3=-10%

oc get route

```

## Additional References

More information about advanced deployment strategies visit: https://docs.openshift.com/container-platform/3.11/dev_guide/deployments/advanced_deployment_strategies.html

