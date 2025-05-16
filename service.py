# Importamos las librerias necesarias
from hikvision_alert import HikvisionEventProcessor
from hikvision_alert import logger

# Instanciacion de clases necesarias
hikvsionEventProcessor = HikvisionEventProcessor()

if __name__ == "__main__":
    try:
        hikvsionEventProcessor.listen()
    except Exception as e:
        logger.error(f"Error general: { str(e)}")
