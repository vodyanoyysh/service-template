import asyncio
import traceback

import uvicorn
import schedule
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from template_service.api.router import router
from template_service.core.config import get_config
from template_service.core.metrics import MetricsLoader
from template_service.core.logger import set_logger_config


class TemplateService:
    def __init__(self, config_file_name: str):
        """
        Инициализация сервиса
        :param config_file_name: Имя файла конфига. Конфиг должен находиться в корне проекта
        """
        self.cfg = get_config(config_file_name)
        self.log = set_logger_config(self.cfg.log)
        self.metrics = MetricsLoader(self.cfg.metrics)
        self.app = FastAPI(lifespan=None,
                           title=f"{self.cfg.service.name} {self.cfg.service.env}",
                           description=self.cfg.service.description,
                           version=self.cfg.service.version)
        self.app.include_router(router)
        self.app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
        # asyncio.run(self.start())

    async def start(self):
        """
        Запуск сервиса
        :return:
        """
        self.log.info(f"service {self.cfg.service.name} is starting in {self.cfg.service.env} environment")
        if self.cfg.schedule:
            self._create_schedule(self.run)
            asyncio.create_task(self._scheduler())
        else:
            self.run()
        await self._start_server()
        self.stop()

    def run(self):
        """
        Запуск сервиса
        :return:
        """

    def stop(self):
        """
        Вызывается при остановке сервиса
        :return:
        """
        self.log.info(f"Service {self.cfg.service.name} is stopping")

    def _create_schedule(self, func):
        """
        Создание расписания
        :param func: Функция, которая будет запускаться по расписанию
        :return:
        """
        cfg = self.cfg.schedule
        if cfg:
            if hasattr(self.cfg.schedule, 'every_day'):
                for job in cfg.every_day.start_at:
                    self.log.info(f"create schedule every day run at {job.time} tag: {job.tag} kwargs: {job.kwargs}")
                    schedule.every().day.at(job.time).do(self._wrap_job(func, **job.kwargs)).tag(job.tag)

            if hasattr(cfg, 'weeks'):
                for week in cfg.weeks:
                    for job in week.start_at:
                        self.log.info(f"create schedule week {week.weekday} run at {job.time} tag: {job.tag} kwargs: {job.kwargs}")
                        getattr(schedule.every(), week.weekday).at(job.time).do(self._wrap_job(func, **job.kwargs))

    async def _scheduler(self):
        """
        Запуск расписания
        :return:
        """
        while True:
            schedule.run_pending()
            self.log.info(f"next schedule run at {schedule.next_run().strftime('%H:%M:%S')}")
            await asyncio.sleep(self.cfg.service.wait_time)

    def _wrap_job(self, func, **kwargs):
        """
        Обертка для функции job'a с обработкой ошибок и повторными попытками.
        :param func: Функция
        :return: Обернутая функция
        """

        async def wrapped_func():
            retry_count = 0
            max_retry_count = self.cfg.service.on_error.try_count

            while retry_count < max_retry_count:
                try:
                    await func(**kwargs)
                    return
                except Exception as err:
                    self.log.error(f"Error executing job: {err}")
                    self.log.error(traceback.format_exc())
                    retry_count += 1
                    if retry_count < max_retry_count:
                        self.log.info(f"Retrying job ({retry_count}/{max_retry_count}) after error.")
                        await asyncio.sleep(self.cfg.service.on_error.wait_time)
                    else:
                        self.log.error("Failed after maximum attempts, skipping job.")

        def run_wrapped_func():
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.ensure_future(wrapped_func())
            else:
                loop.run_until_complete(wrapped_func())

        return run_wrapped_func

    async def _start_server(self):
        """
        Запуск FastAPI сервера
        :return:
        """
        uvicorn_config = uvicorn.Config(self.app, host="0.0.0.0", port=self.cfg.service.port)
        server = uvicorn.Server(uvicorn_config)
        await server.serve()
