# sesam-azure-service-bus-sink
Simple sink from Sesam.io to Azure service bus

## System setup
```json
{
  "_id": "azure-sb-sink",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "SERVICE_NAMESPACE": "<namespace>",
      "SERVICE_SAS_TOKEN_NAME": "<sas token name>",
      "SERVICE_SAS_TOKEN_VALUE": "<sas token>"
    },
    "image": "ohuenno/sesam-azure-sb-sink",
    "port": 5000
  },
  "verify_ssl": true
}

```

## Pipe setup

```json
{
  "_id": "<id>",
  "type": "pipe",
  "source": {
    "type": "dataset",
    "dataset": "<source data set>"
  },
  "sink": {
    "type": "json",
    "system": "azure-sb-sink",
    "url": "<queue name>"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        <Transformations you need to apply before send data>
      ]
    }
  },
  "pump": {
    "cron_expression": "0 0 * * ?"
  }
}
```
