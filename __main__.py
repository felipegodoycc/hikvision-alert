# Importamos las librerias necesarias
from src.config import Config
from src.hikvision_event_processor import HikvisionEventProcessor
from src.utils import config_logger

# Agregamos mensajes de depuración para verificar la inicialización de Config
try:
    config = Config()
    print("Configuración inicializada correctamente.")
except Exception as e:
    print(f"Error al inicializar la configuración: {str(e)}")

# Instanciacion de clases necesarias
hikvsionEventProcessor = HikvisionEventProcessor()
logger = config_logger()

if __name__ == "__main__":
    try:
        hikvsionEventProcessor.listen()
    except Exception as e:
        logger.error(f"Error general: { str(e)}")
