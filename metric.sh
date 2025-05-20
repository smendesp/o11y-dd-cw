#!/bin/bash


export metric_name="dist.http.endpoint.request"
export DD_API_KEY="d618822854902d8c67fc42ae858f6543"
export DD_APP_KEY="7b859c75b0517e22d80181d24ba21d7f572ae82e"

# Curl command
curl -X POST "https://api.datadoghq.com/api/v2/metrics/${metric_name}/tags" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-H "DD-APPLICATION-KEY: ${DD_APP_KEY}" \
-d @- << EOF
{
  "data": {
    "type": "manage_tags",
    "id": "ExampleMetric",
    "attributes": {
      "tags": [
        "app",
        "datacenter"
      ],
      "metric_type": "gauge"
    }
  }
}
EOF