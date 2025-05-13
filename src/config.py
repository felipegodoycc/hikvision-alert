# Config
import os
import dotenv
import yaml
import logging


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        dotenv.load_dotenv()
        
        # Base directory
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # Home assistant and Node-Red configuration
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL")
        
        # Hikvision configuration
        self.HIKVISION_IP = os.getenv("HIKVISION_IP")
        self.HIKVISION_USER = os.getenv("HIKVISION_USER")
        self.HIKVISION_PASSWORD = os.getenv("HIKVISION_PASSWORD")
        self.HIKVISION_URL_EVENT = os.getenv("HIKVISION_URL_EVENT", "ISAPI/Event/notification/alertStream")
        self.HIKVISION_SNAPSHOT = os.getenv("HIKVISION_SNAPSHOT", "ISAPI/Streaming/channels")
        self.TIME_TO_RECONNECT = int(os.getenv("TIME_TO_RECONNECT", 5))
        
        # Image analysis configuration
        self.IMAGE_STORAGE = os.getenv("IMAGE_STORAGE", "images")
        self.YOLO_DIR = os.getenv("YOLO_DIR", "yolo")
        self.YOLO_CONFIG = os.getenv("YOLO_CONFIG","yolov4-tiny.cfg")
        self.YOLO_WEIGHTS = os.getenv("YOLO_WEIGHTS","yolov4-tiny.weights")
        self.COCO_NAMES = os.getenv("COCO_NAMES","coco.names")
        self.CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.5))
        
        # Loki configuration
        self.LOKI_URL = os.getenv("LOKI_URL", None)

        # Cameras configuration
        config_path = os.path.join(self.BASE_DIR, '../config.yaml')
        with open(config_path, 'r') as file:
            yaml_config = yaml.safe_load(file)

        self.CAMERA_SCHEDULES = yaml_config.get('camera_schedules', {})
        self.CAMERAS_NAME = yaml_config.get('cameras_name', {})
        self.TIME_ZONE = yaml_config.get('time_zone', 'UTC')

        # Events configuration
        self.DIFFERENCE_TIME = int(os.getenv("DIFFERENCE_TIME", 5))
        self.MAX_EVENTS = int(os.getenv("MAX_EVENTS", 100))
        
        # Validamos y mostramos la configuración al inicializar
        self.validate()
        self.print_config()

    def validate(self):
        required_vars = [
            "WEBHOOK_URL",
            "HIKVISION_IP",
            "HIKVISION_USER",
            "HIKVISION_PASSWORD"
        ]
        missing_vars = [var for var in required_vars if not getattr(self, var)]
        if missing_vars:
            raise EnvironmentError(f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}")
        
    def print_config(self):
        logger = logging.getLogger("Config")
        logger.info("Configuración actual:")
        logger.info(f"WEBHOOK_URL: {self.WEBHOOK_URL}")
        logger.info(f"HIKVISION_IP: {self.HIKVISION_IP}")
        logger.info(f"HIKVISION_USER: {self.HIKVISION_USER}")
        logger.info(f"HIKVISION_PASSWORD: {self.HIKVISION_PASSWORD}")
        logger.info(f"HIKVISION_URL_EVENT: {self.HIKVISION_URL_EVENT}")
        logger.info(f"HIKVISION_SNAPSHOT: {self.HIKVISION_SNAPSHOT}")
        logger.info(f"TIME_TO_RECONNECT: {self.TIME_TO_RECONNECT}")
        logger.info(f"IMAGE_STORAGE: {self.IMAGE_STORAGE}")
        logger.info(f"YOLO_DIR: {self.YOLO_DIR}")
        logger.info(f"YOLO_CONFIG: {self.YOLO_CONFIG}")
        logger.info(f"YOLO_WEIGHTS: {self.YOLO_WEIGHTS}")
        logger.info(f"COCO_NAMES: {self.COCO_NAMES}")
        logger.info(f"CONFIDENCE_THRESHOLD: {self.CONFIDENCE_THRESHOLD}")
        logger.info(f"LOKI_URL: {self.LOKI_URL}")
        logger.info(f"CAMERA_SCHEDULES: {self.CAMERA_SCHEDULES}")
        logger.info(f"CAMERAS_NAME: {self.CAMERAS_NAME}")
        logger.info(f"TIME_ZONE: {self.TIME_ZONE}")
        logger.info(f"DIFFERENCE_TIME: {self.DIFFERENCE_TIME}")
        logger.info(f"MAX_EVENTS: {self.MAX_EVENTS}")


# Punto de acceso global a la configuración
config = Config()