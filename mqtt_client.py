import os
import time
import paho.mqtt.client as mqtt


class MQTTClient:

    def __init__(self):

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

    def on_disconnect(self, client, userdata, rc):
        print(
            f"MQTT disconnected. Return code: {rc}"
        )

    def connect(self):

        self.client.connect(
            self.broker,
            self.port
        )

        self.client.loop_start()

        print(
            f"Connected to MQTT broker at "
            f"{self.broker}:{self.port}"
        )

    def reconnect(self):

        while not self.client.is_connected():

            try:
                print("MQTT connection lost. Reconnecting...")

                self.client.reconnect()

                print("MQTT reconnected.")

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
            f"Publish completed: {result.is_published()}"
        )