# Utils
import requests 
import json
import time

from .logger import logger
from .config import config

def send_event_to_loki(event):
    try:
        stream_labels = {
            "job": "hikvision_stream_events",
            "source": "python",
            'level': 'info'
        }

        # Agrega como etiquetas los campos útiles del evento
        for key in ["channel", "channel_name", "result", "event_description", "event_target_type"]:
            if event.get(key):
                stream_labels[key] = str(event[key])

        payload = {
            "streams": [
                {
                    "stream": stream_labels,
                    "values": [
                        [str(int(time.time() * 1e9)), json.dumps(event, ensure_ascii=False)]
                    ]
                }
            ]
        }

        response = requests.post(f"{config.LOKI_URL}/loki/api/v1/push", json=payload)
        if response.status_code != 204:
            logger.error(f"Error enviando evento a Loki: {response.status_code} - {response.text}")
        else:
            logger.debug(f"Evento enviado a Loki: {json.dumps(event)}")
    except Exception as e:
        logger.error(f"Error enviando evento a Loki: {e}")
        
# Decorador para medir tiempo de ejecucion de funciones
def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.debug(f"Tiempo de ejecucion de {func.__name__}: {elapsed_time:.2f} segundos")
        return result
    return wrapper

