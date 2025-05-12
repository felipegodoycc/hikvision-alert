import os
import cv2

from .config import config
from .utils import config_logger, timeit

logger = config_logger()

class ImageAnalizer():
    def __init__(self):
        self.YOLO_NET = None
        self.YOLO_CLASSES = None
        self.YOLO_OUTPUT_LAYERS = None
        
    # Cargamos el modelo YOLO
    @timeit
    def load_model(self):
        logger.info("Cargando modelo YOLO...")
        model_path = os.path.join(config.BASE_DIR, config.YOLO_DIR)
        yolo_config_path = os.path.join(model_path, config.YOLO_CONFIG)
        yolo_weights_path = os.path.join(model_path, config.YOLO_WEIGHTS)
        
        self.YOLO_NET = cv2.dnn.readNetFromDarknet(yolo_config_path, yolo_weights_path)
        self.YOLO_NET.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        
        layer_names = self.YOLO_NET.getLayerNames()
        self.YOLO_OUTPUT_LAYERS = [layer_names[i - 1] for i in self.YOLO_NET.getUnconnectedOutLayers()]

        with open(os.path.join(model_path, config.COCO_NAMES), "r") as f:
            self.YOLO_CLASSES = [line.strip() for line in f.readlines()]

    @timeit
    def detectar_objetos(self, path_img, clases_interes={"person", "car"}):
        img = cv2.imread(path_img)
        if img is None:
            return []

        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 1/255.0, (608, 608), swapRB=True, crop=False)
        self.YOLO_NET.setInput(blob)
        outputs = self.YOLO_NET.forward(self.YOLO_OUTPUT_LAYERS)

        encontrados = set()
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = scores.argmax()
                confidence = scores[class_id]
                if confidence > config.CONFIDENCE_THRESHOLD:
                    label = self.YOLO_CLASSES[class_id]
                    if label in clases_interes:
                        encontrados.add(label)

        return list(encontrados)