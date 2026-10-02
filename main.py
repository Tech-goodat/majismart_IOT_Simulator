import os
import time
import json
import urllib.request
import urllib.error

from dotenv import load_dotenv

from simulator import Simulator
from mqtt_client import MQTTClient


load_dotenv()


DJANGO_API_URL = os.getenv(
    "DJANGO_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


def get_active_meters():

    url = (
        f"{DJANGO_API_URL}"
        "/meters/active/"
    )

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json"
        },
        method="GET"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=10
        ) as response:

            data = json.loads(
                response.read().decode()
            )

            return data

    except urllib.error.HTTPError as error:

        print(
            f"Failed to fetch active meters. "
            f"HTTP {error.code}"
        )

        return None

    except urllib.error.URLError as error:

        print(
            f"Could not connect to Django: "
            f"{error.reason}"
        )

        return None

    except Exception as error:

        print(
            f"Failed to fetch active meters: "
            f"{error}"
        )

        return None


simulator = Simulator()


mqtt_client = MQTTClient(
    simulator
)

mqtt_client.connect()


telemetry_interval = float(
    os.getenv(
        "TELEMETRY_INTERVAL",
        "2"
    )
)


sync_interval = float(
    os.getenv(
        "METER_SYNC_INTERVAL",
        "10"
    )
)


last_sync_time = 0


while True:

    current_time = time.time()

    if (
        current_time - last_sync_time
        >= sync_interval
    ):

        active_meters = (
            get_active_meters()
        )

        if active_meters is not None:

            simulator.sync_active_meters(
                active_meters
            )

            print(
                "Active meters from Django:"
            )

            for meter in active_meters:

                print(
                    f" - "
                    f"{meter['meter_number']} | "
                    f"Valve: "
                    f"{'OPEN' if meter['valve_open'] else 'CLOSED'} | "
                    f"Source: "
                    f"{meter['closure_source']}"
                )

            last_sync_time = current_time

    readings = (
        simulator.generate_readings()
    )

    for reading in readings:

        topic = (
            f"maji/meters/"
            f"{reading.meter_id}"
            f"/telemetry"
        )

        payload = json.dumps(
            reading.to_dict()
        )

        mqtt_client.publish(
            topic,
            payload
        )

        print(
            f"Published: {topic}"
        )

    time.sleep(
        telemetry_interval
    )