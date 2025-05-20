#!/bin/bash


export metric_name="dist.http.endpoint.request"
export DD_API_KEY="d618822854902d8c67fc42ae858f6543"
export DD_APP_KEY="7b859c75b0517e22d80181d24ba21d7f572ae82e"
## Dynamic Points
# Post time-series data that can be graphed on Datadog’s dashboards.

# Template variables
export NOW="$(date +%s)"
# Curl command
curl -X POST "https://api.datadoghq.com/api/v2/series" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-d @- << EOF
{
  "series": [
    {
      "metric": "system.load.1",
      "type": 0,
      "points": [
        {
          "timestamp": 1746565293,
          "value": 0.7
        }
      ],
      "resources": [
        {
          "name": "dummyhost",
          "type": "host"
        }
      ]
    }
  ]
}
EOF
