from DataObservability.Metrics.cloudwatch import config, count
import random


success = random.randint(0, 1)

config(namespace="DataObservability")

@count(name="execution.success.count")
def f1(nome, sobrenome):
    print(f"success -> {nome} - {sobrenome}")


@count(name="execution.fail.count")
def f2(nome):
    print(f"fail -> {nome}")


if success == 1:
    f1(nome="silvio", sobrenome="mendes")

if success == 0:
    f2("silvio")

