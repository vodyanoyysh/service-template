import easydict
from s7metrics import Metrics


class MetricsLoader(Metrics):
    def __init__(self, config: easydict):
        """
        Инициализация класса метрик
        :param config: config.metrics
        """
        super().__init__(config)
        self.init_setup()
