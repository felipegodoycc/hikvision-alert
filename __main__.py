# Importamos las librerias necesarias
from hikvision_event_processor import HikvisionEventProcessor
from src.utils import config_logger

# Instanciacion de clases necesarias
hikvsionEventProcessor = HikvisionEventProcessor()
logger = config_logger()

if __name__ == "__main__":
    try:
        hikvsionEventProcessor.listen()
    except Exception as e:
        logger.error(f"Error general: { str(e)}")
