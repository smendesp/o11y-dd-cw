import boto3

from .logging import Logging


class Config:

    def __init__(self):
        self.cw_client = boto3.client("cloudwatch")
        self.namespace: str = "DataObservability"
        self.metric_data: list = []

    def set_config(self, namespace: str = ""):
        self.namespace = namespace


logging = Logging()
logger = logging.logger

configs: Config = Config()


def _put_metric_data(_metric_data: list = [], _namespace: str = ""):
    client = configs.cw_client

    try:
        response = client.put_metric_data(
            Namespace=configs.namespace if _namespace == "" else _namespace,
            MetricData=configs.metric_data if _metric_data == [] else _metric_data,
        )
    except Exception as e:
        raise e


def _count(_name: str = "", _value=0, _dimensions: list = [], _namespace: str = ""):

    if _name == "":
        raise "Informe um nome para métrica."

    metric: dict = {
        "MetricName": _name,
        "Dimensions": _dimensions,
        "Value": _value,
        "Unit": "Count",
        "StorageResolution": 1,
    }

    metric_data: list = []
    metric_data.append(metric)

    _put_metric_data(_metric_data=metric_data, _namespace=_namespace)


def config(namespace: str = ""):
    configs.set_config(namespace=namespace)


def count(name: str = "", value=1, dimensions: list = [], namespace: str = ""):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                call_func = func(*args, **kwargs)

                _count(
                    _name=name,
                    _value=value,
                    _dimensions=dimensions,
                    _namespace=namespace,
                )

                return call_func

            except Exception as e:
                logger.error(e)

        return wrapper

    return decorator
