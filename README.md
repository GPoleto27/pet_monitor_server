# Pet Monitor Server

This repository contains the server code for the Pet Monitor project. The server is responsible for receiving data from the client and storing it in a database and communicating with the embbeded system for Pet Monitor. The server also provides a GraphQL API for querying the data. 

## Getting Started

This server is designed to run on a Raspberry Pi 3b+ running Raspberry Pi OS Lite. It should work on newer versions of the Raspberry Pi, but this has not been tested.

### Prerequisites

#### Install Raspberry Pi OS Lite

Download the latest version of Raspberry Pi OS Lite from the [Raspberry Pi website](https://www.raspberrypi.org/software/operating-systems/). Follow the instructions on the website to flash the image to an SD card. On flashing set up the WiFi connection and enable SSH.

#### Install the dependencies

Python 3.9.2 is required to run the server, it should already be available on Raspberry Pi OS Lite, if not, install Python 3.9.2 by running the following commands:

```bash
sudo apt update
sudo apt install python3.9
```

This project also depends on:
- pip
- mosquitto
- mosquitto-clients
- MariaDB

These dependencies can be installed by running the following commands:

```bash
make install
```

This will install the O.S. dependencies and set up the configuration files for the server as well as the python dependencies.

### Running the server

To run the server, run the following command:

```bash
make start
```

This will start the MQTT broker, MariaDB and the server. The server will be available on port 5000.

### Stopping the server

To stop the server, run the following command:

```bash
make stop
```

This will stop the MQTT broker, MariaDB and the server.

### Restarting the server

To restart the server, run the following command:

```bash
make restart
```

This will restart the MQTT broker, MariaDB and the server.

### Checking the server status

To check the status of the server, run the following commands:

```bash
make status_mqtt
```

```bash
make status_mariadb
```
