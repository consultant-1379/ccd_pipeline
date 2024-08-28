# Eventrouter Helm Chart

This helm chart deploys Heptio Eventrouter with the Elasticsearch sink included.

## Installation using Helm 3

1. Create values file with required configuration to override defaults

Example values for Elasticsearch sink:

    config:
      sink: elastic
      elasticURL: http://my-elastic.search:9200
      elasticTag: k8s-deployment-id

2. Install to deployment using values file in step 1
```bash
$ helm install my-release ./services/eventrouter -n mynamespace -f myvalues.yaml
```
