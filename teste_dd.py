from DataObservability.Metrics.datadog import config, series, reset_start_time
import random


success = random.randint(0, 1)

config(job_name="entregas_full", tags=["env:local"], retry=2)

resources = [{"name": "glue_job_teste", "type": "glue_job_teste"}]
tags = ["lab:true"]


@series(metric="execution.success.count", resources=resources, tags=tags)
def f1(nome, sobrenome):
    #time.sleep(5)
    print(f"success -> {nome} - {sobrenome}")


@series(metric="execution.fail.count", resources=resources, tags=tags)
def f2(nome):
    print(f"fail -> {nome}")


if success == 1:
    f1(nome="silvio", sobrenome="mendes")

if success == 0:
    reset_start_time()
    f2("silvio")

