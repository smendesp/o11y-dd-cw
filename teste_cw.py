from DataObservability.Metrics.cloudwatch import config, put_metric, close as cw_close
import random


success = random.randint(0, 1)

config(namespace="DataObservability")


@put_metric(name="execution.success.count")
def f1(nome, sobrenome):
    print(f"success -> {nome} - {sobrenome}")


@put_metric(name="execution.fail.count")
def f2(nome):
    print(f"fail -> {nome}")


if success == 1:
    f1(nome="silvio", sobrenome="mendes")

if success == 0:
    f2("silvio")


cw_close()