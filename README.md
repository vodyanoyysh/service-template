# service-name

## Usage example
```python

class MyService(Service):
        def __init__(self, config_file_name: str):
        super().__init__(config_file_name)
        self.app.include_router(custom_router)
        asyncio.run(self.start())

    def run(self):
        while True:
            self.log.info("hello world")
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
    start_at: [ "04:19", "04:20" ]
  weeks:
    - weekday: "monday"
      start_at: [ "10:10" ]

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