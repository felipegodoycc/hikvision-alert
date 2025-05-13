import logging
from .config import config
from logging_loki import LokiHandler

class HikvisionAlertLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_logger()
        
    # Configuracion de logging
    def config_logger(self):
        # Logger sistema
        logging.basicConfig(
            level=config.LOGGER_LEVEL,
            format='%(asctime)s [%(levelname)s] %(message)s'
        )

        # Logger to loki
        if config.LOKI_URL:
            handler = LokiHandler(
                url=f"{config.LOKI_URL}/loki/api/v1/push",
                tags={"job": "hikvision_stream", "source": "python"},
                version="1",
            )

            self.logger.addHandler(handler)
        
    def get_logger(self):
        return self.logger

logger = HikvisionAlertLogger().get_logger()