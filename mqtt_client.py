import os
import time
import json

import paho.mqtt.client as mqtt


class MQTTClient:

    def __init__(self, simulator):

        self.simulator = simulator

        self.broker = os.getenv(
            "MQTT_BROKER_HOST",
            "localhost"
        )

        self.port = int(
            os.getenv(
                "MQTT_BROKER_PORT",
                "1883"
            )
        )

        self.username = os.getenv("MQTT_USERNAME")
        self.password = os.getenv("MQTT_PASSWORD")

        self.use_tls = os.getenv(
            "MQTT_USE_TLS",
            "False"
        ) == "True"

        self.client = mqtt.Client()

        if self.username and self.password:
            self.client.username_pw_set(
                self.username,
                self.password
            )

        if self.use_tls:
            self.client.tls_set()

        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_disconnect(self, client, userdata, rc):
        print(
            f"MQTT disconnected. Return code: {rc}"
        )

    def on_message(self, client, userdata, msg):

        try:
            payload = msg.payload.decode()

            data = json.loads(payload)

            meter_id = data["meter_id"]
            valve_open = data["valve_open"]
            closure_source = data["closure_source"]

            print(
                f"Command received for {meter_id}: "
                f"valve_open={valve_open}, "
                f"closure_source={closure_source}"
            )

            self.simulator.set_valve_state(
                meter_id=meter_id,
                valve_open=valve_open,
                closure_source=closure_source
            )

        except Exception as error:

            print(
                f"Failed to process MQTT command: {error}"
            )

    def connect(self):

        self.client.connect(
            self.broker,
            self.port
        )

        self.client.subscribe(
            "maji/meters/+/command"
        )

        self.client.loop_start()

        print(
            f"Connected to MQTT broker at "
            f"{self.broker}:{self.port}"
        )

        print(
            "Subscribed to maji/meters/+/command"
        )

    def reconnect(self):

        while not self.client.is_connected():

            try:

                print(
                    "MQTT connection lost. Reconnecting..."
                )

                self.client.reconnect()

                print(
                    "MQTT reconnected."
                )

            except Exception as error:

                print(
                    f"Reconnect failed: {error}"
                )

                time.sleep(2)

    def publish(self, topic, payload):

        self.reconnect()

        result = self.client.publish(
            topic,
            payload
        )

        if result.rc != mqtt.MQTT_ERR_SUCCESS:

            print(
                f"Publish failed with code: {result.rc}"
            )

            return

        print(
            f"Publish queued: {result.rc}"
        )

        result.wait_for_publish()

        print(
            f"Publish completed: "
            f"{result.is_published()}"
        )