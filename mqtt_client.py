
import os
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

    def publish(self, topic, payload):
        result = self.client.publish(
            topic,
            payload
        )

        print(
            f"Publish queued: {result.rc}"
        )

        result.wait_for_publish()

        print(
            f"Publish completed: {result.is_published()}"
        )