import requests
import json
from datetime import datetime

from .logging import Logging

## Dynamic Points
# Post time-series data that can be graphed on Datadog’s dashboards.

# # Template variables
# export NOW="$(date +%s)"
# # Curl command
# curl -X POST "https://api.datadoghq.com/api/v2/series" \
# -H "Accept: application/json" \
# -H "Content-Type: application/json" \
# -H "DD-API-KEY: ${DD_API_KEY}" \
# -d @- << EOF
# {
#   "series": [
#     {
#       "metric": "system.load.1",
#       "type": 0,
#       "points": [
#         {
#           "timestamp": 1636629071,
#           "value": 0.7
#         }
#       ],
#       "resources": [
#         {
#           "name": "dummyhost",
#           "type": "host"
#         }
#       ]
#     }
#   ]
# }
# EOF

logging = Logging()
logger = logging.logger


class Config:

    def __init__(self, job_name: str = "", tags: list = [], preffix: str = ""):
        API_KEY = "d618822854902d8c67fc42ae858f6543"
        APP_KEY = "7b859c75b0517e22d80181d24ba21d7f572ae82e"

        self.retry = 3
        self.time_start = datetime.now()
        self.job_name = job_name
        self.tags = tags
        self.preffix = "glue.job." if preffix == "" else preffix
        self.resources = [{"name": self.job_name, "type": "glue_job"}]

        self.series_buffer: dict = {"series": []}

        self.datadog_api_url_base: str = "https://us5.datadoghq.com/api/v2"
        self.headers: list = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "DD-API-KEY": API_KEY,
            "DD-APPLICATION-KEY": APP_KEY,
        }

    def set_config(
        self, job_name: str = "", tags: list = [], preffix: str = "", retry: int = 0
    ):
        self.job_name = job_name
        self.tags = tags
        self.preffix = "glue.job." if preffix == "" else preffix
        self.resources = [{"name": self.job_name, "type": "glue_job"}]
        self.retry = self.retry if retry == 0 else retry

    def reset_start_time(self):
        self.time_start = datetime.now()



configs: Config = Config()


def _post_series(series_data: dict = {}, _retry: int = 0):
    try:
        retry = configs.retry if _retry == 0 else _retry
        api_url: str = f"{configs.datadog_api_url_base}/series"
        req = requests.post(
            url=api_url, headers=configs.headers, data=json.dumps(series_data)
        )

        log_data: dict = {
            "url": api_url,
            "status_code": req.status_code,
            "headers": configs.headers,
            "series_data": series_data,
            "response": req.text,
            "retry": 0,
        }

        if req.status_code == 202:
            logger.info(log_data)

        if req.status_code != 202:
            log_data["retry"] = retry

            logger.error(log_data)

            while retry > 1:
                retry = retry - 1
                _post_series(series_data=series_data, _retry=retry)

        configs.series_buffer = {"series": []}

        return req

    except Exception as error:
        raise error


def _series(
    metric: str = "",
    points: list = [],
    resources: list = [],
    tags: list = [],
    is_buffer: bool = False,
    type: int = 1,
):

    # Types: 0 (unspecified), 1 (count), 2 (rate), and 3 (gauge)
    tags.extend(configs.tags)
    resources.extend(configs.resources)

    if "value" not in points and type == 1:
        points = [{"value": 1}]

    if "timestamp" not in points:
        now = datetime.now()
        ts = datetime.timestamp(now)
        timestamp: dict = {"timestamp": int(ts)}

        points[0].update(timestamp)

    series_data: list = [
        {
            "metric": configs.preffix + metric,
            "type": type,
            "points": points,
            "resources": resources,
            "tags": tags,
        }
    ]

    if type == 1 or type == 2:
        series_data[0].update({"interval": 1})

    if is_buffer:
        configs.series_buffer["series"].extend(series_data)

    if not is_buffer:
        configs.series_buffer["series"].extend(series_data)
        _post_series(configs.series_buffer)


def reset_start_time():
    configs.reset_start_time()

def config(job_name: str = "", tags: list = [], preffix: str = "", retry: int = 0):
    configs.set_config(job_name=job_name, tags=tags, preffix=preffix, retry=retry)


def _close():
    time_stop = datetime.now()
    time_delta = (time_stop - configs.time_start).microseconds
    now_timestamp: int = int(datetime.timestamp(time_stop))

    metric_name = "execution.time.total"
    points = [{"timestamp": now_timestamp, "value": time_delta}]

    _series(metric=metric_name, points=points, type=1, is_buffer=True)

    metric_name = "execution.count"
    points = [{"timestamp": now_timestamp, "value": 1}]

    _series(metric=metric_name, points=points, type=1)


def series(
    metric: str = "",
    points: list = [],
    resources: list = [],
    tags: list = [],
    is_buffer: bool = False,
    type: int = 1,
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:

                call_func = func(*args, **kwargs)

                tags.extend([f"func_name:{func.__name__}"])

                _series(
                    metric=metric,
                    points=points,
                    resources=resources,
                    tags=tags,
                    is_buffer=is_buffer,
                    type=type,
                )

                _close()

                return call_func

            except Exception as e:
                logger.error(e)

        return wrapper

    return decorator
