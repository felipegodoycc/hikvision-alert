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
  HIKVISION_URL_EVENT=hikvision_event_endpoint              # Default: ISAPI/Event/notification/alertStream
  HIKVISION_SNAPSHOT=hikvision_snapshot_endpoint            # Default: ISAPI/Streaming/channels

  # Webhook Configuration (Required)
  WEBHOOK_URL=full_url_of_the_webhook_for_events

  # Image Storage (Default Value)
  IMAGE_STORAGE=directory_to_store_images                   # Default: images

  # OpenCV Configuration (Default Values)
  YOLO_DIR=yolo_model_directory                             # Default: yolo
  YOLO_CONFIG=yolo_configuration_file                       # Default: yolov4-tiny.cfg
  YOLO_WEIGHTS=yolo_weights_file                            # Default: yolov4-tiny.weights
  COCO_NAMES=coco_classes_file                              # Default: coco.names
  CONFIDENCE_THRESHOLD=detection_confidence_threshold       # Default: 0.5

  # Event Configuration (Default Values)
  MAX_EVENTS=maximum_number_of_events_to_store              # Default: 100
  DIFFERENCE_TIME=seconds_between_relevant_events           # Default: 15

  # Loki Configuration (Optional)
  LOKI_URL=your_loki_server_url                             # If not set, Loki logging is disabled

  # Logger configuration (Optional)
  LOGGER_LEVEL=DEBUG
  ```
- Your Hikvision DVR must be configured to send alerts to event stream. This is usually done through the web interface of the DVR.

## Configure Hikvision DVR

1. Access the web interface of your Hikvision DVR.
2. Navigate to the "Configuration" section.
3. In the sidebar, go to the "Intelligent" section.
4. Select the event type you want to receive alerts for (e.g., motion detection).
5. Choose the camera you want to configure.
6. Enable the event type and configure the "Link action" to send an alert to "Notify remote software".

## Usage as script
1. Clone this repository:
   ```bash
   git clone https://github.com/your_user/hikvision-alert.git
   cd hikvision-alert
   ```

2. Install python (if not already installed):
   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```

3. Create a virtual environment:
   ```bash
    python3 -m venv venv
    ```

3. Install the dependencies:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Configure the `.env` file with your credentials and parameters.

5. Ensure the `config.yaml` file contains the schedules and names of the cameras:

   > **IMPORTANT**: The camera ID must match the one in your Hikvision DVR. Check your DVR to get the correct camera ID. Normally, the camera ID is same of the channel number.

   ```yaml
   camera_schedules:
     '1':
       start: '22:00' # Night
       end: '08:00'
     '2':
       start: '00:00' # All day
       end: '23:59'
   cameras_name:
     '1': 'Main Entrance'
     '2': 'East Exterior'
   ```

   If you want to use the default configuration, you can skip this step. The default configuration is set to record all events from all cameras.

6. Run the application:
   ```bash
   python __main__.py
   ``` 

## Install as a service

1. Clone this repository:
   ```bash
    git clone
    cd hikvision-alert
   ```

2. Install python (if not already installed):
   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```

3. Execute the `install_service.sh` script:
   ```bash
   chmod +x install_service.sh
   ./install_service.sh # If you dont have permission, use sudo
   ```

4. Configure the `.env` file with your credentials and parameters.
5. Ensure the `config.yaml` file contains the schedules and names of the cameras:

   > **IMPORTANT**: The camera ID must match the one in your Hikvision DVR. Check your DVR to get the correct camera ID. Normally, the camera ID is same of the channel number.

   ```yaml
   camera_schedules:
     '1':
       start: '22:00' # Night
       end: '08:00'
     '2':
       start: '00:00' # All day
       end: '23:59'
   cameras_name:
     '1': 'Main Entrance'
     '2': 'East Exterior'
   ```

6. Enable and start the service:
   ```bash
   sudo systemctl enable hikvision-alert
   sudo systemctl start hikvision-alert
   ```

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

## Issues
If you encounter any issues, please open an issue on GitHub. Include details about your environment and the steps to reproduce the problem.

## License
This project is under the MIT License. See the `LICENSE` file for more details.
