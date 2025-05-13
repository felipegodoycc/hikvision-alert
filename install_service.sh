#!/bin/bash

SERVICE_NAME="hikvision-alert"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SCRIPT_PATH="$(realpath "$0")"
INSTALL_DIR="$(dirname "$SCRIPT_PATH")"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install it before proceeding."
    exit 1
fi

# Create a virtual environment
VENV_DIR="${INSTALL_DIR}/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in ${VENV_DIR}..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment and install dependencies
echo "Installing dependencies in the virtual environment..."
source "$VENV_DIR/bin/activate"
pip install -r "$INSTALL_DIR/requirements.txt"
deactivate

# Create the service file with the virtual environment configured
echo "Creating service file at ${SERVICE_FILE}..."
sudo bash -c "cat > ${SERVICE_FILE}" <<EOL
[Unit]
Description=Hikvision Alert Service
After=network.target

[Service]
ExecStart=${VENV_DIR}/bin/python ${INSTALL_DIR}/__main__.py
WorkingDirectory=${INSTALL_DIR}
Restart=always
User=$(whoami)

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, enable and start the service
echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Enabling the ${SERVICE_NAME} service..."
systemctl enable ${SERVICE_NAME}

echo "Starting the ${SERVICE_NAME} service..."
systemctl start ${SERVICE_NAME}

echo "The ${SERVICE_NAME} service was successfully installed and started."