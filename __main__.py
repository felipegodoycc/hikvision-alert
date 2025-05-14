# Importamos las librerias necesarias
from src.config import config
from src.hikvision_event_processor import HikvisionEventProcessor
from src.logger import logger

# Instanciacion de clases necesarias
hikvsionEventProcessor = HikvisionEventProcessor()

# Usamos el logger para registrar mensajes de depuración
try:
    config.print_vars()
    logger.info("Configuración inicializada correctamente.")
except Exception as e:
    logger.error(f"Error al inicializar la configuración: {str(e)}")

if __name__ == "__main__":
    try:
        hikvsionEventProcessor.listen()
    except Exception as e:
        logger.error(f"Error general: { str(e)}")
