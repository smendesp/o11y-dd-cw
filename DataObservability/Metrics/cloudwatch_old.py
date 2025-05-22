import boto3

from .logging import Logging


class Config:
    
    def __init__(self):
        self.cw_client = boto3.client("cloudwatch")
        self.namespace: str = "DataObservability"
        self.metric_data: list = []

        
        ...
        
    def set_config():


        ...


logging = Logging()
logger = logging.logger

configs: Config = Config()

class CloudWatch:
    cw_client = {}
    namespace: str = "DataObservability"
    metric_data: list = []

    def __init__(self):
        self.cw_client = boto3.client("cloudwatch")

    def get_cw_client(self):
        return self.cw_client

    def set_namespace(self, _namespace: str = ""):
        if _namespace == "":
            raise "Informe o nome para o NameSpace."

        self.namespace = _namespace

    def get_namespace(self):
        return self.namespace

    def get_metric_data(self):
        return self.metric_data

    def dimension_formater(self, name: str = "", value: str = ""):
        return {"Name": name, "Value": value}

    def add_metric(self, metric: dict = {}):
        if metric == {}:
            raise "Informe a métrica."

        self.metric_data.append(metric)

    def put_metricas(self, metric_data: list = [], namespace: str = ""):
        client = self.get_cw_client()

        try:
            response = client.put_metric_data(
                Namespace=self.get_namespace() if namespace == "" else namespace,
                MetricData=self.get_metric_data() if metric_data == [] else metric_data,
            )
        except Exception as e:
            raise e

    def count(
        self, _name: str = "", _value=0, _dimensions: list = [], _namespace: str = ""
    ):
        if _name == "":
            raise "Informe um nome para métrica."

        metric: dict = {
            "MetricName": _name,
            "Dimensions": _dimensions,
            "Value": _value,
            "Unit": "Count",
            "StorageResolution": 60,
        }

        metric_data: list = []
        metric_data.append(metric)

        self.put_metricas(metric_data, namespace=_namespace)
