import datetime
import uuid
import logging

from .config import config
from .utils import send_event_to_loki

logger = logging.getLogger(__name__)

class EventStore():
    def __init__(self):
        self.self = []
        self.idx = {}
        self.idx_by_channel = {}
        
    def add_event(self, hik_event):
        channel = hik_event.get('channelID')
        logger.debug(f"Evento hik: {str(hik_event)}")
        camera_name = config.CAMERAS_NAME.get(channel, hik_event.get('channelName', 'Desconocido'))
        alert_event = {
            'id': str(uuid.uuid4()),
            'channel': channel,
            'channel_name': camera_name,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'result': False,
            'event_description': hik_event.get('eventDescription', 'Desconocido'),
            'event_target_type': hik_event.get('targetType', 'Desconocido'),
            'selftate': hik_event.get('selftate', 'Desconocido'),
            'url_snapshot': hik_event.get('bkgUrl', None),
            'number_of_objects': hik_event.get('detectionPicturesNumber', 0),
            'active_post_count': hik_event.get('activePostCount', 0)
        }
        
        self.self.append(alert_event)
        self.idx[alert_event['id']] = len(self.self) - 1
        
        if channel not in self.idx_by_channel:
            self.idx_by_channel[channel] = [alert_event['id']]
        else:
            self.idx_by_channel[channel].append(alert_event['id'])
        
        if len(self.self) > config.MAX_EVENTS:
            del self.self[0]
            self.idx.pop(self.self[0]['id'], None)
            if channel in self.idx_by_channel:
                self.idx_by_channel[channel].pop(0)
                if not self.idx_by_channel[channel]:
                    del self.idx_by_channel[channel]
        
        return alert_event
    
    def get_event(self, event_id):
        if event_id in self.idx:
            return self.self[self.idx[event_id]]
        return None
    
    def delete_event(self, event_id):
        if event_id in self.idx:
            index = self.idx[event_id]
            del self.self[index]
            del self.idx[event_id]
            return True
        return False 
    
    def confirm_detection(self, event_id: str, detected_objects: list):
        if event_id in self.idx:
            index = self.idx[event_id]
            self.self[index]['result'] = True
            self.self[index]['detected_objects'] = detected_objects
            if config.LOKI_URL:
                send_event_to_loki(self.self[index])
            return True
        return False
    
    def get_last_event(self, channel):
        if channel in self.idx_by_channel:
            event_ids = self.idx_by_channel[channel]
            if event_ids:
                last_event_id = event_ids[-1]
                return self.get_event(last_event_id)
        return None
    
    def check_if_scheduled(self, channel):
        if config.CAMERA_SCHEDULES is {}:
            logger.info("No hay horarios programados para las cámaras.")
            return True
        
        if channel in config.CAMERA_SCHEDULES:
            schedule = config.CAMERA_SCHEDULES[channel]
            start_time = datetime.datetime.strptime(schedule['start'], '%H:%M').time()
            end_time = datetime.datetime.strptime(schedule['end'], '%H:%M').time()
            current_time = datetime.datetime.now().time()
            if start_time <= current_time <= end_time:
                return True
        return False
    
    # Chequeamos si el evento del canal es reciente, si ha pasado al menos 20 segundos desde el ultimo evento, no lo agregamos
    def check_if_recent_event(self, hikvision_event):
        channel = hikvision_event.get('channelID')
        
        channel_scheduled = self.check_if_scheduled(channel)
        if not channel_scheduled:
            logger.info(f"El canal {channel} no está programado para grabar, se ignora el evento.")
            return True, None
        
        last_event = self.get_last_event(channel)
        logger.debug(f"Ultimo evento en el canal {channel}: {last_event}")
        if last_event:
            last_event_time = datetime.datetime.strptime(last_event['timestamp'], "%Y-%m-%d %H:%M:%S")
            current_time = datetime.datetime.now()
            time_difference = (current_time - last_event_time).total_seconds()

            if time_difference < config.DIFFERENCE_TIME:
                logger.info(f'Evento reciente detectado en el canal {channel}, no se agrega nuevo evento.')
                return True, last_event

        logger.info(f'No hay eventos previos en el canal {channel}, se agrega nuevo evento.')
        alert_event = self.add_event(hikvision_event)
        return False, alert_event

