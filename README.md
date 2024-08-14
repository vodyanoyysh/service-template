# TEMPLATE SERVICE

## Usage example
```python
import asyncio

from template_service.main import TemplateService


class Service(TemplateService):
    def __init__(self, config_file_name: str):
        super().__init__(config_file_name)
        asyncio.run(self.start())

    async def run(self, job_name: str):
        if job_name == "job name":
            print(True)
        else:
            print(False)


if __name__ == '__main__':
    service = Service("application.yml")
```


## Configuration file example
```yaml
service:
  env: $ENV
  name: "service-name"
  description: "service-name"
  version: "0.1.0"
  port: 8000
  wait_time: 10
  on_error:
    try_count: 5
    wait_time: 10

schedule:
  every_day:
    start_at:
      - time: "12:04"
        tag: "job tag"
        kwargs:
          job_name: "job name"
  weeks:
    - weekday: "wednesday"
      start_at:
        - time: "12:07"
          tag: "job tag"
          kwargs:
            job_name: "job name"

log:
  name: "service-name"
  level: "INFO"
  format: "%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(funcName)s | %(lineno)s | %(message)s"
  datefmt: "%Y-%m-%d %H:%M:%S"
  other_loggers:
    - name: "other_logger_name"
      level: "WARNING"

metrics:
  port: 8000
  processing:
    documentation: processing docs
    labels:
      service.run:
        type: service
        process: run
        trigger_count: 1
        trigger_time: 24h
        trigger_description_url: ""

  error:
    documentation: processing docs
    labels:
      service.run:
        type: service
        process: run
        trigger_count: 1
        trigger_time: 10m
        trigger_description_url: ""

```