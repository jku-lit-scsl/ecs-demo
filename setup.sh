#!/bin/bash

NTP_SERVERS=(
    "server at.pool.ntp.org iburst"
    "server europe.pool.ntp.org iburst"
    "server ntps1-0.cs.tu-berlin.de iburst"
    "server ntps1-1.cs.tu-berlin.de iburst"
)

sudo timedatectl set-timezone Europe/Vienna


# Set up Git credential caching
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=43200'

# Install required tools
sudo apt-get install -y build-essential python3.11 python3.11-venv python3.11-dev ntp

# Add NTP servers to the configuration
{
    echo "# Custom NTP servers"
    for server in "${NTP_SERVERS[@]}"; do
        echo "server $server iburst"
    done
} | sudo tee /etc/ntp.conf

# Restart and enable NTP service
sudo systemctl restart ntp
sudo systemctl enable ntp

# Display the NTP service status
echo "NTP service status:"
sudo systemctl status ntp | grep "Active"

# Create a Python virtual environment
python3.11 -m venv venv311
source venv311/bin/activate

# Install requirements from requirements
pip install -r resources/requirements.txt

# Display the path of the Python interpreter
which python

# Deactivate the virtual environment
deactivate
