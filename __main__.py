# Importamos las librerias necesarias
from src.config import Config
from src.hikvision_event_processor import HikvisionEventProcessor
from src.utils import config_logger

# Instanciacion de clases necesarias
hikvsionEventProcessor = HikvisionEventProcessor()
logger = config_logger()

# Usamos el logger para registrar mensajes de depuración
try:
    config = Config()
    logger.info("Configuración inicializada correctamente.")
except Exception as e:
    logger.error(f"Error al inicializar la configuración: {str(e)}")

if __name__ == "__main__":
    try:
        hikvsionEventProcessor.listen()
    except Exception as e:
        logger.error(f"Error general: { str(e)}")
