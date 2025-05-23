import boto3
from datetime import datetime

from .logging import Logging


class Config:

    def __init__(self):
        self.cw_client = boto3.client("cloudwatch")
        self.namespace: str = "DataObservability"
        self.metric_data: list = []
        self.time_start = datetime.now()
        self.count = 0
        
    def set_config(self, namespace: str = ""):
        self.namespace = namespace

    def reset_start_time(self):
        self.time_start = datetime.now()

    def count_add(self):
        self.count = self.count + 1

logging = Logging()
logger = logging.logger

configs: Config = Config()


def _put_metric(_metric_data: list = [], _namespace: str = ""):
    client = configs.cw_client

    try:
        response = client.put_metric_data(
            Namespace=configs.namespace if _namespace == "" else _namespace,
            MetricData=configs.metric_data if _metric_data == [] else _metric_data,
        )
        
        configs.count_add()
        
    except Exception as e:
        raise e


def close():
    time_stop = datetime.now()
    time_delta = (time_stop - configs.time_start).microseconds

    _put_metric_data(
        _name="execution.time.total", _value=time_delta, _unit="Milliseconds"
    )
    _put_metric_data(_name="execution.count", _value=configs.count, _unit="Count")


def _put_metric_data(
    _name: str = "",
    _value: int = 0,
    _unit: str = "Count",
    _timestamp: int = 0,
    _dimensions: list = [],
    _namespace: str = "",
):
    # 'Unit': 'Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None',

    now = datetime.now()
    now_timestamp: int = _timestamp if _timestamp != 0 else int(datetime.timestamp(now))

    metric: dict = {
        "MetricName": _name,
        "Dimensions": _dimensions,
        "Timestamp": now_timestamp,
        "Value": _value,
        "Unit": _unit,
        "StorageResolution": 1,
    }

    metric_data: list = []
    metric_data.append(metric)

    _put_metric(_metric_data=metric_data, _namespace=_namespace)


def reset_start_time():
    configs.reset_start_time()


def config(namespace: str = ""):
    configs.set_config(namespace=namespace)


def put_metric(
    name: str = "",
    value: int = 1,
    unit: str = "Count",
    dimensions: list = [],
    namespace: str = "",
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                call_func = func(*args, **kwargs)

                _put_metric_data(
                    _name=name,
                    _value=value,
                    _unit=unit,
                    _dimensions=dimensions,
                    _namespace=namespace,
                )

                return call_func

            except Exception as e:
                logger.error(e)

        return wrapper

    return decorator
