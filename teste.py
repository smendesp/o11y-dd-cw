# from DataObservability.Metrics.cloudwatch import CloudWatch
from DataObservability.Metrics.datadog_class import DataDog

# from DataObservability.DataQuality.glue import Glue

from datetime import datetime
import random
import time

# cw = CloudWatch()
# glue = Glue()


datadog = DataDog(job_name="entregas_full", tags=["env:local"])

# datadog.gauge('teste_gauge')
#

now = datetime.now()
ts = datetime.timestamp(now)

print(int(ts))
print(datetime.fromtimestamp(int(ts)))

success = random.randint(0, 1)

points = [{"timestamp": int(ts), "value": 1}]
resources = [{"name": "glue_job_teste", "type": "glue_job_teste"}]
tags = ["lab:true"]

if success == 1:
    metric_name = "execution.success.count"
    datadog.series(metric=metric_name, points=points, resources=resources, tags=tags)

if success == 0:
    metric_name = "execution.fail.count"
    datadog.series(metric=metric_name, points=points, resources=resources, tags=tags)

time.sleep(2)

