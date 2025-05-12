# Hikvision Alert

Este proyecto está diseñado para procesar eventos de cámaras Hikvision, analizar imágenes utilizando un modelo YOLO y enviar notificaciones a través de webhooks.

## Características
- Conexión al stream de eventos de cámaras Hikvision.
- Análisis de imágenes con YOLO para detectar objetos de interés.
- Gestión de eventos recientes y horarios de grabación.
- Envío de notificaciones a través de webhooks.
- Registro de eventos en Loki para análisis posterior.

## Requisitos
- Python 3.10 o superior.
- Dependencias listadas en `requirements.txt`.
- Archivo de configuración `.env` con las siguientes variables:
  ```env
  # Configuración de Hikvision (Obligatorias)
  HIKVISION_USER=tu_usuario_hikvision
  HIKVISION_PASSWORD=tu_contraseña_hikvision
  HIKVISION_IP=ip_de_tu_cámara_hikvision
  HIKVISION_URL_EVENT=endpoint_de_eventos_hikvision # Predeterminado: ISAPI/Event/notification/alertStream
  HIKVISION_SNAPSHOT=endpoint_de_snapshot_hikvision # Predeterminado: ISAPI/Streaming/channels

  # Configuración del Webhook (Obligatoria)
  WEBHOOK_URL=url_completa_del_webhook_para_eventos

  # Almacenamiento de imágenes (Con valor predeterminado)
  IMAGE_STORAGE=directorio_para_guardar_imágenes # Predeterminado: images

  # Configuración de OpenCV (Con valores predeterminados)
  YOLO_DIR=directorio_del_modelo_yolo # Predeterminado: yolo
  YOLO_CONFIG=archivo_de_configuración_yolo # Predeterminado: yolov4-tiny.cfg
  YOLO_WEIGHTS=archivo_de_pesos_yolo # Predeterminado: yolov4-tiny.weights
  COCO_NAMES=archivo_de_clases_coco # Predeterminado: coco.names
  CONFIDENCE_THRESHOLD=umbral_de_confianza_para_detección # Predeterminado: 0.5

  # Configuración de eventos (Con valores predeterminados)
  MAX_EVENTS=número_máximo_de_eventos_a_guardar # Predeterminado: 100
  DIFFERENCE_TIME=tiempo_en_segundos_entre_eventos_relevantes # Predeterminado: 15

  # Configuración de Loki (Opcional)
  LOKI_URL=url_de_tu_servidor_loki
  ```

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/hikvision-alert.git
   cd hikvision-alert
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura el archivo `.env` con tus credenciales y parámetros.

4. Asegúrate de que el archivo `config.yaml` contenga los horarios y nombres de las cámaras:
   ```yaml
   camera_schedules:
     '1':
       start: '22:00'
       end: '08:00'
     '2':
       start: '00:00'
       end: '23:59'
   cameras_name:
     '1': 'Acceso principal'
     '2': 'Exterior Oriente'
   ```

## Uso
Ejecuta el archivo principal para iniciar el procesamiento de eventos:
```bash
python __main__.py
```

## Estructura del Proyecto
- `__main__.py`: Punto de entrada principal.
- `src/config.py`: Gestión de configuración.
- `src/events.py`: Gestión de eventos.
- `src/hikvision_api.py`: Conexión con cámaras Hikvision.
- `src/image_analizer.py`: Análisis de imágenes con YOLO.
- `src/utils.py`: Funciones utilitarias.

## Contribuciones
¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
