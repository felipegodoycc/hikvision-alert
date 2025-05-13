import requests
from urllib3 import Retry
from requests.adapters import HTTPAdapter
import threading
import os
import logging

from .events import EventStore
from .hikvision_api import HikvisionAPI
from .image_analizer import ImageAnalizer
from .config import config

logger = logging.getLogger(__name__)

class HikvisionEventProcessor:
    def __init__(self):
        self.eventsStore = EventStore()
        self.hikvisionApi = HikvisionAPI(config.HIKVISION_IP, config.HIKVISION_USER, config.HIKVISION_PASSWORD)
        self.imageAnalizer = ImageAnalizer()

    def process_event(self, hikvision_event):
        try:
            if hikvision_event:
                channel = hikvision_event.get('channelID')
                isRecent, alert_event = self.eventsStore.check_if_recent_event(hikvision_event)
                if not isRecent:
                    self.logger.debug(f"Agregando evento del canal {channel} y enviando a analisis interno.", extra=alert_event)
                    snapshot = self.hikvisionApi.save_snapshot(channel, alert_event.get('url_snapshot'))
                    if snapshot:
                        objetos = self.imageAnalizer.detectar_objetos(snapshot)
                        if len(objetos) > 0:
                            self.fire_webhook(channel, snapshot)
                            self.eventsStore.confirm_detection(alert_event['id'], objetos) # Actualizamos el evento como positivo
                        else:
                            self.eventsStore.delete_event(alert_event['id']) # Eliminamos el ultimo evento ya que no tiene importancia
                        os.remove(snapshot)
        except Exception as e:
            self.logger.error(f"[process_event] Error procesando evento: { str(e) }")
            
    def fire_webhook(channel, snapshot):
        def send():
            url = config.WEBHOOK_URL
            
            logger.debug(f"Disparando webhook para canal: {channel}")

            payload = {
                'event': 'motion_detected',
                'channel': channel
            }

            files = {
                'image': open(snapshot, 'rb')
            }

            # Crear sesión aislada con reintentos
            session = requests.Session()
            retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            try:
                res = session.post(url, data=payload, files=files, timeout=10)
                res.raise_for_status()
                logger.debug(f"✅ Webhook enviado con éxito: {res.status_code}")
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Error enviando webhook: {e}")
            finally:
                session.close()
                files["image"].close()

        # Ejecutar el envío en un hilo para no bloquear el stream
        threading.Thread(target=send, daemon=True).start()
        
    def listen(self):
        try:
            self.hikvisionApi.conect_stream_event(self.process_event)
        except Exception as e:
            logger.error(f"Error al conectar al stream de eventos: { str(e) }")