# Hikvision Alert

This project is designed to process events from Hikvision cameras in DVR, analyze images using a YOLO model, and send notifications via webhooks. In my case, I send it to Node-Red in my HomeAssistant for analysis with an LLM, and depending on the result, I send a notification to Telegram.

## Features
- Connection to the event stream of Hikvision cameras.
- Image analysis with YOLO to detect objects of interest.
- Management of recent events and recording schedules.
- Sending notifications via webhooks.
- Logging events to Loki for later analysis (optional).

## Requirements
- Python 3.10 or higher.
- Dependencies listed in `requirements.txt`.
- Configuration file `.env` with the following variables:
  ```env
  # Hikvision Configuration (Required)
  HIKVISION_USER=your_hikvision_user
  HIKVISION_PASSWORD=your_hikvision_password
  HIKVISION_IP=your_hikvision_camera_ip
  HIKVISION_URL_EVENT=hikvision_event_endpoint # Default: ISAPI/Event/notification/alertStream
  HIKVISION_SNAPSHOT=hikvision_snapshot_endpoint # Default: ISAPI/Streaming/channels

  # Webhook Configuration (Required)
  WEBHOOK_URL=full_url_of_the_webhook_for_events

  # Image Storage (Default Value)
  IMAGE_STORAGE=directory_to_store_images # Default: images

  # OpenCV Configuration (Default Values)
  YOLO_DIR=yolo_model_directory # Default: yolo
  YOLO_CONFIG=yolo_configuration_file # Default: yolov4-tiny.cfg
  YOLO_WEIGHTS=yolo_weights_file # Default: yolov4-tiny.weights
  COCO_NAMES=coco_classes_file # Default: coco.names
  CONFIDENCE_THRESHOLD=detection_confidence_threshold # Default: 0.5

  # Event Configuration (Default Values)
  MAX_EVENTS=maximum_number_of_events_to_store # Default: 100
  DIFFERENCE_TIME=seconds_between_relevant_events # Default: 15

  # Loki Configuration (Optional)
  LOKI_URL=your_loki_server_url
  ```

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your_user/hikvision-alert.git
   cd hikvision-alert
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the `.env` file with your credentials and parameters.

4. Ensure the `config.yaml` file contains the schedules and names of the cameras:
   ```yaml
   camera_schedules:
     '1':
       start: '22:00'
       end: '08:00'
     '2':
       start: '00:00'
       end: '23:59'
   cameras_name:
     '1': 'Main Entrance'
     '2': 'East Exterior'
   ```

## Usage
Run the main file to start processing events:
```bash
python __main__.py
```

## Setting Up as a Service

You can set up this project as a systemd service using the `install_service.sh` script. This will ensure the application runs automatically on system startup.

### Steps:
1. Make the script executable:
   ```bash
   chmod +x install_service.sh
   ```

2. Run the script:
   ```bash
   ./install_service.sh
   ```

The script will:
- Check if Python 3 is installed.
- Create a virtual environment in the project directory.
- Install the required dependencies from `requirements.txt`.
- Create a systemd service file to run the application.
- Enable and start the service.

### Managing the Service
- To check the status of the service:
  ```bash
  sudo systemctl status hikvision-alert
  ```

- To stop the service:
  ```bash
  sudo systemctl stop hikvision-alert
  ```

- To restart the service:
  ```bash
  sudo systemctl restart hikvision-alert
  ```

## Project Structure
- `__main__.py`: Main entry point.
- `src/config.py`: Configuration management.
- `src/events.py`: Event management.
- `src/hikvision_api.py`: Connection with Hikvision cameras.
- `src/image_analizer.py`: Image analysis with YOLO.
- `src/utils.py`: Utility functions.

## Contributions
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is under the MIT License. See the `LICENSE` file for more details.
