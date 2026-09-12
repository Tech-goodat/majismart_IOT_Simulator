import time
import json

from meter import Meter
from simulator import Simulator
from mqtt_client import MQTTClient


simulator=Simulator(20)
mqtt_client=MQTTClient()
mqtt_client.connect()

while True:
    readings=simulator.generate_readings()
    for reading in readings:
        topic=f"maji/meters/{reading.meter_id}/telemetry"
        payload=json.dumps(reading.to_dict())
        mqtt_client.publish(topic, payload)
        print(f"Published : {topic}")

    time.sleep(2)