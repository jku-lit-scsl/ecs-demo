# Towards Resilient Edge-Architecture

## Setup

There is a shell script for setting up the environment.
It assumes the system it is running on is Ubuntu 20.04:

- `chmod +x setup.sh`
- `./setup.sh`
- update `config/config.py` with IPs of own machine + the server/client IPs
- start project running the virtual environment (printed out by the script) with the `main.py` file

These packages will be installed:
```bash
paho-mqtt
pytz
python-statemachine
pydot
# to generate statemachine images, graphviz is required and the PATH variable must be set
psutil
websockets
```