# Lab 2: Simulating webhooks rebuild events

Display the BuildConfig to identify the "Webhook Generic" URL
```
oc describe bc/myapp1
```

The <secret> in the URL will be the output of this command
```
oc get bc -o json | jq '.items[0] .spec.triggers[].generic.secret' | grep -v null
```

You can also find the correct URL over the console at the configuration tab of the build config:

https://<your-okd-path>/console/project/demo-app/browse/builds/myapp1?tab=configuration

Simulating a generic Webhook event:
```
curl -X POST -k https://<your-okd-path>/apis/build.openshift.io/v1/namespaces/demo-app/buildconfigs/myapp1/webhooks/<secret>/generic
```