import datetime
import os
import json
import time
import requests
from requests.auth import HTTPDigestAuth
import xmltodict

from .utils import config_logger
from .config import config

logger = config_logger()

class HikvisionAPI:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password
        self.auth = HTTPDigestAuth(user, password)
        self.url_event = f"http://{ip}/{config.HIKVISION_URL_EVENT}"
        
    def take_snapshot(self, channel, url):
        if not url:
            # Si no se pasa la url, se usa la configuracion por defecto
            url = f"http://{self.ip}/{config.HIKVISION_SNAPSHOT}/{channel}01/picture"

        try:
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                logger.debug(f"Snapshot tomado del canal {channel}")
                return response.content
            else:
                logger.error(f"Error tomando snapshot: {response.status_code}")
        except Exception as e:
            logger.error(f"Error tomando snapshot: { json.dumps(e) }")
        return None
    
    def save_snapshot(self, channel, url = None):
        snapshot = self.take_snapshot(channel, url)
            
        if snapshot:
            filename = f"snapshot_{config.CAMERAS_NAME.get(channel, 'Desconocido').lower()}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            fullpath = os.path.join(config.BASE_DIR, config.IMAGE_STORAGE, filename)
            with open(fullpath, 'wb') as f:
                f.write(snapshot)
                return fullpath
        logger.error("Error guardando snapshot.")
        return None
           
    def listen_hikvision_events(self, callback):
        url = self.url_event
        
        logger.info("Iniciando conexión al stream de eventos Hikvision...")

        while True:
            try:
                with requests.get(url, auth=self.auth, stream=True, timeout=(3, 10)) as r:
                    logger.info("✅ Conectado al stream de eventos.")
                    buffer = b""

                    for line in r.iter_lines(chunk_size=512):
                        if line.startswith(b'<EventNotificationAlert'):
                            buffer = line + b"\n"
                        elif b'</EventNotificationAlert>' in line:
                            buffer += line
                            try:
                                hik_event = xmltodict.parse(buffer)
                                hikvision_event = hik_event.get('EventNotificationAlert') or hik_event.get('ns0:EventNotificationAlert')
                                if hikvision_event:
                                    if hikvision_event.get('eventType', 'Desconocido') == 'VMD':
                                        callback(hikvision_event)
                            except Exception as e:
                                logger.error(f"Error parseando evento: {str(e)}")
                            buffer = b""
                        elif buffer:
                            buffer += line + b"\n"
            except requests.exceptions.RequestException as e:
                logger.warning(f"🔌 Stream desconectado, reintentando en 5s... ({e})")
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error inesperado: {e}")
                time.sleep(5)
            
    def conect_stream_event(self, callback):
        try:
            logger.info("Conectando al stream de ISAPI...")
            self.listen_hikvision_events(callback)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexion: {e}")
            logger.error(f"Reintentando en { config.TIME_TO_RECONNECT } segundos...")
            time.sleep(config.TIME_TO_RECONNECT)
        except Exception as e:
            raise e
