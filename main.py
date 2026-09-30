import os
import time
import json

from dotenv import load_dotenv

from simulator import Simulator
from mqtt_client import MQTTClient

load_dotenv()

meter_count = int(os.getenv("METER_COUNT", "20"))

simulator = Simulator(meter_count)

mqtt_client = MQTTClient(simulator)
mqtt_client.connect()

while True:
    readings = simulator.generate_readings()

    for reading in readings:
        topic = f"maji/meters/{reading.meter_id}/telemetry"
        payload = json.dumps(reading.to_dict())

        mqtt_client.publish(topic, payload)

        print(f"Published: {topic}")

    time.sleep(2)