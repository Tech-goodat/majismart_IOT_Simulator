# Majismart — IoT Simulator

The Majismart Simulator is a Python-based telemetry generator that simulates a fleet of connected water meters.

It allows the Majismart platform to be developed and tested without requiring physical water-meter hardware.

The simulator generates realistic meter readings and publishes them to an MQTT broker using the same communication pattern expected from connected IoT devices.

## Architecture

```text
                  Python Simulator
                         │
                         ├── Meter 1
                         ├── Meter 2
                         ├── Meter 3
                         ├── ...
                         └── Meter N
                              │
                              ▼
                         MQTT Client
                              │
                              ▼
                         HiveMQ Cloud
                              │
                              ▼
                      Majismart Backend
```

## Features

* Simulates multiple water meters
* Generates continuous telemetry
* Simulates normal water consumption
* Supports leak-mode simulation
* Tracks cumulative consumption
* Publishes telemetry through MQTT
* Configurable meter count
* Automatic MQTT reconnection
* TLS support for secure MQTT connections

## Tech Stack

* **Python**
* **Paho MQTT**
* **python-dotenv**
* **MQTT**
* **HiveMQ Cloud**

## Simulated Meter

Each meter maintains:

```text
Meter ID
Flow rate
Total consumption
Status
Operating mode
Last reading timestamp
```

Example meter:

```text
MTR-00001
```

## Meter Modes

### Normal

Normal mode generates flow rates between:

```text
0.0 — 3.0 L/s
```

### Leak

Leak mode generates higher flow rates:

```text
4.0 — 6.0 L/s
```

This allows the simulator to produce abnormal telemetry that can later be used to test Majismart's leak and anomaly detection systems.

## MQTT Topics

Each meter publishes to:

```text
maji/meters/{meter_id}/telemetry
```

Example:

```text
maji/meters/MTR-00001/telemetry
```

## Telemetry Payload

The simulator publishes JSON payloads such as:

```json
{
  "meter_id": "MTR-00001",
  "flow_rate": 2.14,
  "total_consumption": 3299.34,
  "status": "ONLINE",
  "timestamp": "2026-09-17T10:30:00+00:00"
}
```

## Project Structure

```text
maji_simulator/
│
├── main.py
├── meter.py
├── simulator.py
├── telemetry.py
├── mqtt_client.py
├── requirements.txt
├── tests.py
├── tests/
├── README.md
└── .gitignore
```

### `meter.py`

Defines the individual simulated water meter and its telemetry generation logic.

### `simulator.py`

Creates and manages multiple simulated meters.

### `telemetry.py`

Defines the telemetry data structure and serialization logic.

### `mqtt_client.py`

Handles:

* MQTT connection
* Authentication
* TLS
* Publishing
* Reconnection

### `main.py`

Acts as the simulator entry point.

It continuously generates readings and publishes them to the MQTT broker.

## Local Setup

### Clone the repository

```bash
git clone <your-repository-url>
cd maji_simulator
```

### Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
METER_COUNT=20

MQTT_BROKER_HOST=your-hivemq-host
MQTT_BROKER_PORT=8883

MQTT_USERNAME=your-mqtt-username
MQTT_PASSWORD=your-mqtt-password

MQTT_USE_TLS=True
```

Never commit `.env` or MQTT credentials to the repository.

## Run the Simulator

```bash
python main.py
```

The simulator will create the configured number of meters and continuously publish telemetry.

For example:

```text
MTR-00001
MTR-00002
MTR-00003
...
MTR-00020
```

Telemetry is published approximately every two seconds.

## Example Output

```text
Connected to MQTT broker at your-hivemq-host:8883

Publish queued: 0
Publish completed: True

Published: maji/meters/MTR-00001/telemetry

Publish queued: 0
Publish completed: True

Published: maji/meters/MTR-00002/telemetry
```

## Why a Simulator?

Physical IoT hardware is not required during the early development stages of Majismart.

The simulator makes it possible to:

* Test MQTT communication
* Generate large volumes of telemetry
* Test backend persistence
* Test real-time dashboards
* Simulate abnormal water usage
* Develop anomaly detection
* Test the system before integrating physical meters

The simulator can eventually be replaced by real water-meter devices without fundamentally changing the backend's MQTT ingestion architecture.

## Future Improvements

Potential future capabilities include:

* Configurable consumption patterns
* Randomized meter failures
* Offline/online simulation
* Different household usage profiles
* Scheduled leaks
* Burst consumption events
* Large-scale simulations
* Device health simulation
* Command/control support

## Author

**Felix Kiprotich Cheruiyot**

Building Majismart as an applied IoT platform focused on telemetry, intelligent monitoring, anomaly detection, and AI-assisted decision making.
